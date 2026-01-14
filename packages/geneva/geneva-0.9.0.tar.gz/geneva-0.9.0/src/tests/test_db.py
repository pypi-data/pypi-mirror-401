# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
from pathlib import Path
from unittest.mock import MagicMock, patch

import lancedb
import pyarrow as pa
import pytest

from geneva import connect


def test_connect(tmp_path: Path) -> None:
    db = connect(tmp_path)

    # Use lancedb to verify the results are the same
    ldb = lancedb.connect(tmp_path)

    # Create a Table with integer columns
    tbl = pa.Table.from_pydict({"a": [1, 2, 3], "b": [4, 5, 6]})
    db.create_table("table1", tbl)
    ldb_tbls = db.table_names()
    assert "table1" in ldb_tbls
    db.open_table("table1")

    db_tbls = db.table_names()
    assert db_tbls == ldb_tbls

    # Use lancedb to read the data back
    ldb_tbl = ldb.open_table("table1")
    assert ldb_tbl.to_arrow() == tbl
    db.drop_table("table1")


def test_connect_non_existent(tmp_path: Path) -> None:
    db = connect(tmp_path)
    assert db.table_names() == []

    with pytest.raises(ValueError, match=r".*was not found"):
        db.open_table("non_existent")


class TestConnectRemote:
    """Tests for connect() with remote db:// URI (Phalanx server)."""

    def test_connect_remote_uri_uses_host_override(self) -> None:
        """Test that db:// URI with host_override triggers remote connection."""
        with patch("geneva.db.lancedb.connect") as mock_lancedb_connect:
            mock_conn = MagicMock()
            mock_conn.table_names.return_value = []
            mock_lancedb_connect.return_value = mock_conn

            db = connect(
                uri="db://my_database",
                api_key="test-api-key",
                host_override="https://phalanx.internal:8080",
            )

            # Trigger the lazy connection
            _ = db._connect

            # Verify lancedb.connect was called with correct parameters
            mock_lancedb_connect.assert_called_once()
            call_kwargs = mock_lancedb_connect.call_args.kwargs
            assert call_kwargs.get("api_key") is not None
            assert call_kwargs.get("host_override") == "https://phalanx.internal:8080"

            # Verify the URI was passed correctly
            call_args = mock_lancedb_connect.call_args.args
            assert call_args[0] == "db://my_database"

    def test_connect_remote_stores_connection_params(self) -> None:
        """Test that remote connection parameters are stored on Connection object."""
        db = connect(
            uri="db://test_db",
            api_key="my-api-key",
            host_override="https://phalanx.example.com",
            region="us-west-2",
        )

        assert db.uri == "db://test_db"
        assert db._host_override == "https://phalanx.example.com"
        assert db._region == "us-west-2"
        # api_key is wrapped in Credential
        assert db._api_key is not None

    def test_connect_remote_system_namespace_empty_without_namespace_impl(self) -> None:
        """Test that system_namespace is empty for non-namespace remote connections.

        For db:// remote connections (without namespace_impl), system tables
        are accessed at the root level of the remote database, so system_namespace
        should be empty.
        """
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
            system_namespace=["prod", "system"],
        )

        # Without namespace_impl, system_namespace is forced to []
        assert db.system_namespace == []

    def test_connect_remote_creates_checkpoint_store(self) -> None:
        """Test that checkpoint store is created for remote connections."""
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com",
        )

        # Checkpoint store should be created
        assert db._checkpoint_store is not None

    def test_connect_local_vs_remote_differentiation(self, tmp_path: Path) -> None:
        """Test that local and remote URIs are handled differently."""
        # Local connection
        local_db = connect(tmp_path)
        assert not local_db.uri.startswith("db://")

        # Remote connection
        remote_db = connect(
            uri="db://remote_db",
            api_key="key",
            host_override="https://phalanx.example.com",
        )
        assert remote_db.uri == "db://remote_db"

    def test_connect_remote_flight_client_creation(self) -> None:
        """Test that flight_client is properly configured for remote connections."""
        db = connect(
            uri="db://test_db",
            api_key="test-key",
            host_override="https://phalanx.example.com:8080",
        )

        # Access flight_client to trigger creation
        with patch("flightsql.FlightSQLClient") as mock_flight:
            mock_flight.return_value = MagicMock()
            _ = db.flight_client

            # Verify FlightSQLClient was created with correct host
            mock_flight.assert_called_once()
            call_kwargs = mock_flight.call_args.kwargs
            assert call_kwargs.get("host") == "phalanx.example.com"


