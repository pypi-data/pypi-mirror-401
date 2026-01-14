# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import time
from collections.abc import Iterator, Mapping
from typing import Any, TypeVar

import attrs
import lance
import pyarrow as pa
from .utils import (
    _buffered_shuffle,
    _check_fragment_data_file_exists,
    _compute_missing_ranges,
    _count_udf_rows,
    _iter_checkpoint_ranges_for_fragment,
    _legacy_fragment_dedupe_key,
    _merge_ranges,
    _num_tasks,
    _parse_checkpoint_ranges_for_fragment,
    diversity_aware_shuffle,
)

from geneva.apply.adaptive import (
    AdaptiveCheckpointSizer,
    AdaptiveReadTask,
    BatchSizeTracker,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.simple import SimpleApplier
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    CopyTask,
    MapTask,
    ReadTask,
    ScanTask,
)
from geneva.checkpoint import CheckpointStore
from geneva.checkpoint_utils import hash_source_files
from geneva.debug.logger import ErrorLogger, NoOpErrorLogger
from geneva.table import TableReference

_LOG = logging.getLogger(__name__)


@attrs.define(frozen=True)
class MapBatchCheckpoint:
    """Metadata for a single checkpointed map-task batch.

    Notes:
        `offset` and `span` define the coverage window in the planner's
        fragment-local offset domain: `[offset, offset + span)`.

        `span` is the amount of progress this checkpoint represents in the
        planner's *logical* offset domain (the same domain used by `ScanTask`
        offset/limit and by writer ordering). It corresponds to the `_range-`
        suffix in `checkpoint_key` and may be larger than the batch's physical
        row count when `_rowaddr` is sparse (e.g., `where` filters or deletes).

        `num_rows` is the physical number of materialized rows stored in the
        checkpointed `RecordBatch` (`batch.num_rows`). This is useful for
        introspection/metrics/debugging, but must not be used as "coverage" when
        `_rowaddr` has gaps.
    """

    checkpoint_key: str
    offset: int
    num_rows: int  # Physical rows in the stored RecordBatch (may be < span).
    span: int  # Logical coverage/progress in the planner offset domain.
    udf_rows: int


@attrs.define(frozen=True)
class _PlanReadResult:
    tasks: Iterator[ReadTask]
    skipped_fragments: dict[int, lance.fragment.DataFile]
    skipped_stats: dict[str, int]
    src_data_files_by_dst: dict[int, frozenset[str]]


class _CountingReadTask(ReadTask):
    """Proxy ReadTask that counts rows selected for UDF execution."""

    def __init__(self, inner: ReadTask) -> None:
        self._inner = inner
        self.cnt_udf_computed: int = 0
        self.udf_rows_history: list[int] = []

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch | list[dict]]:
        for batch in self._inner.to_batches(batch_size=batch_size):
            count = _count_udf_rows(batch)
            self.cnt_udf_computed += count
            self.udf_rows_history.append(count)
            yield batch

    def checkpoint_key(self) -> str:
        return self._inner.checkpoint_key()

    def dest_frag_id(self) -> int:
        return self._inner.dest_frag_id()

    def dest_offset(self) -> int:
        return self._inner.dest_offset()

    def num_rows(self) -> int:
        return self._inner.num_rows()

    def table_uri(self) -> str:
        return self._inner.table_uri()

    def __getattr__(self, item: str) -> Any:
        return getattr(self._inner, item)


