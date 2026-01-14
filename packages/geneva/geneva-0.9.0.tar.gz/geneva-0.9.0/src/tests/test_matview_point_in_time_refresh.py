# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for materialized view point-in-time refresh (rollback to older versions)."""

from unittest.mock import patch

import pytest

from conftest import create_filtered_mv, make_batch, refresh_and_verify
from geneva import connect
from geneva.jobs.config import JobConfig
from geneva.packager import DockerUDFPackager

pytestmark = pytest.mark.ray


def test_point_in_time_refresh_requires_stable_row_ids(tmp_path) -> None:
    """Test that point-in-time refresh fails without stable row IDs."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITHOUT stable row IDs
    animals = db.create_table("animals", make_batch(0, 100))
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Add more data
    animals.add(make_batch(100, 50))
    v2 = animals.version
    assert v2 > v1

    # Refresh to v2 should fail (different version without stable row IDs)
    with pytest.raises(RuntimeError, match="stable row IDs"):
        dogs.refresh()


def test_point_in_time_refresh_rollback(tmp_path) -> None:
    """Test that we can roll back to an older source version with stable row IDs."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs out of 100 (every other row)

    # Add more data
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(dogs, 75)  # 75 dogs out of 150

    # Rollback to v1 (point-in-time refresh)
    refresh_and_verify(dogs, 50, src_version=v1)  # Back to 50 dogs

    # Can refresh forward again
    refresh_and_verify(dogs, 75)  # Back to 75 dogs


def test_point_in_time_refresh_multiple_rollbacks(tmp_path) -> None:
    """Test multiple rollback and forward refreshes."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Add batch 2
    animals.add(make_batch(100, 50))
    v2 = animals.version
    refresh_and_verify(dogs, 75)

    # Add batch 3
    animals.add(make_batch(150, 50))
    v3 = animals.version
    refresh_and_verify(dogs, 100)

    # Rollback to v1
    refresh_and_verify(dogs, 50, src_version=v1)

    # Rollback to v2
    refresh_and_verify(dogs, 75, src_version=v2)

    # Forward to v3
    refresh_and_verify(dogs, 100, src_version=v3)

    # Rollback to v1 again
    refresh_and_verify(dogs, 50, src_version=v1)


def test_point_in_time_refresh_without_filter(tmp_path) -> None:
    """Test point-in-time refresh on MV without WHERE filter."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV without filter (copies all rows)
    all_animals = animals.search(None).create_materialized_view(
        conn=db, view_name="all_animals"
    )
    refresh_and_verify(all_animals, 100)

    # Add more data
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(all_animals, 150)

    # Rollback to v1
    refresh_and_verify(all_animals, 100, src_version=v1)

    # Forward again
    refresh_and_verify(all_animals, 150)


def test_point_in_time_refresh_batched_deletion(tmp_path) -> None:
    """Test that rollback deletes rows in batches when delete_batch_size is small."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV without filter (copies all rows)
    all_animals = animals.search(None).create_materialized_view(
        conn=db, view_name="all_animals"
    )
    refresh_and_verify(all_animals, 100)

    # Add more data - 50 additional rows
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(all_animals, 150)

    # Rollback to v1 with small batch size (10) to force multiple batches
    # This will delete 50 rows in 5 batches of 10
    config_with_small_batch = JobConfig(delete_batch_size=10)

    with patch.object(JobConfig, "get", return_value=config_with_small_batch):
        refresh_and_verify(all_animals, 100, src_version=v1)


def test_forward_refresh_with_source_deletions(tmp_path) -> None:
    """Test that forward refresh deletes MV rows when source rows are deleted."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs (IDs 0, 2, 4, ..., 98)

    # Delete some dogs from source (IDs 0, 2, 4 are dogs)
    animals.delete("id IN (0, 2, 4)")

    # Forward refresh should detect and delete corresponding MV rows
    refresh_and_verify(dogs, 47)  # 50 - 3 deleted dogs


def test_forward_refresh_with_mixed_adds_and_deletes(tmp_path) -> None:
    """Test forward refresh handles both additions and deletions."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs

    # Delete some dogs (IDs 0, 2 are dogs)
    animals.delete("id IN (0, 2)")

    # Add new rows (IDs 100-149, 25 will be dogs)
    animals.add(make_batch(100, 50))

    # Forward refresh should handle both deletions and additions
    # 50 original - 2 deleted + 25 new dogs = 73
    refresh_and_verify(dogs, 73)


def test_forward_refresh_filter_affects_deletions(tmp_path) -> None:
    """Test that MV filter is applied when checking deletions."""
    packager = DockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)

    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Delete cats (IDs 1, 3, 5 are cats, not dogs)
    animals.delete("id IN (1, 3, 5)")

    # Forward refresh should not affect MV (cats weren't in it)
    refresh_and_verify(dogs, 50)  # Still 50 dogs