class TestConnectConfig:
    """Tests for connect() configuration loading."""

    def test_connect_loads_config_defaults(self, tmp_path: Path) -> None:
        """Test that connect() loads defaults from config."""
        db = connect(tmp_path)
        # Default region should be set
        assert db._region == "us-east-1"

    def test_connect_explicit_params_override_config(self, tmp_path: Path) -> None:
        """Test that explicit parameters override config defaults."""
        db = connect(tmp_path, region="eu-west-1")
        assert db._region == "eu-west-1"


class TestUploadBucket:
    """Tests for upload_bucket configuration (Phalanx security model)."""

    def test_connect_with_upload_bucket(self, tmp_path: Path) -> None:
        """Test that upload_bucket is stored on Connection object."""
        db = connect(
            tmp_path,
            upload_dir="s3://my-upload-bucket/manifests",
        )
        assert db._upload_dir == "s3://my-upload-bucket/manifests"

    def test_connect_without_upload_bucket(self, tmp_path: Path) -> None:
        """Test that upload_bucket defaults to None."""
        db = connect(tmp_path)
        assert db._upload_dir is None

    def test_upload_bucket_with_remote_connection(self) -> None:
        """Test upload_bucket with remote db:// URI (Phalanx scenario)."""
        db = connect(
            uri="db://my_database",
            api_key="test-api-key",
            host_override="https://phalanx.example.com",
            upload_dir="gs://enterprise-upload-bucket/manifests",
        )
        assert db._upload_dir == "gs://enterprise-upload-bucket/manifests"
        assert db.uri == "db://my_database"

    def test_upload_bucket_serialization(self, tmp_path: Path) -> None:
        """Test that upload_bucket is properly serialized/deserialized."""
        db = connect(
            tmp_path,
            upload_dir="s3://my-upload-bucket/manifests",
        )

        # Get serialized state
        state = db.__getstate__()
        assert state["upload_dir"] == "s3://my-upload-bucket/manifests"

        # Create new connection from state
        new_db = connect(tmp_path)
        new_db.__setstate__(state)
        assert new_db._upload_dir == "s3://my-upload-bucket/manifests"

    def test_define_manifest_uses_upload_bucket(self, tmp_path: Path) -> None:
        """Test that define_manifest uses upload_bucket when configured."""
        db = connect(
            tmp_path,
            upload_dir="s3://my-upload-bucket/manifests",
        )

        # Mock the Uploader to capture how it's instantiated
        with patch("geneva.db.Uploader") as mock_uploader_class:
            mock_uploader = MagicMock()
            mock_uploader_class.return_value = mock_uploader

            # Mock upload_local_env to avoid actual file operations
            with patch("geneva.db.upload_local_env") as mock_upload:
                mock_upload.return_value.__enter__ = MagicMock(return_value=[])
                mock_upload.return_value.__exit__ = MagicMock(return_value=None)

                # Mock the manifest manager
                with patch.object(db, "_manifest_manager") as mock_mgr:
                    mock_mgr.get_table.return_value = MagicMock()
                    db._manifest_manager = mock_mgr

                    # Create a minimal manifest
                    from geneva.manifest.mgr import GenevaManifest

                    manifest = GenevaManifest(name="test_manifest")

                    db.define_manifest("test_manifest", manifest)

                    # Verify Uploader was called with upload_dir (not table context)
                    mock_uploader_class.assert_called_once_with(
                        upload_dir="s3://my-upload-bucket/manifests"
                    )
