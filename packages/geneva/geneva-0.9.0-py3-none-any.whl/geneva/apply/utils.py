# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import hashlib
import itertools
import json
import logging
import random
import re
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any, Optional, TypeVar

import lance
import more_itertools
import pyarrow as pa
import pyarrow.compute as pc
from yarl import URL

from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, MapTask
from geneva.checkpoint import CheckpointStore
from geneva.transformer import BACKFILL_SELECTED

if TYPE_CHECKING:
    from lance_namespace import LanceNamespace

_LOG = logging.getLogger(__name__)


def _legacy_map_task_key(map_task: MapTask) -> str:
    """Best-effort reconstruction of pre-range map task key."""
    try:
        return map_task.legacy_map_task_key(where=getattr(map_task, "where", None))
    except Exception:
        return "unknown"


def _legacy_fragment_dedupe_key(uri: str, frag_id: int, map_task: MapTask) -> str:
    key = f"{uri}:{frag_id}:{_legacy_map_task_key(map_task)}"
    return hashlib.sha256(key.encode()).hexdigest()


def _parse_checkpoint_ranges_for_fragment(
    *,
    checkpoint_store: CheckpointStore,
    prefixes: list[str],
    frag_id: int,
) -> list[tuple[int, int]]:
    """
    Collect checkpointed row ranges for a fragment.

    This is a thin wrapper over `_iter_checkpoint_ranges_for_fragment` that
    discards the checkpoint keys and returns only the covered ranges.
    Callers typically feed the result into `_merge_ranges` and
    `_compute_missing_ranges` during `plan_read` to avoid re-scanning rows that
    have already been checkpointed.

    Returns:
        A list of ranges `[start, end)` (0-based, fragment-local; start inclusive,
        end exclusive).
    """
    # `_iter_checkpoint_ranges_for_fragment` yields (key, start, end). We only
    # need the numeric ranges here.
    return [
        r[1:]
        for r in _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=checkpoint_store, prefixes=prefixes, frag_id=frag_id
        )
    ]


