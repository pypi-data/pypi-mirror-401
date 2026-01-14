# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Basic execution tests for direct Ray connect mode.

These tests validate that Geneva's core functionality works correctly
when connecting to a pre-existing Ray cluster via direct network access.
"""

import logging
import uuid

import pyarrow as pa
import pytest

import geneva

_LOG = logging.getLogger(__name__)


# Use a random version to force checkpoint to invalidate
@geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
def plus_one(a: int) -> int:
    return a + 1


SIZE = 1024


@pytest.mark.timeout(900)
def test_direct_connect_add_column_pipeline(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test basic add_column pipeline using direct Ray connection."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},
            batch_size=32,
            concurrency=2,
            intra_applier_concurrency=2,
        )
        table.backfill("b")

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        conn.drop_table(table_name)


def test_direct_connect_cpu_only_pool(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test CPU-only resource pool with direct connect."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},
            batch_size=32,
            concurrency=4,
            use_cpu_only_pool=True,
        )
        table.backfill("b")

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        conn.drop_table(table_name)


@pytest.mark.timeout(900)
def test_direct_connect_multiple_fragments(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test backfill across multiple fragments with direct connect."""
    adds = 10
    rows_per_add = 10
    db = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
    table = db.create_table(table_name, data)

    try:
        for _ in range(adds):
            # Split adds to create many fragments
            data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
            table.add(data)

        table.add_columns({"b": plus_one})
        table.backfill("b", concurrency=2)

        # Verify job tracking still works
        jobs = db._history.list_jobs(table_name, None)
        _LOG.info(f"{jobs=}")
        assert len(jobs) == 1, "expected a job record"
        assert jobs[0].status == "DONE"
        assert jobs[0].table_name == table_name
        assert jobs[0].job_type == "BACKFILL"
    finally:
        db.drop_table(table_name)
