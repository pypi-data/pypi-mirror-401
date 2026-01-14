# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# definition of the read task, which is portion of a fragment

import hashlib
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, cast

import attrs
import pyarrow as pa
import pyarrow.compute as pc
from typing_extensions import override

from geneva.checkpoint_utils import format_checkpoint_key, format_checkpoint_prefix
from geneva.query import ExtractedTransform
from geneva.table import Table, TableReference
from geneva.transformer import BACKFILL_SELECTED, UDF, UDFArgType
from geneva.utils.arrow import batch_add_column

_LOG = logging.getLogger(__name__)

DEFAULT_CHECKPOINT_ROWS = 100


class ReadTask(ABC):
    """
    A task to read data that has a defined output location and unique identifier
    """

    @abstractmethod
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        """Return the data to read"""

    @abstractmethod
    def checkpoint_key(self) -> str:
        """Return a unique key for this task"""

    @abstractmethod
    def dest_frag_id(self) -> int:
        """Return the id of the destination fragment"""

    @abstractmethod
    def dest_offset(self) -> int:
        """Return the offset into the destination fragment"""

    @abstractmethod
    def num_rows(self) -> int:
        """Return the number of rows this task will read"""

    @abstractmethod
    def table_uri(self) -> str:
        """Return the source table URI for this read task"""


@attrs.define(order=True)
class ScanTask(ReadTask):
    uri: str
    table_ref: TableReference
    columns: list[str]
    frag_id: int
    offset: int
    limit: int

    version: int | None = None
    where: str | None = None

    with_row_address: bool = False
    # Hash of source data files for input columns in this fragment.
    # Used in checkpoint keys.
    src_files_hash: str | None = None

    def _get_table(self) -> Table:
        # Use the task's version (set during planning) to ensure we read from
        # the correct point-in-time snapshot, not the latest version
        if self.version is not None and self.table_ref.version != self.version:
            # Create a new reference with the correct version
            versioned_ref = attrs.evolve(self.table_ref, version=self.version)
            return versioned_ref.open()
        return self.table_ref.open()

    @override
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        _LOG.debug(
            f"Reading {self.uri} with version {self.version} for cols {self.columns}"
            f" offset {self.offset} limit {self.limit} where='{self.where}'"
        )
        tbl = self._get_table()
        query = tbl.search().enable_internal_api()  # type: ignore[attr-defined]

        if self.with_row_address:
            query = query.with_row_address()

        query = query.with_fragments(self.frag_id).offset(self.offset).limit(self.limit)
        query = query.with_where_as_bool_column()

        # works with blobs but not filters
        if self.columns is not None:
            query = query.select(self.columns)
        if self.where is not None:
            query = query.where(self.where)

        # Currently lancedb reports the wrong type for the return value
        # of the to_batches method.  Remove pyright ignore when fixed.
        batches: pa.RecordBatchReader = query.to_batches(batch_size)  # pyright: ignore[reportAssignmentType]

        yield from batches

    @override
    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"{self.uri}:{self.version}:{self.columns}:{self.frag_id}:{self.offset}:{self.limit}:{self.where}".encode(),
        )
        return hasher.hexdigest()

    @override
    def dest_frag_id(self) -> int:
        return self.frag_id

    @override
    def dest_offset(self) -> int:
        return self.offset

    @override
    def num_rows(self) -> int:
        # TODO calculate # rows
        return self.limit

    @override
    def table_uri(self) -> str:
        return self.uri