@attrs.define
class CheckpointingApplier:
    """
    Reads a read task and applies a map task to the data
    using a batch applier.

    The applier will checkpoint the output of the map task so that it can be
    resumed from the same point if the job is interrupted.
    """

    checkpoint_uri: str = attrs.field()
    map_task: MapTask = attrs.field()

    error_logger: ErrorLogger = attrs.field(default=NoOpErrorLogger())
    batch_applier: BatchApplier = attrs.field(
        factory=SimpleApplier,
        converter=attrs.converters.default_if_none(factory=SimpleApplier),
    )

    checkpoint_store: CheckpointStore = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.checkpoint_store = CheckpointStore.from_uri(self.checkpoint_uri)

    @property
    def output_schema(self) -> pa.Schema:
        return self.map_task.output_schema()

    def _checkpoint_key_for_task(self, task: ReadTask) -> str:
        start = task.dest_offset()
        end = start + task.num_rows()

        try:
            dataset_uri = task.table_uri()
        except Exception:
            dataset_uri = "unknown"

        dataset_version = getattr(task, "version", None)
        where = getattr(task, "where", None)
        src_files_hash = getattr(task, "src_files_hash", None)

        return self.map_task.checkpoint_key(
            dataset_uri=dataset_uri or "",
            dataset_version=dataset_version,
            frag_id=task.dest_frag_id(),
            start=start,
            end=end,
            where=where,
            src_files_hash=src_files_hash,
        )

    def _checkpoint_single_batch(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        dataset_uri: str,
        dataset_version: int | str | None,
        where: str | None,
        udf_rows: int | None,
        start: int,
        checkpoint_size: int,
        src_files_hash: str | None = None,
    ) -> MapBatchCheckpoint:
        task_end = task.dest_offset() + task.num_rows()

        # Determine the farthest row actually present in this batch
        if "_rowaddr" in batch.schema.names and batch.num_rows > 0:
            rowaddrs = batch["_rowaddr"]
            last_row_offset = int(rowaddrs[-1].as_py() & 0xFFFFFFFF)
        else:
            last_row_offset = start - 1

        end = max(start + checkpoint_size, last_row_offset + 1)
        end = min(task_end, end)
        if end < start:
            end = start

        checkpoint_key = self.map_task.checkpoint_key(
            dataset_uri=dataset_uri or "",
            dataset_version=dataset_version,
            frag_id=task.dest_frag_id(),
            start=start,
            end=end,
            where=where,
            src_files_hash=src_files_hash,
        )

        self.checkpoint_store[checkpoint_key] = batch
        udf_rows_val = int(udf_rows) if udf_rows is not None else _count_udf_rows(batch)

        return MapBatchCheckpoint(
            checkpoint_key=checkpoint_key,
            offset=start,
            num_rows=int(batch.num_rows),
            span=int(end - start),
            udf_rows=int(udf_rows_val),
        )

    def _load_checkpointed_results(
        self, task: ReadTask
    ) -> tuple[list[MapBatchCheckpoint], int] | None:
        task_key = self._checkpoint_key_for_task(task)

        if task_key in self.checkpoint_store:
            cached = self.checkpoint_store[task_key]
            try:
                schema_names = cached.schema.names
            except Exception:
                schema_names = []

            if "checkpoint_key" in schema_names:
                ck = cached.column("checkpoint_key")
                offsets = cached.column("offset")
                num_rows = cached.column("num_rows")
                spans = cached.column("span")
                udf_rows = cached.column("udf_rows")

                results = [
                    MapBatchCheckpoint(
                        checkpoint_key=str(ck[idx].as_py()),
                        offset=int(offsets[idx].as_py()),
                        num_rows=int(num_rows[idx].as_py()),
                        span=int(spans[idx].as_py()),
                        udf_rows=int(udf_rows[idx].as_py()),
                    )
                    for idx in range(cached.num_rows)
                ]

                total_udf = sum(r.udf_rows for r in results)
                _LOG.info("Using cached result for %s", task_key)
                return results, total_udf

            # Legacy single-batch checkpoint stored directly under task key
            _LOG.info("Using legacy cached result for %s", task_key)
            dataset_uri = getattr(task, "table_uri", lambda: "unknown")()
            dataset_version = getattr(task, "version", None)
            where = getattr(task, "where", None)

            result = self._checkpoint_single_batch(
                task,
                cached,
                dataset_uri=dataset_uri,
                dataset_version=dataset_version,
                where=where,
                udf_rows=None,
                start=task.dest_offset(),
                checkpoint_size=self.map_task.batch_size() or DEFAULT_CHECKPOINT_ROWS,
                src_files_hash=getattr(task, "src_files_hash", None),
            )
            return [result], result.udf_rows

        # Reconstruct from per-batch checkpoints if the task range is fully covered
        src_files_hash = getattr(task, "src_files_hash", None)
        prefixes = [
            self.map_task.checkpoint_prefix(
                dataset_uri=task.table_uri(),
                where=getattr(task, "where", None),
                column=None,
                src_files_hash=src_files_hash,
            )
        ]

        ranges = _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=self.checkpoint_store,
            prefixes=prefixes,
            frag_id=task.dest_frag_id(),
        )

        if not ranges:
            return None

        task_start = task.dest_offset()
        task_end = task_start + task.num_rows()

        # Select ranges overlapping the task window
        ranges = [
            (k, max(s, task_start), min(e, task_end))
            for k, s, e in ranges
            if e > task_start and s < task_end
        ]
        ranges.sort(key=lambda r: r[1])

        cur = task_start
        results: list[MapBatchCheckpoint] = []
        for key, s, e in ranges:
            if s > cur:
                return None  # gap
            span = e - cur
            if span <= 0:
                continue
            batch = self.checkpoint_store[key]
            results.append(
                MapBatchCheckpoint(
                    checkpoint_key=key,
                    offset=cur,
                    num_rows=int(batch.num_rows),
                    span=span,
                    udf_rows=_count_udf_rows(batch),
                )
            )
            cur = max(cur, e)
            if cur >= task_end:
                break

        if cur < task_end:
            return None

        total_udf = sum(r.udf_rows for r in results)
        return results, total_udf

    def _run(self, task: ReadTask) -> tuple[list[MapBatchCheckpoint], int]:
        _LOG.info("Running task %s", task)

        if cached := self._load_checkpointed_results(task):
            return cached

        try:
            dataset_uri = task.table_uri()
        except Exception:
            dataset_uri = "unknown"

        dataset_version = getattr(task, "version", None)
        where = getattr(task, "where", None)

        results: list[MapBatchCheckpoint] = []
        checkpoint_size = self.map_task.batch_size() or DEFAULT_CHECKPOINT_ROWS
        size_tracker = BatchSizeTracker()
        min_override, max_override = self.map_task.adaptive_checkpoint_bounds()
        max_explicit = max_override is not None
        min_size = 1 if min_override is None else int(min_override)
        max_size = checkpoint_size if max_override is None else int(max_override)
        initial_size = self.map_task.initial_checkpoint_size()

        if max_size <= 0:
            max_size = checkpoint_size
        if not max_explicit and checkpoint_size > 0 and max_size > checkpoint_size:
            max_size = checkpoint_size
        if min_size <= 0:
            min_size = 1
        if min_size > max_size:
            min_size = max_size

        sizer = AdaptiveCheckpointSizer(
            max_size=max_size,
            min_size=min_size,
            initial_size=initial_size,
            target_seconds=10.0,
        )
        adaptive_task: ReadTask = AdaptiveReadTask(
            task,
            sizer=sizer,
            size_tracker=size_tracker,
        )
        proxy_task = _CountingReadTask(adaptive_task)
        batches = self.batch_applier.run(
            proxy_task,
            self.map_task,
            error_logger=self.error_logger,
        )

        next_start = task.dest_offset()

        had_any_batch = False
        idx = 0
        batch_iter = iter(batches)
        while True:
            batch_start = time.monotonic()
            try:
                batch = next(batch_iter)
            except StopIteration:
                break
            had_any_batch = True
            udf_rows = (
                proxy_task.udf_rows_history[idx]
                if idx < len(proxy_task.udf_rows_history)
                else None
            )
            batch_checkpoint_size = size_tracker.pop() or checkpoint_size

            result = self._checkpoint_single_batch(
                task,
                batch,
                dataset_uri=dataset_uri,
                dataset_version=dataset_version,
                where=where,
                udf_rows=udf_rows,
                start=next_start,
                checkpoint_size=batch_checkpoint_size,
                src_files_hash=getattr(task, "src_files_hash", None),
            )

            next_start = result.offset + result.span
            results.append(result)
            idx += 1
            elapsed = time.monotonic() - batch_start
            sizer.record(duration_seconds=elapsed, rows=batch.num_rows)

        # If the read task yields no batches (e.g., `where` filters everything
        # out), we still need to persist completion checkpoints. Otherwise the
        # task is not idempotent: status()/_load_cached_results() would always
        # treat it as unfinished and retries would reschedule the same empty
        # work. We also need to enqueue *logical rows* for the writer, since the
        # writer waits for batches whose total num_rows matches the fragment's
        # logical row count. To satisfy both, we synthesize null-filled batches
        # in checkpoint_size chunks that cover the entire task window.
        if not had_any_batch:
            task_start = task.dest_offset()
            task_end = task_start + task.num_rows()
            frag_id = task.dest_frag_id()

            if task_end > task_start:
                schema = self.map_task.output_schema()
                # Partition the task window into checkpoint-sized subranges so the
                # number of synthetic checkpoints matches planning estimates.
                start = task_start
                while start < task_end:
                    end = min(start + checkpoint_size, task_end)
                    span = int(end - start)

                    arrays: list[pa.Array] = []
                    has_rowaddr = "_rowaddr" in schema.names
                    # Precompute rowaddr if needed.
                    if has_rowaddr:
                        row_addrs = pa.array(
                            [(frag_id << 32) | i for i in range(start, end)],
                            type=pa.uint64(),
                        )
                    for field in schema:
                        if field.name == "_rowaddr" and has_rowaddr:
                            arrays.append(row_addrs)
                        else:
                            arrays.append(pa.nulls(span, type=field.type))

                    filler_batch = pa.record_batch(arrays, schema=schema)
                    completion_key = self.map_task.checkpoint_key(
                        dataset_uri=dataset_uri or "",
                        dataset_version=dataset_version,
                        frag_id=frag_id,
                        start=start,
                        end=end,
                        where=where,
                        src_files_hash=getattr(task, "src_files_hash", None),
                    )
                    self.checkpoint_store[completion_key] = filler_batch
                    results.append(
                        MapBatchCheckpoint(
                            checkpoint_key=completion_key,
                            offset=int(start),
                            num_rows=span,
                            span=span,
                            udf_rows=0,
                        )
                    )
                    start = end

        total_udf_computed = proxy_task.cnt_udf_computed
        return results, total_udf_computed

    def run(self, task: ReadTask) -> tuple[list[MapBatchCheckpoint], int]:
        try:
            return self._run(task)
        except Exception as e:
            logging.exception("Error running task %s: %s", task, e)
            raise RuntimeError(f"Error running task {task}") from e

    def status(self, task: ReadTask) -> bool:
        # Reuse cached results reconstruction path for completion check
        return self._load_checkpointed_results(task) is not None


