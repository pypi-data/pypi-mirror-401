# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import attrs
from typing_extensions import Self  # noqa: UP035

from geneva.checkpoint import CheckpointConfig, CheckpointStore
from geneva.config import ConfigBase


@attrs.define
class JobConfig(ConfigBase):
    """Geneva Job Configurations."""

    checkpoint: CheckpointConfig = attrs.field(default=CheckpointConfig("tempfile"))

    batch_size: int = attrs.field(default=10240, converter=int)

    task_size: int | None = attrs.field(
        default=None, converter=lambda v: None if v is None else int(v)
    )

    task_shuffle_diversity: int = attrs.field(default=8, converter=int)

    # How many fragments to be committed in one single transaction.
    commit_granularity: int = attrs.field(default=64, converter=int)

    # How many rows to delete per batch during point-in-time MV refresh rollback.
    delete_batch_size: int = attrs.field(default=10000, converter=int)

    @classmethod
    def name(cls) -> str:
        return "job"

    def make_checkpoint_store(self) -> CheckpointStore:
        return (self.checkpoint or CheckpointConfig("tempfile")).make()

    def with_overrides(
        self,
        *,
        batch_size: int | None = None,
        task_size: int | None = None,
        task_shuffle_diversity: int | None = None,
        commit_granularity: int | None = None,
        delete_batch_size: int | None = None,
    ) -> Self:
        # IMPORTANT: ConfigBase.get() returns a cached singleton instance. This
        # method must not mutate `self` in-place, otherwise tests (and long-lived
        # processes) can leak configuration changes across calls.
        return attrs.evolve(
            self,
            batch_size=self.batch_size if batch_size is None else batch_size,
            task_size=(self.task_size if task_size is None else task_size),
            task_shuffle_diversity=(
                self.task_shuffle_diversity
                if task_shuffle_diversity is None
                else task_shuffle_diversity
            ),
            commit_granularity=(
                self.commit_granularity
                if commit_granularity is None
                else commit_granularity
            ),
            delete_batch_size=(
                self.delete_batch_size
                if delete_batch_size is None
                else delete_batch_size
            ),
        )