@attrs.define(order=True)
class CopyTask(ReadTask):
    src: TableReference
    dst: TableReference
    # columns: list of names or dict mapping output names to expressions
    # e.g., ["id", "value"] or {"id": "id", "doubled": "value * 2"}
    columns: list[str] | dict[str, str]
    frag_id: int
    offset: int
    limit: int
    # Hash of source data files for input columns in this fragment.
    # Used in checkpoint keys.
    src_files_hash: str | None = None

    @property
    def version(self) -> int | None:
        """Return source version for checkpoint key generation."""
        return self.src.version

    @override
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        dst_tbl = self.dst.open()

        # Read __source_row_id from the specific destination fragment using Lance API
        # This ensures we read from the correct fragment, not from the entire table
        dst_lance = dst_tbl.to_lance()
        dst_fragment = dst_lance.get_fragment(self.frag_id)

        # Use dataset scanner with fragment restriction for efficient offset/limit
        # This only reads the requested slice, avoiding loading the entire fragment
        scanner = dst_lance.scanner(
            columns=["__source_row_id"],
            offset=self.offset,
            limit=self.limit,
            fragments=[dst_fragment],
        )
        row_ids_batch = scanner.to_table()
        row_ids = cast("list[int]", row_ids_batch["__source_row_id"].to_pylist())

        # TODO: Add streaming take to lance
        src_table_lance = self.src.open().to_lance()
        _LOG.info(
            f"CopyTask: frag_id={self.frag_id}, offset={self.offset}, "
            f"limit={self.limit}, row_ids={row_ids}"
        )
        table = src_table_lance._take_rows(row_ids, columns=self.columns)
        _LOG.info(f"CopyTask: Fetched {table.num_rows} rows from source")

        # Generate row addresses based on ACTUAL number of rows returned
        # (not self.limit, which may be larger than actual rows)
        row_addrs = self._get_row_addrs(table.num_rows)
        table = table.add_column(table.num_columns, "_rowaddr", row_addrs)

        batches = table.to_batches(max_chunksize=batch_size)

        yield from batches

    @override
    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"CopyTask:{self.src.db_uri}:{self.src.table_name}:{self.src.version}:{self.columns}:{self.dst.db_uri}:{self.dst.table_name}:{self.frag_id}:{self.offset}:{self.limit}".encode(),
        )
        return hasher.hexdigest()

    @override
    def dest_frag_id(self) -> int:
        return self.frag_id

    @override
    def dest_offset(self) -> int:
        return self.offset

    def _get_row_addrs(self, num_rows: int) -> pa.Array:
        frag_mod = self.frag_id << 32
        addrs = [frag_mod + x for x in range(self.offset, self.offset + num_rows)]
        return cast("pa.Array", pa.array(addrs, pa.uint64()))

    @override
    def num_rows(self) -> int:
        # TODO calculate # rows
        return self.limit

    @override
    def table_uri(self) -> str:
        return f"{self.src.db_uri}/{self.src.table_name}"


class MapTask(ABC):
    @abstractmethod
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        """Return a unique key for the task"""

    @abstractmethod
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        """Return a stable prefix (no fragment/range) for logging/aggregation."""

    @abstractmethod
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        """Return legacy map task key (pre-range) for backwards compat."""

    @abstractmethod
    def input_columns(self) -> list[str] | None:
        """Return source columns used by this map task (if known)."""

    @abstractmethod
    def name(self) -> str:
        """Return a name to use for progress strings"""

    @abstractmethod
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        """Apply the map function to the input batch, returning the output batch"""

    @abstractmethod
    def output_schema(self) -> pa.Schema:
        """Return the output schema"""

    @abstractmethod
    def is_cuda(self) -> bool:
        """Return true if the task requires CUDA

        .. deprecated::
            Use :meth:`num_gpus` instead to get the actual GPU requirement.
        """

    @abstractmethod
    def num_cpus(self) -> float | None:
        """Return the number of CPUs the task should use (None for default)"""

    @abstractmethod
    def num_gpus(self) -> float | None:
        """Return the number of GPUs the task should use (None for default)"""

    @abstractmethod
    def memory(self) -> int | None:
        """Return the amount of RAM the task should use (None for default)"""

    @abstractmethod
    def batch_size(self) -> int:
        """Return the batch size the task should use"""

    def adaptive_checkpoint_bounds(self) -> tuple[int | None, int | None]:
        """Return adaptive checkpoint (min, max) bounds when supported."""
        return None, None

    def initial_checkpoint_size(self) -> int | None:
        """Return an explicit initial checkpoint size for adaptive sizing."""
        return None

    def udf_version(self) -> str | None:
        """Return the UDF version hash for checkpoint comparison (optional)."""
        return None


