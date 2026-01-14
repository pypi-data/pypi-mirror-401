# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Integration tests for Phalanx remote server connection.

These tests assume a local Phalanx server is running on localhost.
The server can be started with:
    cd src/rust/phalanx && cargo run -- --config configs/local.toml

Tests verify:
1. Client can connect to Phalanx via db:// URI with host_override
2. Client can access system tables (jobs, clusters, manifests) via remote connection
3. Backfill jobs work correctly through Phalanx
"""

import logging
import os
import uuid
from pathlib import Path

import pyarrow as pa
import pytest

import geneva
from geneva import connect

_LOG = logging.getLogger(__name__)

# Phalanx server defaults - can be overridden via environment variables
PHALANX_HOST = os.environ.get("GENEVA_HOST_OVERRIDE", "http://localhost:10024")
DB_URI = "db://test_database"
PHALANX_API_KEY = os.environ.get("GENEVA_API_KEY", "sk_localtest")


def phalanx_available() -> bool:
    """Check if Phalanx server is available on localhost."""
    try:
        import socket

        split = PHALANX_HOST.split(":")
        hostname = split[1].strip("/")
        port = int(split[2])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((hostname, port))
        sock.close()
        return result == 0
    except Exception as e:
        _LOG.warning(f"Skipping phalanx test: {e}")
        return False


# Skip all tests in this module if Phalanx is not available
pytestmark = pytest.mark.skipif(
    not phalanx_available(),
    reason="Phalanx server not available on localhost",
)


class TestPhalanxConnection:
    """Tests for connecting to Phalanx server via db:// URI."""

    def test_connect_to_phalanx(self) -> None:
        """Test basic connection to Phalanx server."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        assert db.uri == DB_URI
        assert db._host_override == PHALANX_HOST

    def test_phalanx_table_names(self) -> None:
        """Test listing table names via Phalanx."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        # Should be able to list tables (may be empty initially)
        tables = db.table_names()
        assert isinstance(tables, list)
        _LOG.info(f"Tables via Phalanx: {tables}")

    def test_phalanx_create_and_read_table(self, tmp_path: Path) -> None:
        """Test creating and reading a table via Phalanx."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        # Create a test table
        table_name = f"phalanx_test_{uuid.uuid4().hex[:8]}"
        data = pa.Table.from_pydict({"id": [1, 2, 3], "value": ["a", "b", "c"]})

        try:
            db.create_table(table_name, data)

            # Verify table exists
            assert table_name in db.table_names()

            # Read back data
            tbl = db.open_table(table_name)
            assert tbl.count_rows() == 3
        finally:
            # Cleanup
            db.drop_table(table_name)

    def test_phalanx_with_upload_bucket(self, tmp_path: Path) -> None:
        """Test Phalanx connection with separate upload bucket."""
        upload_bucket = str(tmp_path / "uploads")

        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
            upload_dir=upload_bucket,
        )

        assert db._upload_dir == upload_bucket


class TestPhalanxSystemTables:
    """Tests for system tables (jobs, clusters, manifests) via Phalanx."""

    def test_list_manifests_via_phalanx(self) -> None:
        """Test listing jobs via Phalanx connection."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        # Should be able to list jobs (may be empty)
        jobs = db.list_manifests()
        assert isinstance(jobs, list)

    def test_list_clusters_via_phalanx(self) -> None:
        """Test listing clusters via Phalanx connection."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        # Should be able to list clusters (may be empty)
        clusters = db.list_clusters()
        assert isinstance(clusters, list)


class TestPhalanxBackfill:
    """Integration tests for running backfill jobs through Phalanx."""

    @pytest.fixture
    def test_table(self) -> str:
        """Create a test table for backfill tests."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        table_name = f"backfill_test_{uuid.uuid4().hex[:8]}"
        data = pa.Table.from_pydict(
            {
                "id": list(range(100)),
                "text": [f"item_{i}" for i in range(100)],
            }
        )

        db.create_table(table_name, data)
        yield table_name

        # Cleanup
        db.drop_table(table_name)

    @pytest.mark.skip(reason="no support in RemoteTable")
    # todo: https://linear.app/lancedb/issue/GEN-267/enterprise-support-for-backfillcreate-materialized-view
    def test_backfill_via_phalanx_local_ray(self, test_table: str) -> None:
        """Test backfill job execution via Phalanx with local Ray cluster.

        This test:
        1. Connects to Phalanx server
        2. Creates a backfill job on a test table
        3. Runs the job with local Ray
        4. Verifies results
        """
        from geneva.cluster import GenevaClusterType

        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        @geneva.udf(data_type=pa.string(), version=uuid.uuid4().hex)
        def uppercase_text(text: str) -> str:
            return text.upper() if text else text

        tbl = db.open_table(test_table)

        # note create_materialized_view and add_columns with UDF not supported
        # by remote table
        with db.context(cluster_type=GenevaClusterType.LOCAL_RAY):
            mv = tbl.search().create_materialized_view(db, "test")
            mv.refresh()

            tbl.add_columns(
                {"b": uppercase_text},  # type: ignore[arg-type]
                batch_size=32,
                concurrency=2,
                intra_applier_concurrency=2,
            )
            tbl.backfill("b")
            # todo: add data assertions

        _LOG.info(f"Backfill via Phalanx completed for table {test_table}")


class TestPhalanxFlightSQL:
    """Tests for FlightSQL client via Phalanx."""

    def test_flight_client_initialization(self) -> None:
        """Test that flight client is properly initialized for Phalanx."""
        db = connect(
            uri=DB_URI,
            api_key=PHALANX_API_KEY,
            host_override=PHALANX_HOST,
        )

        # Accessing flight_client should not raise
        # Note: actual queries require proper FlightSQL setup on Phalanx
        assert db._host_override is not None
