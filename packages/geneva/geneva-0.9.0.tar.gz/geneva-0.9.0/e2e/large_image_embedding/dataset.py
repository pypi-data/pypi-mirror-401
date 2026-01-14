# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
from collections.abc import Generator

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pytest
from pyarrow.fs import S3FileSystem

from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)

ImageBatchGenerator = Generator[pa.RecordBatch, None, None]

# Keep this in sync with e2e/large_image_embedding/benchmarks/ray_data_main.py
INPUT_PREFIX = "s3://anonymous@ray-example-data/image-datasets/10TiB-b64encoded-images-in-parquet-v3/"
S3_REGION = "us-west-2"


def _parse_anonymous_s3_prefix(prefix: str) -> tuple[str, str]:
    if not prefix.startswith("s3://anonymous@"):
        raise ValueError("Expected s3://anonymous@... prefix")
    without_scheme = prefix[len("s3://anonymous@") :]
    bucket, _, key_prefix = without_scheme.partition("/")
    if not bucket or not key_prefix:
        raise ValueError(f"Invalid S3 prefix: {prefix}")
    return bucket, key_prefix


def _coerce_batch_schema(batch: pa.RecordBatch) -> pa.RecordBatch:
    if "url" not in batch.schema.names or "image" not in batch.schema.names:
        raise RuntimeError(f"Expected columns 'url' and 'image', got {batch.schema}")

    url = batch.column(batch.schema.get_field_index("url"))
    image = batch.column(batch.schema.get_field_index("image"))

    if pa.types.is_string(url.type) or pa.types.is_large_string(url.type):
        url = pc.cast(url, pa.large_string())

    if pa.types.is_string(image.type) or pa.types.is_large_string(image.type):
        image = pc.cast(image, pa.large_binary())
    elif pa.types.is_binary(image.type):
        image = pc.cast(image, pa.large_binary())

    return pa.record_batch([url, image], names=["url", "image"])


def load_large_image_rows(
    num_images: int = 20,
    frag_size: int = 5,
) -> ImageBatchGenerator:
    """
    Yield base64-encoded images from the same dataset used by the Ray benchmark.

    Columns:
      - url: string
      - image: bytes (base64-encoded bytes)
    """
    try:
        bucket, key_prefix = _parse_anonymous_s3_prefix(INPUT_PREFIX)
        filesystem = S3FileSystem(anonymous=True, region=S3_REGION)
        base_dir = f"{bucket}/{key_prefix}"
        dataset = ds.dataset(base_dir, filesystem=filesystem, format="parquet")
    except Exception as exc:
        pytest.skip(f"Failed to access Ray example dataset at {INPUT_PREFIX}: {exc}")

    remaining = int(num_images)
    batch_size = max(1, min(int(frag_size), remaining))

    scanner = dataset.scanner(columns=["url", "image"], batch_size=batch_size)
    for batch in tqdm(scanner.to_batches()):
        if remaining <= 0:
            break
        rb = (
            batch
            if isinstance(batch, pa.RecordBatch)
            else batch.to_record_batch()  # pragma: no cover
        )
        if len(rb) > remaining:
            rb = rb.slice(0, remaining)
        remaining -= len(rb)
        yield _coerce_batch_schema(rb)

    if remaining > 0:
        pytest.skip(
            f"Ray example dataset returned fewer rows than requested: missing {remaining} rows"
        )