def _plan_read(
    uri: str,
    table_ref: TableReference,
    columns: list[str],
    *,
    read_version: int | None = None,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    where: str | None = None,
    num_frags: int | None = None,
    map_task: MapTask | None = None,
    checkpoint_store: CheckpointStore | None = None,
) -> _PlanReadResult:
    """Make Plan for Reading Data from a Dataset
    We want a ScanTask for each fragment in the dataset even if they are filtered
    out. This should make the checkpointing recovery easier to manage.

    Returns a tuple of (ReadTask iterator, skipped_fragments dict, skipped_stats dict,
    src_data_files_by_dst). skipped_stats contains {'fragments': count, 'rows': count}
    for progress tracking.
    """
    # Open dataset with namespace if available
    if namespace := table_ref.connect_namespace():
        dataset = lance.dataset(namespace=namespace, table_id=table_ref.table_id)
    else:
        dataset = lance.dataset(uri)

    if read_version is not None:
        dataset = dataset.checkout_version(read_version)

    skipped_fragments = {}
    skipped_stats = {"fragments": 0, "rows": 0}
    tasks = []
    src_data_files_by_dst: dict[int, frozenset[str]] = {}

    relevant_field_ids = None
    if map_task is not None:
        input_cols = map_task.input_columns()
        if input_cols is not None:
            from geneva.runners.ray.pipeline import _get_relevant_field_ids

            relevant_field_ids = _get_relevant_field_ids(dataset, input_cols)
    # Track output-column field IDs so we can validate fragment-level checkpoints
    # against the *current* output data files. This is important for cases like
    # test_rebackfill: when a column is dropped and re-added, the output column's
    # data files change even though the input-column src_files_hash can remain the
    # same. Without checking output files, we might wrongly reuse a checkpoint and
    # skip recomputation.
    output_field_ids: frozenset[int] | None = None
    if map_task is not None:
        try:
            from geneva.utils.parse_rust_debug import extract_field_ids

            output_field_id_set: set[int] = set()
            for field in map_task.output_schema():
                if field.name == "_rowaddr":
                    continue
                try:
                    output_field_id_set.update(
                        extract_field_ids(dataset.lance_schema, field.name)
                    )
                except Exception:  # noqa: PERF203
                    _LOG.debug(
                        "Output column %s not found in schema, skipping", field.name
                    )
            if output_field_id_set:
                output_field_ids = frozenset(output_field_id_set)
        except Exception:  # noqa: PERF203
            output_field_ids = None

    # get_fragments has an unsupported filter method, so we do filtering deeper in.
    for idx, frag in enumerate(dataset.get_fragments()):
        _LOG.info(
            f"Processing fragment {idx} (fragment_id={frag.fragment_id}), "
            f"num_frags={num_frags}"
        )
        if num_frags is not None and idx >= num_frags:
            _LOG.info(f"Breaking loop: idx {idx} >= num_frags {num_frags}")
            break

        src_files_hash = None
        if map_task is not None:
            from geneva.runners.ray.pipeline import get_source_data_files

            src_files = get_source_data_files(frag, relevant_field_ids)
            src_data_files_by_dst[frag.fragment_id] = src_files
            src_files_hash = hash_source_files(src_files)

        # Check if fragment data file already exists (fragment-level checkpoint)
        checkpoint_exists = (
            map_task is not None
            and checkpoint_store is not None
            and _check_fragment_data_file_exists(
                uri,
                frag.fragment_id,
                map_task,
                checkpoint_store,
                dataset_version=dataset.version,
                src_files_hash=src_files_hash,
                current_output_field_ids=output_field_ids,
                namespace=namespace,
                table_id=table_ref.table_id,
            )
        )
        dedupe_present = False
        if map_task is not None and checkpoint_store is not None:
            from geneva.runners.ray.pipeline import _get_fragment_dedupe_key

            dedupe_key = _get_fragment_dedupe_key(
                uri,
                frag.fragment_id,
                map_task,
                dataset_version=dataset.version,
                src_files_hash=src_files_hash,
            )
            if dedupe_key in checkpoint_store:
                dedupe_present = True
            else:
                legacy_key = _legacy_fragment_dedupe_key(
                    uri, frag.fragment_id, map_task
                )
                dedupe_present = legacy_key in checkpoint_store
        _LOG.info(
            f"Fragment {idx} (fragment_id={frag.fragment_id}): "
            f"checkpoint_exists={checkpoint_exists}"
        )

        if checkpoint_exists:
            _LOG.info(
                f"Skipping fragment {frag.fragment_id} - data file already exists"
            )

            # Count rows in skipped fragment for progress tracking
            frag_rows = frag.count_rows()
            filtered_frag_rows = frag.count_rows(filter=where)
            skipped_rows = filtered_frag_rows if where else frag_rows

            skipped_stats["fragments"] += 1
            skipped_stats["rows"] += skipped_rows

            # Collect skipped fragment information for commit inclusion
            from geneva.runners.ray.pipeline import _get_fragment_dedupe_key
            from geneva.utils.parse_rust_debug import extract_field_ids

            # These should not be None here due to the checkpoint_exists check above
            assert map_task is not None
            assert checkpoint_store is not None

            dedupe_key = _get_fragment_dedupe_key(
                uri,
                frag.fragment_id,
                map_task,
                dataset_version=dataset.version,
                src_files_hash=src_files_hash,
            )
            if dedupe_key not in checkpoint_store:
                legacy_key = _legacy_fragment_dedupe_key(
                    uri, frag.fragment_id, map_task
                )
                if legacy_key in checkpoint_store:
                    dedupe_key = legacy_key
            checkpointed_data = checkpoint_store[dedupe_key]
            file_list = checkpointed_data["file"].to_pylist()
            file_path = "".join(str(f) for f in file_list if f is not None)

            # The checkpointed files should only contain the columns being transformed
            # For UDF tasks, determine the field_ids for the output columns
            # Use the same logic as the writer to ensure consistency
            field_ids = []
            if hasattr(map_task, "udfs") and map_task.udfs:  # type: ignore[attr-defined]
                # Use extract_field_ids for consistency with writer.py
                # Pre-check schema to avoid try-except in loop (PERF203)
                schema_fields = {
                    field.name() for field in dataset.lance_schema.fields()
                }

                for column_name in map_task.udfs:  # type: ignore[attr-defined]
                    if column_name not in schema_fields:
                        # Column doesn't exist in current schema, this shouldn't happen
                        # for checkpointed fragments, but if it does, skip this fragment
                        _LOG.warning(
                            f"Column {column_name} not found in schema for "
                            f"checkpointed fragment {frag.fragment_id}, skipping"
                        )
                        continue

                    field_ids.extend(
                        extract_field_ids(dataset.lance_schema, column_name)
                    )
            else:
                # Fallback: use all columns (this shouldn't happen for UDF tasks)
                for column_name in columns:
                    field_ids.extend(
                        extract_field_ids(dataset.lance_schema, column_name)
                    )

            # Create a DataFile object for this existing file
            existing_data_file = lance.fragment.DataFile(
                file_path,
                field_ids,
                list(range(len(field_ids))),
                2,  # major_version
                0,  # minor_version
            )
            skipped_fragments[frag.fragment_id] = existing_data_file
            continue

        frag_rows = frag.count_rows()
        filtered_frag_rows = frag.count_rows(filter=where)
        if filtered_frag_rows == 0:
            _LOG.debug(
                f"frag {frag.fragment_id} filtered by '{where}' has no rows, skipping."
            )
            continue

        _LOG.debug(
            f"plan_read fragment: {frag} has {frag_rows} rows, filtered to"
            f" {filtered_frag_rows} rows"
        )

        # the ranges that we need to backfill, the tuple is (offset, num_rows),
        # which means we need to backfill the range [offset, offset + num_rows)
        gaps: list[tuple[int, int]]
        if map_task is None or checkpoint_store is None:
            gaps = [
                (offset, min(task_size, frag_rows - offset))
                for offset in range(
                    0, frag_rows, task_size if task_size > 0 else frag_rows
                )
            ]
        else:
            prefixes = [
                map_task.checkpoint_prefix(
                    dataset_uri=uri,
                    where=where,
                    column=None,
                    src_files_hash=src_files_hash,
                ),
            ]
            covered = _merge_ranges(
                _parse_checkpoint_ranges_for_fragment(
                    checkpoint_store=checkpoint_store,
                    prefixes=prefixes,
                    frag_id=frag.fragment_id,
                )
            )
            if not checkpoint_exists and dedupe_present:
                if covered:
                    _LOG.info(
                        "Ignoring %d checkpoint ranges for fragment %s because "
                        "no data file exists for this fragment",
                        len(covered),
                        frag.fragment_id,
                    )
                covered = []

            # All rows in fragment already covered
            if (
                covered
                and covered[0][0] <= 0
                and covered[-1][1] >= frag_rows
                and len(covered) == 1
            ):
                _LOG.info(
                    "Skipping fragment %s entirely (all rows checkpointed)",
                    frag.fragment_id,
                )
                skipped_stats["rows"] += frag_rows
                skipped_stats["fragments"] += 1
                continue

            gaps = _compute_missing_ranges(
                total_rows=frag_rows,
                task_size=task_size,
                covered=covered,
            )

        for offset, span in gaps:
            limit = span
            _LOG.debug(
                f"scan task: idx={idx} fragid={frag.fragment_id} offset={offset} "
                f"limit={limit} where={where}"
            )

            tasks.append(
                ScanTask(
                    uri=uri,
                    table_ref=table_ref,
                    version=read_version
                    if read_version is not None
                    else dataset.version,
                    columns=columns,
                    frag_id=frag.fragment_id,
                    offset=offset,
                    limit=limit,
                    where=where,
                    with_row_address=True,
                    src_files_hash=src_files_hash,
                )
            )

    return _PlanReadResult(
        tasks=iter(tasks),
        skipped_fragments=skipped_fragments,
        skipped_stats=skipped_stats,
        src_data_files_by_dst=src_data_files_by_dst,
    )