@attrs.define(order=True)
class BackfillUDFTask(MapTask):
    udfs: dict[str, UDF] = (
        attrs.field()
    )  # TODO: use attrs to enforce stateful udfs are handled here

    # this is needed to differentiate a filtered task's checkpont keys
    # for backfill jobs
    where: str | None = attrs.field(default=None)

    # If set, this overrides the UDF-declared batch size. Used to respect
    # the backfill(batch_size=...) parameter from the job config.
    override_batch_size: int | None = attrs.field(default=None)
    explicit_checkpoint_size: bool = attrs.field(default=False)
    min_checkpoint_size: int | None = attrs.field(default=None)
    max_checkpoint_size: int | None = attrs.field(default=None)

    def __get_udf(self) -> tuple[str, UDF]:
        # TODO: Add support for multiple columns to add_columns operation
        if len(self.udfs) != 1:
            raise NotImplementedError("Add columns does not support multiple UDFs")
        col, udf = next(iter(self.udfs.items()))
        if not isinstance(udf, UDF):
            # stateful udf are Callable classes that need to be instantiated.
            udf = udf()
        return col, udf

    def adaptive_checkpoint_bounds(self) -> tuple[int | None, int | None]:
        min_size = self.min_checkpoint_size
        max_size = self.max_checkpoint_size
        if min_size is None or max_size is None:
            _, udf = self.__get_udf()
            if min_size is None:
                min_size = getattr(udf, "min_checkpoint_size", None)
            if max_size is None:
                max_size = getattr(udf, "max_checkpoint_size", None)
        return min_size, max_size

    def initial_checkpoint_size(self) -> int | None:
        if self.override_batch_size is not None and self.explicit_checkpoint_size:
            return self.override_batch_size
        _, udf = self.__get_udf()
        if udf.checkpoint_size is not None:
            return udf.checkpoint_size
        if udf.batch_size is not None:
            return udf.batch_size
        return None

    @override
    def name(self) -> str:
        name, _ = self.__get_udf()
        return name

    @override
    def input_columns(self) -> list[str] | None:
        input_cols: set[str] = set()
        for udf in self.udfs.values():
            if not isinstance(udf, UDF):
                try:
                    udf = udf()
                except Exception:
                    return None
            cols = udf.input_columns
            if cols is None:
                return None
            input_cols.update(cols)
        if not input_cols:
            return None
        return list(input_cols)

    @override
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        # 'where' is required in key to distinguish different partial backfills jobs
        # hashing it so that it cannot be used as a directory path attack vector
        col, udf = self.__get_udf()
        prefix = udf.checkpoint_prefix(
            column=col,
            dataset_uri=dataset_uri,
            where=where if where is not None else self.where,
            src_files_hash=src_files_hash,
        )
        return format_checkpoint_key(
            prefix,
            frag_id=frag_id if frag_id is not None else 0,
            start=start,
            end=end,
        )

    @override
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        col, udf = self.__get_udf()
        return udf.checkpoint_prefix(
            column=column or col,
            dataset_uri=dataset_uri,
            where=where if where is not None else self.where,
            src_files_hash=src_files_hash,
        )

    @override
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        col, udf = self.__get_udf()
        where_val = where if where is not None else self.where
        if where_val:
            hasher = hashlib.md5()
            hasher.update(where_val.encode())
            return f"{udf.checkpoint_key}:where={hasher.hexdigest()}"
        return udf.checkpoint_key

    @override
    def apply(self, batch: pa.RecordBatch | list[dict[str, Any]]) -> pa.RecordBatch:
        udf_col_name, udf = self.__get_udf()

        if isinstance(batch, pa.RecordBatch):
            row_addr = batch["_rowaddr"]
            has_carry_forward_col = udf_col_name in batch.schema.names
            has_backfill_selected = BACKFILL_SELECTED in batch.schema.names
        else:
            # might have blob_columns which needs _rowaddr
            row_addr = pa.array([x["_rowaddr"] for x in batch], type=pa.uint64())
            has_carry_forward_col = bool(batch) and (udf_col_name in batch[0])
            has_backfill_selected = bool(batch) and (BACKFILL_SELECTED in batch[0])

        # drop carry_foward cols from what will be UDF arguments.
        if isinstance(batch, pa.RecordBatch):
            if udf_col_name in batch.schema.names:
                # select all the other columns
                col_val_arrays = [
                    batch[col] for col in batch.schema.names if col != udf_col_name
                ]
                col_names = [col for col in batch.schema.names if col != udf_col_name]
                batch_for_udf = pa.RecordBatch.from_arrays(col_val_arrays, col_names)
            else:
                batch_for_udf = batch
        else:
            # list-of-dicts case: just filter out the key
            batch_for_udf = [
                {k: v for k, v in row.items() if k != udf_col_name} for row in batch
            ]

        # execute the udf
        # Optimization: For RecordBatch and Array UDFs with filtering, only process
        # selected rows
        try:
            if (
                has_backfill_selected
                and isinstance(batch, pa.RecordBatch)
                and udf.arg_type in (UDFArgType.RECORD_BATCH, UDFArgType.ARRAY)
            ):
                # Get the selection mask
                mask = batch[BACKFILL_SELECTED]

                # Will be set to array data or None if no rows processed
                new_arr = None

                # Check if any rows are selected
                if any(mask.to_pylist()):
                    # Filter batch_for_udf to only include selected rows
                    filtered_batch_for_udf = pc.filter(batch_for_udf, mask)  # type: ignore[call-overload,arg-type]
                    _LOG.debug(
                        f"{udf.arg_type.name} UDF optimization: processing "
                        f"{filtered_batch_for_udf.num_rows} rows instead of "  # type: ignore[attr-defined]
                        f"{batch_for_udf.num_rows}"  # type: ignore[attr-defined]
                    )

                    # Execute UDF on filtered batch
                    filtered_new_arr = udf(filtered_batch_for_udf, use_applier=True)

                    # Expand results back to full batch size.
                    # Get indices of rows that passed the filter
                    indices_array = pa.array(range(batch.num_rows))
                    selected_indices = pc.filter(indices_array, mask)

                    if len(filtered_new_arr) > 0:
                        # Build complete list with values at correct positions
                        result_pylist = [None] * batch.num_rows
                        for i, filtered_val in enumerate(filtered_new_arr):
                            original_idx = selected_indices[i].as_py()  # type: ignore[attr-defined]
                            result_pylist[original_idx] = filtered_val.as_py()

                        # Create array using pa.table() to ensure proper buffer
                        # structure for variable-width types (strings, binary,
                        # lists). pa.table() guarantees correct buffer allocation.
                        # See writer.py:_make_filler_batch() for details.
                        temp_table = pa.table(
                            {"_temp": result_pylist},
                            schema=pa.schema([("_temp", udf.data_type)]),
                        )  # type: ignore[arg-type,list-item]
                        new_arr = temp_table.column("_temp").combine_chunks()

                # If no rows were processed, return array of nulls
                if new_arr is None:
                    # Use pa.nulls() to ensure proper buffer structure for
                    # variable-width types (strings, binary, lists).
                    # See writer.py:_make_filler_batch() for details.
                    new_arr = pa.nulls(batch.num_rows, type=udf.data_type)  # type: ignore[arg-type]
            else:
                # Original behavior for non-RecordBatch UDFs or when no filtering
                new_arr = udf(batch_for_udf, use_applier=True)
        except KeyError as e:
            # Column not found in batch
            if isinstance(batch_for_udf, pa.RecordBatch):
                available_cols = batch_for_udf.schema.names
            elif batch_for_udf and len(batch_for_udf) > 0:  # list[dict] with elements
                available_cols = list(batch_for_udf[0].keys())
            else:  # empty list
                available_cols = []
            raise KeyError(
                f"UDF '{udf.name}' failed: column {e} not found in batch. "
                f"Available columns: {available_cols}. "
                f"UDF expects input_columns: {udf.input_columns}. "
                f"This typically means the UDF's input_columns don't match "
                f"the table schema."
            ) from e
        except (pa.ArrowInvalid, pa.ArrowTypeError) as e:
            # Type mismatch or serialization error
            batch_schema = (
                batch_for_udf.schema
                if isinstance(batch_for_udf, pa.RecordBatch)
                else None
            )
            raise TypeError(
                f"UDF '{udf.name}' failed with type error: {e}. "
                f"Input batch schema: {batch_schema}. "
                f"UDF expects input_columns: {udf.input_columns}. "
                f"UDF output type: {udf.data_type}. "
                f"This often indicates a type mismatch (e.g., float32 vs float64) "
                f"between the table schema and UDF expectations."
            ) from e

        # now finalize the result.
        if not has_carry_forward_col or not has_backfill_selected:
            schema = pa.schema(
                [
                    pa.field(udf_col_name, udf.data_type, metadata=udf.field_metadata),
                    pa.field("_rowaddr", pa.uint64()),
                ]
            )

            # no carry forward col? return the new
            return pa.record_batch([new_arr, row_addr], schema=schema)

        # handle carry forward of old values
        if isinstance(batch, pa.RecordBatch):
            orig_arr = batch[udf_col_name]
            mask = batch[BACKFILL_SELECTED]
        else:
            # extract py values and wrap into pa array
            orig_vals = [x.get(udf_col_name) for x in batch]
            orig_arr = pa.array(orig_vals, type=new_arr.type)
            mask_vals = [x.get(BACKFILL_SELECTED) for x in batch]
            mask = pa.array(mask_vals, type=pa.bool_())

        merged = pc.if_else(mask, new_arr, orig_arr)
        schema = pa.schema(
            [
                pa.field(udf_col_name, udf.data_type, metadata=udf.field_metadata),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        return pa.record_batch([merged, row_addr], schema=schema)

    @override
    def output_schema(self) -> pa.Schema:
        name, udf = self.__get_udf()
        return pa.schema(
            [pa.field(name, udf.data_type), pa.field("_rowaddr", pa.uint64())]
        )

    @override
    def is_cuda(self) -> bool:
        """Deprecated: Use num_gpus() instead."""
        _, udf = self.__get_udf()
        return bool(udf.num_gpus and udf.num_gpus > 0)

    @override
    def num_cpus(self) -> float | None:
        _, udf = self.__get_udf()
        return udf.num_cpus

    @override
    def num_gpus(self) -> float | None:
        _, udf = self.__get_udf()
        return udf.num_gpus

    @override
    def memory(self) -> int | None:
        _, udf = self.__get_udf()
        return udf.memory

    @override
    def batch_size(self) -> int:
        if self.override_batch_size is not None:
            return self.override_batch_size
        _, udf = self.__get_udf()
        return udf.batch_size or DEFAULT_CHECKPOINT_ROWS

    @override
    def udf_version(self) -> str | None:
        """Return the UDF version hash for checkpoint comparison."""
        _, udf = self.__get_udf()
        return udf.version


@attrs.define(order=True)
class CopyTableTask(MapTask):
    column_udfs: list[ExtractedTransform] = attrs.field()
    view_name: str = attrs.field()
    schema: pa.Schema = attrs.field()
    override_batch_size: int | None = attrs.field(default=None)

    @override
    def name(self) -> str:
        return self.view_name

    @override
    def input_columns(self) -> list[str] | None:
        if not self.column_udfs:
            return None
        input_cols: set[str] = set()
        for transform in self.column_udfs:
            cols = transform.udf.input_columns
            if cols is None:
                return None
            input_cols.update(cols)
        if not input_cols:
            return None
        return list(input_cols)

    @override
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        column_label = (
            "+".join(sorted(transform.output_name for transform in self.column_udfs))
            if self.column_udfs
            else self.view_name
        )
        prefix = format_checkpoint_prefix(
            udf_name=self.view_name,
            udf_version="copy",
            column=column_label,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )
        return format_checkpoint_key(
            prefix,
            frag_id=frag_id if frag_id is not None else 0,
            start=start,
            end=end,
        )

    @override
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        column_label = column
        if column_label is None:
            column_label = (
                "+".join(
                    sorted(transform.output_name for transform in self.column_udfs)
                )
                if self.column_udfs
                else self.view_name
            )
        return format_checkpoint_prefix(
            udf_name=self.view_name,
            udf_version="copy",
            column=column_label,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )

    @override
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        return self.view_name

    @override
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        for transform in self.column_udfs:
            new_arr = transform.udf(batch)
            # Create field with metadata (e.g., lance-encoding:blob) to ensure
            # proper encoding when written to Lance files
            field = pa.field(
                transform.output_name,
                transform.udf.data_type,
                metadata=transform.udf.field_metadata,
            )
            batch = batch_add_column(batch, transform.output_index, field, new_arr)

        return batch

    @override
    def output_schema(self) -> pa.Schema:
        return self.schema

    @override
    def is_cuda(self) -> bool:
        """Deprecated: Use num_gpus() instead."""
        return any(
            column_udf.udf.num_gpus and column_udf.udf.num_gpus > 0
            for column_udf in self.column_udfs
        )

    @override
    def num_cpus(self) -> float | None:
        return max(
            (
                column_udf.udf.num_cpus
                for column_udf in self.column_udfs
                if column_udf.udf.num_cpus is not None
            ),
            default=None,
        )

    @override
    def num_gpus(self) -> float | None:
        return max(
            (
                column_udf.udf.num_gpus
                for column_udf in self.column_udfs
                if column_udf.udf.num_gpus is not None
            ),
            default=None,
        )

    @override
    def memory(self) -> int | None:
        return max(
            (
                column_udf.udf.memory
                for column_udf in self.column_udfs
                if column_udf.udf.memory is not None
            ),
            default=None,
        )

    @override
    def batch_size(self) -> int:
        if self.override_batch_size is not None:
            return self.override_batch_size
        if not self.column_udfs:
            return DEFAULT_CHECKPOINT_ROWS
        return min(
            column_udf.udf.batch_size or DEFAULT_CHECKPOINT_ROWS
            for column_udf in self.column_udfs
        )
