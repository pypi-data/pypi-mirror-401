# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections.abc import Iterator

import pyarrow as pa

import geneva.apply as apply_mod
from geneva.apply import CheckpointingApplier
from geneva.apply.adaptive import (
    AdaptiveCheckpointSizer,
    AdaptiveReadTask,
    BatchSizeTracker,
)
from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, BackfillUDFTask, ReadTask
from geneva.transformer import BACKFILL_SELECTED, udf


class _DummyReadTask(ReadTask):
    def __init__(self, batches: list[pa.RecordBatch]) -> None:
        self._batches = batches

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch]:
        yield from self._batches

    def checkpoint_key(self) -> str:
        return "dummy"

    def dest_frag_id(self) -> int:
        return 0

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return sum(batch.num_rows for batch in self._batches)

    def table_uri(self) -> str:
        return "memory://dummy"


@udf(data_type=pa.int32(), min_checkpoint_size=2, max_checkpoint_size=3)
def _double(a: int) -> int:
    return a * 2


def test_adaptive_checkpoint_sizer_clamps_size() -> None:
    sizer = AdaptiveCheckpointSizer(max_size=100, min_size=1, target_seconds=10.0)
    assert sizer.current_size == 1

    sizer.record(duration_seconds=20.0, rows=100)
    assert sizer.current_size == 50

    sizer.record(duration_seconds=1.0, rows=100)
    assert sizer.current_size == 100

    sizer.record(duration_seconds=1000.0, rows=1)
    assert sizer.current_size == 1


def test_adaptive_read_task_slices_and_tracks_sizes() -> None:
    batch = pa.record_batch(
        [pa.array(list(range(10))), pa.array(list(range(10)), type=pa.uint64())],
        names=["a", "_rowaddr"],
    )
    task = _DummyReadTask([batch])
    sizer = AdaptiveCheckpointSizer(max_size=4, min_size=1, target_seconds=10.0)
    tracker = BatchSizeTracker()
    adaptive = AdaptiveReadTask(task, sizer=sizer, size_tracker=tracker)

    it = adaptive.to_batches(batch_size=4)
    first = next(it)
    assert first.num_rows == 1
    sizer.record(duration_seconds=1.0, rows=1)

    second = next(it)
    assert second.num_rows == 4
    sizer.record(duration_seconds=20.0, rows=4)

    third = next(it)
    assert third.num_rows == 2
    sizer.record(duration_seconds=1.0, rows=2)

    fourth = next(it)
    assert fourth.num_rows == 3

    sizes = [tracker.pop() for _ in range(4)]
    assert sizes == [1, 4, 2, 3]


def test_checkpointing_applier_adapts_batch_sizes(monkeypatch) -> None:
    map_task = BackfillUDFTask(
        udfs={"b": _double},
        override_batch_size=4,
        explicit_checkpoint_size=True,
    )

    batch = pa.record_batch(
        [
            pa.array(list(range(8))),
            pa.array([True] * 8),
            pa.array(list(range(8)), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )
    read_task = _DummyReadTask([batch])

    times = iter([0.0, 1.0, 1.0, 21.0, 21.0, 31.0, 31.0, 41.0, 41.0])
    monkeypatch.setattr(apply_mod.time, "monotonic", lambda: next(times))

    applier = CheckpointingApplier(checkpoint_uri="memory", map_task=map_task)
    checkpoints, _ = applier.run(read_task)

    assert [checkpoint.span for checkpoint in checkpoints] == [3, 3, 2]
    assert [
        applier.checkpoint_store[checkpoint.checkpoint_key].num_rows
        for checkpoint in checkpoints
    ] == [3, 3, 2]


def test_backfill_task_overrides_adaptive_bounds() -> None:
    task = BackfillUDFTask(
        udfs={"b": _double},
        override_batch_size=4,
        min_checkpoint_size=1,
        max_checkpoint_size=4,
    )
    assert task.adaptive_checkpoint_bounds() == (1, 4)


def test_udf_default_min_checkpoint_size() -> None:
    @udf(data_type=pa.int32())
    def _identity(a: int) -> int:
        return a

    task = BackfillUDFTask(udfs={"b": _identity}, override_batch_size=4)
    min_size, _ = task.adaptive_checkpoint_bounds()
    assert min_size == 1