T = TypeVar("T")  # Define type variable "T"


@attrs.define
class _LanceReadPlanIterator(Iterator[T]):
    it: Iterator[T]
    total: int

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return next(self.it)

    def __len__(self) -> int:
        return self.total


def plan_read(
    uri: str,
    table_ref: TableReference,
    columns: list[str],
    *,
    read_version: int | None = None,
    task_size: int | None = None,
    batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    where: str | None = None,
    shuffle_buffer_size: int = 0,
    task_shuffle_diversity: int | None = None,
    num_frags: int | None = None,
    map_task: MapTask | None = None,
    checkpoint_store: CheckpointStore | None = None,
    **unused_kwargs,
) -> tuple[Iterator[ReadTask], Mapping]:
    """
    Make Plan for Reading Data from a Dataset

    Parameters
    ----------
    num_frags:
        max number of fragments to scan for sampling use cases.
    """
    # `batch_size` historically controlled read-task sizing in these planners.
    # Keep it as a backwards-compatible alias for `task_size`.
    if (
        task_size is not None
        and batch_size != DEFAULT_CHECKPOINT_ROWS
        and batch_size != task_size
    ):
        _LOG.warning(
            "plan_read(batch_size=%s) overrides task_size=%s; "
            "use task_size going forward.",
            batch_size,
            task_size,
        )
    effective_task_size = batch_size if task_size is None else task_size

    plan_result = _plan_read(
        uri,
        table_ref,
        columns=columns,
        read_version=read_version,
        task_size=effective_task_size,
        where=where,
        num_frags=num_frags,
        map_task=map_task,
        checkpoint_store=checkpoint_store,
    )
    it = plan_result.tasks
    # same as no shuffle
    if shuffle_buffer_size > 1 and task_shuffle_diversity is None:
        it = _buffered_shuffle(it, buffer_size=shuffle_buffer_size)
    elif task_shuffle_diversity is not None:
        buffer_size = max(4 * task_shuffle_diversity, shuffle_buffer_size)
        it = diversity_aware_shuffle(
            it,
            key=lambda task: task.checkpoint_key(),
            diversity_goal=task_shuffle_diversity,
            buffer_size=buffer_size,
        )

    unused_kwargs["skipped_fragments"] = plan_result.skipped_fragments
    unused_kwargs["skipped_stats"] = plan_result.skipped_stats
    unused_kwargs["src_data_files_by_dst"] = plan_result.src_data_files_by_dst

    # Get namespace from table_ref for _num_tasks
    namespace_client = table_ref.connect_namespace()

    return _LanceReadPlanIterator(
        it,
        _num_tasks(
            uri=uri,
            read_version=read_version,
            task_size=effective_task_size,
            namespace_client=namespace_client,
            table_id=table_ref.table_id,
        ),
    ), unused_kwargs