def _iter_checkpoint_ranges_for_fragment(
    *,
    checkpoint_store: CheckpointStore,
    prefixes: list[str],
    frag_id: int,
) -> list[tuple[str, int, int]]:
    """
    Enumerate per-batch checkpoints for a fragment.

    We intentionally *list and parse existing checkpoint keys* rather than
    probing at fixed steps of `checkpoint_size`. This makes `plan_read`
    resilient to:
    - legacy checkpoints (task-level or different naming),
    - future adaptive checkpoint sizes (varying batch lengths),
    - partial progress where only some batches exist.

    Expected key format (suffix):
        "..._frag-{frag_id}_range-{start}-{end}"

    Where `start`/`end` are 0-based, fragment-local row offsets and represent
    `[start, end)` (start inclusive, end exclusive). Any key that doesn't match
    this format is ignored.

    Returns:
        A list of tuples `(key, start, end)` for matching checkpoints.
    """

    ranges: list[tuple[str, int, int]] = []
    # We only care about checkpoints that were written for this fragment.
    marker = f"_frag-{frag_id}_range-"

    # `CheckpointStore` may contain keys from multiple datasets / tasks, so we
    # restrict listing to the relevant key prefixes. We de-duplicate across
    # prefixes because callers may include multiple compatible prefix shapes
    # (e.g., legacy keys without srcfiles hashes).
    seen: set[str] = set()
    for prefix in prefixes:
        # Narrow listing to keys for this specific fragment/range shape. This
        # avoids scanning unrelated fragment checkpoints that share the same
        # dataset/task prefix.
        for key in checkpoint_store.list_keys(prefix=f"{prefix}{marker}"):
            if key in seen:
                continue
            seen.add(key)
            try:
                # Split once at the marker to isolate "start-end" suffix.
                suffix = key.split(marker, 1)[1]
                start_str, end_str = suffix.split("-", 1)
                start = int(start_str)
                end = int(end_str)
                # Only accept well-formed, non-empty `[start, end)` ranges.
                if end > start:
                    ranges.append((key, start, end))
            except Exception as exc:
                # Be permissive: ignore malformed / legacy keys instead of failing
                # planning. This avoids a single bad key blocking progress.
                _LOG.debug(
                    "Skipping malformed checkpoint key %s: %s",
                    key,
                    exc,
                    exc_info=True,
                )

    return ranges


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges.

    Input ranges are interpreted as `[start, end)` offsets (0-based, start
    inclusive, end exclusive). After sorting by `start`, we coalesce any range
    whose start is `<=` the previous end. This treats adjacent ranges (e.g.,
    [0,5) and [5,7)) as continuous coverage.

    Returns:
        A sorted, non-overlapping list of merged ranges.
    """
    if not ranges:
        return []
    # Sort so we can sweep left-to-right.
    ranges = sorted(ranges, key=lambda r: r[0])
    merged = [ranges[0]]
    for s, e in ranges[1:]:
        last_s, last_e = merged[-1]
        # Overlap or adjacency => extend the previous coverage window.
        if s <= last_e:
            merged[-1] = (last_s, max(last_e, e))
        else:
            # Gap => start a new coverage window.
            merged.append((s, e))
    return merged


def _compute_missing_ranges(
    *,
    total_rows: int,
    task_size: int,
    covered: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """
    Compute read-task ranges that are not covered by checkpoints.

    Args:
        total_rows: Total number of rows in the fragment.
        task_size: Desired read-task size. Each returned task has
            `limit <= task_size` unless `task_size <= 0`.
        covered: Sorted, merged checkpoint coverage ranges `[start, end)`.

    Returns:
        A list of `(offset, limit)` pairs describing missing regions to scan.
        Here `offset` is the fragment-local row start, and `limit` is the
        number of rows to read for that task.
    """

    # First compute complement gaps of `covered` within [0, total_rows).
    gaps: list[tuple[int, int]] = []
    cur = 0
    for s, e in covered:
        if cur < s:
            gaps.append((cur, s))
        cur = max(cur, e)
    if cur < total_rows:
        gaps.append((cur, total_rows))

    # Then split each gap into one or more tasks of size `task_size`.
    tasks: list[tuple[int, int]] = []
    for start, end in gaps:
        remaining = end - start
        if task_size <= 0:
            # Degenerate / test case: treat the whole gap as a single task.
            tasks.append((start, remaining))
            continue
        while remaining > task_size:
            # Full-sized tasks.
            tasks.append((start, task_size))
            start += task_size
            remaining -= task_size
        if remaining > 0:
            # Final tail task (shorter than task_size).
            tasks.append((start, remaining))

    return tasks


def _count_udf_rows(batch: pa.RecordBatch | list[dict[str, Any]]) -> int:
    """
    Count the number of rows that will execute a UDF within the provided batch.

    The BACKFILL_SELECTED column (when present) identifies the subset of rows
    whose UDF should be evaluated. When the column is absent we assume all rows
    execute the UDF.
    """
    if isinstance(batch, pa.RecordBatch):
        if BACKFILL_SELECTED in batch.schema.names:
            mask = batch[BACKFILL_SELECTED]
            # pyarrow.compute.sum skips nulls by default, treating them as zero.
            summed = pc.sum(mask)
            value = summed.as_py() if hasattr(summed, "as_py") else summed
            return int(value or 0)
        return int(batch.num_rows)

    if not batch:
        return 0

    # this is the blob case where the batch is a list of dicts
    count = 0
    for row in batch:
        if not isinstance(row, dict):
            count += 1
            continue
        selected = row.get(BACKFILL_SELECTED, True)
        if selected:
            count += 1
    return count


def _check_fragment_data_file_exists(
    uri: str,
    frag_id: int,
    map_task: MapTask,
    checkpoint_store: CheckpointStore,
    dataset_version: int | str | None = None,
    src_files_hash: str | None = None,
    current_output_field_ids: frozenset[int] | None = None,
    current_data_files: frozenset[str] | None = None,
    namespace: Optional["LanceNamespace"] = None,
    table_id: Optional[list[str]] = None,
    storage_options: Optional[dict[str, str]] = None,
) -> bool:
    """
    Check if a fragment data file already exists in staging or target locations.

    Returns True if the fragment can be skipped because its data file already exists.
    """
    # Import here to avoid circular imports
    from geneva.runners.ray.pipeline import _get_fragment_dedupe_key

    # Get the fragment's checkpoint key
    dedupe_key = _get_fragment_dedupe_key(
        uri,
        frag_id,
        map_task,
        dataset_version=dataset_version,
        src_files_hash=src_files_hash,
    )
    if dedupe_key not in checkpoint_store:
        # Backward compatibility for pre-change checkpoint keys.
        dedupe_key = _legacy_fragment_dedupe_key(uri, frag_id, map_task)

    # Check if fragment is already checkpointed
    if dedupe_key not in checkpoint_store:
        return False

    try:
        # Get the stored file path from checkpoint
        checkpointed_data = checkpoint_store[dedupe_key]
        if "file" not in checkpointed_data.schema.names:
            return False

        file_list = checkpointed_data["file"].to_pylist()
        file_path = "".join(str(f) for f in file_list if f is not None)
        if not file_path:
            return False

        if (
            current_output_field_ids is not None
            and "output_field_ids" in checkpointed_data.schema.names
        ):
            stored_json = checkpointed_data["output_field_ids"][0].as_py()
            if stored_json is None:
                return False
            stored_field_ids = frozenset(json.loads(stored_json))
            if stored_field_ids != current_output_field_ids:
                _LOG.info(
                    f"Fragment {frag_id} output field IDs changed; "
                    "invalidating checkpoint"
                )
                return False

        if current_data_files is not None and file_path not in current_data_files:
            _LOG.info(
                f"Fragment {frag_id} checkpoint file not in current data files; "
                "invalidating checkpoint"
            )
            return False

        # Check staging location first (dataset/data/{file}.lance)
        base_url = URL(uri)
        if base_url.scheme == "":
            base_url = URL(f"file://{uri}")

        # For Lance datasets, the URI ends with .lance, get the parent directory
        if str(base_url).endswith(".lance"):
            base_url = base_url.parent

        staging_url = base_url / "data" / file_path

        try:
            # Check if the staging file exists using lance's file system abstraction
            from pyarrow.fs import FileSystem, FileType

            fs, path = FileSystem.from_uri(str(staging_url))
            file_info = fs.get_file_info(path)

            if file_info.type != FileType.NotFound:
                _LOG.info(
                    f"Fragment {frag_id} data file exists in staging: {staging_url}"
                )
                return True
        except Exception as e:
            _LOG.debug(f"Failed to check staging location {staging_url}: {e}")

        # Check target table location as fallback
        # The file might have been moved/committed to the main dataset
        if namespace and table_id:
            dataset = lance.dataset(
                namespace=namespace,
                table_id=table_id,
                storage_options=storage_options,
            )
        else:
            dataset = lance.dataset(uri, storage_options=storage_options)

        try:
            fragment = dataset.get_fragment(frag_id)
            if fragment is not None:
                # Check if any data files in the fragment match our expected file
                for data_file in fragment.data_files():
                    if data_file.path == file_path:
                        _LOG.info(
                            f"Fragment {frag_id} data file exists in target: "
                            f"{data_file.path}"
                        )
                        return True
        except Exception as e:
            _LOG.debug(f"Failed to check target location for fragment {frag_id}: {e}")

    except Exception as e:
        _LOG.debug(f"Failed to check fragment data file for {frag_id}: {e}")

    return False


def _num_tasks(
    *,
    uri: str,
    read_version: int | None = None,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    namespace_client: Optional["LanceNamespace"] = None,
    table_id: Optional[list[str]] = None,
) -> int:
    if task_size <= 0:
        return 1

    # Open dataset with namespace if available
    if namespace_client and table_id:
        dataset = lance.dataset(
            namespace=namespace_client,
            table_id=table_id,
            version=read_version,
        )
    else:
        dataset = lance.dataset(uri, version=read_version)

    return sum(-(-frag.count_rows() // task_size) for frag in dataset.get_fragments())


T = TypeVar("T")


def _buffered_shuffle(it: Iterator[T], buffer_size: int) -> Iterator[T]:
    """Shuffle an iterator using a buffer of size buffer_size
    not perfectly random, but good enough for spreading out IO
    """
    # Initialize the buffer with the first buffer_size items from the iterator
    buffer = []
    # Fill the buffer with up to buffer_size items initially
    try:
        for _ in range(buffer_size):
            item = next(it)
            buffer.append(item)
    except StopIteration:
        pass

    while True:
        # Select a random item from the buffer
        index = random.randint(0, len(buffer) - 1)
        item = buffer[index]

        # Try to replace the selected item with a new one from the iterator
        try:
            next_item = next(it)
            buffer[index] = next_item
            # Yield the item AFTER replacing it in the buffer
            # this way the buffer is always contiguous so we can
            # simply yield the buffer at the end
            yield item
        except StopIteration:
            yield from buffer
            break


R = TypeVar("R")


def diversity_aware_shuffle(
    it: Iterator[T],
    key: Callable[[T], R],
    *,
    diversity_goal: int = 4,
    buffer_size: int = 1024,
) -> Iterator[T]:
    """A shuffle iterator that is aware of the diversity of the data
    being shuffled. The key function should return a value that is
    is used to determine the diversity of the data. The diversity_goal
    is the number of unique values that should be in the buffer at any
    given time. if the buffer is full, the items is yielded in a round-robin
    fashion. This is useful for shuffling tasks that are diverse, but

    This algorithm is bounded in memory by the buffer_size, so it is reasonably
    efficient for large datasets.
    """

    # NOTE: this is similar to itertools.groupby, but with a buffering limit

    buffer: dict[R, list[T]] = {}
    buffer_total_size = 0

    peekable_it = more_itertools.peekable(it)

    def _maybe_consume_from_iter() -> bool:
        nonlocal buffer_total_size
        item = peekable_it.peek(default=None)
        if item is None:
            return False
        key_val = key(item)
        if key_val not in buffer and len(buffer) < diversity_goal:
            buffer[key_val] = []
        else:
            return False

        # if the buffer still has room, add the item
        if buffer_total_size < buffer_size:
            buffer[key_val].append(item)
            buffer_total_size += 1
        else:
            return False

        next(peekable_it)
        return True

    while _maybe_consume_from_iter():
        ...

    production_counter = 0

    def _next_key() -> T | None:
        nonlocal buffer_total_size, production_counter
        if not buffer_total_size:
            return None

        # TODO: add warning about buffer size not big enough for diversity_goal
        buffer_slot = production_counter % len(buffer)
        key_val = next(itertools.islice(buffer.keys(), buffer_slot, buffer_slot + 1))
        assert key_val in buffer
        key_buffer = buffer[key_val]

        buffer_total_size -= 1
        item = key_buffer.pop(0)
        if not key_buffer:
            del buffer[key_val]

        # try to fill the removed buffer slot
        _maybe_consume_from_iter()
        production_counter += 1
        return item

    while (item := _next_key()) is not None:
        yield item


def _any_checkpoint_has_srcfiles_mismatch(
    column: str,
    checkpoint_store: CheckpointStore,
    dataset,
    input_field_ids: frozenset[int],
) -> bool:
    """Check if any checkpoint for this column has different srcfiles hash.

    When a UDF's input column is updated (e.g., column b is re-backfilled with
    a new UDF), the data files for that input column change. The checkpoint keys
    include a srcfiles hash of the input data files. If this hash differs from
    the current input files, we need to recompute the output column.

    This is needed for scenarios like:
    - Column c depends on column b
    - Column b is updated via alter_columns + backfill
    - When backfilling c again, we need to detect that b's data changed
    - Without this check, the WHERE filter would skip already-computed c values

    Args:
        column: The output column being backfilled
        checkpoint_store: Store containing checkpoint keys
        dataset: The Lance dataset to read fragments from
        input_field_ids: Field IDs of input columns to hash

    Returns True if srcfiles hash has changed (should recompute all rows).
    Returns False if all checkpoints match or none exist.
    """
    from geneva.checkpoint_utils import hash_source_files
    from geneva.runners.ray.pipeline import get_source_data_files

    # Pattern to match checkpoint keys for this column and extract srcfiles hash
    # Key format: udf-{name}_ver-{ver}_col-{column}_..._srcfiles-{hash}_frag-{id}
    col_pattern = re.compile(rf"_col-{re.escape(column)}_")
    srcfiles_pattern = re.compile(r"_srcfiles-([a-f0-9]+)_")
    # Skip per-batch checkpoints (have _range- suffix)
    range_pattern = re.compile(r"_range-\d+-\d+$")

    # Collect srcfiles hashes from existing checkpoints
    existing_hashes: set[str] = set()
    for key in checkpoint_store.list_keys(prefix="udf-"):
        if not col_pattern.search(key):
            continue
        if range_pattern.search(key):
            continue

        match = srcfiles_pattern.search(key)
        if match:
            existing_hashes.add(match.group(1))

    if not existing_hashes:
        _LOG.debug("No existing checkpoints with srcfiles hash for column=%s", column)
        return False

    # Compute current srcfiles hash for the first fragment
    fragments = list(dataset.get_fragments())
    if not fragments:
        return False

    frag = fragments[0]
    current_src_files = get_source_data_files(frag, input_field_ids)
    current_hash = hash_source_files(current_src_files)

    # Check if current hash matches any existing hash
    if current_hash not in existing_hashes:
        _LOG.debug(
            "Srcfiles hash mismatch for column=%s: current=%s, existing=%s",
            column,
            current_hash,
            existing_hashes,
        )
        return True

    return False


def _any_checkpoint_has_udf_mismatch(
    udf_name: str,
    column: str,
    checkpoint_store: CheckpointStore,
    current_udf_version: str,
) -> bool:
    """Check if any fragment checkpoint for this column has different UDF version.

    Uses regex search to find fragment-level checkpoints across all versions and
    fragment IDs. This correctly handles compaction (fragment ID changes) and UDF
    updates, including when the UDF name changes via alter_columns.

    Only checks per-fragment checkpoints (which contain udf_version), not per-batch
    checkpoints (which store UDF output data without udf_version metadata).

    Key formats:
    - Per-fragment: udf-{name}_ver-{ver}_col-{col}_..._frag-{id} (has udf_version)
    - Per-batch: ..._frag-{id}_range-{s}-{e} (no udf_version)

    Returns True if UDF version has changed (should recompute all rows).
    Returns False if all checkpoints match current version or none exist.
    """
    # Pattern to match fragment-level checkpoint keys for this column.
    # We search by column rather than UDF name because alter_columns can change
    # the UDF name (e.g., from b_from_a_v1 to b_from_a_v2)
    col_pattern = re.compile(rf"_col-{re.escape(column)}_")
    # Pattern to identify per-batch checkpoints (have _range- suffix)
    range_pattern = re.compile(r"_range-\d+-\d+$")

    found_any = False
    # List ALL checkpoint keys and filter by column pattern
    for key in checkpoint_store.list_keys(prefix="udf-"):
        if not col_pattern.search(key):
            continue

        # Skip per-batch checkpoints (they don't have udf_version)
        if range_pattern.search(key):
            continue

        found_any = True
        # Found a fragment checkpoint for this column - check its UDF version
        try:
            checkpointed_data = checkpoint_store[key]
            if "udf_version" not in checkpointed_data.schema.names:
                # Legacy checkpoint without udf_version - assume mismatch to be safe
                _LOG.debug(
                    "Checkpoint %s has no udf_version field, assuming mismatch", key
                )
                return True

            stored_version = checkpointed_data["udf_version"][0].as_py()
            if stored_version != current_udf_version:
                _LOG.debug(
                    "Checkpoint %s has different UDF version: %s vs current %s",
                    key,
                    stored_version,
                    current_udf_version,
                )
                return True  # Found checkpoint with different UDF version
        except Exception as e:
            _LOG.debug("Error reading checkpoint %s: %s", key, e)
            # On error, assume mismatch to be safe
            return True

    if not found_any:
        _LOG.debug(
            "No existing fragment checkpoints for udf=%s, column=%s", udf_name, column
        )

    return False  # All checkpoints match (or none exist)