def _plan_copy(
    src: TableReference,
    dst: TableReference,
    columns: list[str] | dict[str, str],
    *,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    only_fragment_ids: set[int] | None = None,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
) -> tuple[Iterator[CopyTask], int]:
    """Make Plan for Reading Data from a Dataset

    For materialized views, this iterates over DESTINATION fragments and creates
    CopyTasks for all of them. This destination-driven approach correctly handles
    cases where source fragments are consolidated into fewer destination fragments
    (e.g., due to filters or shuffle operations).

    Args:
        only_fragment_ids: If provided, only create tasks for the specified
            destination fragment IDs. Used for incremental refresh to process
            only specific fragments.
    """
    # Read from DESTINATION dataset (destination-driven approach for materialized views)
    dst_dataset = dst.open().to_lance()

    num_tasks = 0
    for frag in dst_dataset.get_fragments():
        # Skip fragments that don't match the filter
        if only_fragment_ids is not None and frag.fragment_id not in only_fragment_ids:
            continue
        frag_rows = frag.count_rows()
        # ceil_div
        num_tasks += -(frag_rows // -task_size)

    def task_gen() -> Iterator[CopyTask]:
        for frag in dst_dataset.get_fragments():
            # Skip fragments that don't match the filter
            if (
                only_fragment_ids is not None
                and frag.fragment_id not in only_fragment_ids
            ):
                continue
            frag_rows = frag.count_rows()
            src_files_hash = None
            if src_data_files_by_dst is not None:
                src_files = src_data_files_by_dst.get(frag.fragment_id)
                if src_files is not None:
                    src_files_hash = hash_source_files(src_files)
            for offset in range(0, frag_rows, task_size):
                limit = min(task_size, frag_rows - offset)
                yield CopyTask(
                    src=src,
                    dst=dst,
                    columns=columns,
                    frag_id=frag.fragment_id,
                    offset=offset,
                    limit=limit,
                    src_files_hash=src_files_hash,
                )

    return (task_gen(), num_tasks)


def plan_copy(
    src: TableReference,
    dst: TableReference,
    columns: list[str] | dict[str, str],
    *,
    task_size: int | None = None,
    batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    shuffle_buffer_size: int = 0,
    task_shuffle_diversity: int | None = None,
    only_fragment_ids: set[int] | None = None,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
    **unused_kwargs,
) -> Iterator[CopyTask]:
    # `batch_size` historically controlled read-task sizing in these planners.
    # Keep it as a backwards-compatible alias for `task_size`.
    if (
        task_size is not None
        and batch_size != DEFAULT_CHECKPOINT_ROWS
        and batch_size != task_size
    ):
        _LOG.warning(
            "plan_copy(batch_size=%s) overrides task_size=%s; "
            "use task_size going forward.",
            batch_size,
            task_size,
        )
    effective_task_size = batch_size if task_size is None else task_size

    (it, num_tasks) = _plan_copy(
        src,
        dst,
        columns,
        task_size=effective_task_size,
        only_fragment_ids=only_fragment_ids,
        src_data_files_by_dst=src_data_files_by_dst,
    )
    # same as no shuffle
    if shuffle_buffer_size > 1 and task_shuffle_diversity is None:
        it = _buffered_shuffle(it, buffer_size=shuffle_buffer_size)
    elif task_shuffle_diversity is not None:
        buffer_size = max(4 * task_shuffle_diversity, shuffle_buffer_size)
        it = diversity_aware_shuffle(
            it,
            key=lambda task: task.checkpoint_key(),
            diversity_goal=task_shuffle_diversity,
            buffer_size=buffer_size,
        )

    return _LanceReadPlanIterator(it, num_tasks)
