# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Upload manifest and add columns for the large image embedding UDF package.

Usage:
    export GENEVA_TABLE_NAME=my_table
    uv run python upload_manifest.py --bucket gs://bucket/path
"""

import logging

from image_udfs import Infer, decode, preprocess
from manifest import create_manifest

from geneva.manifest.uploader_cli import main_upload_workflow

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

DEFAULT_MANIFEST_NAME = "large-image-embedding-udfs-v1"


def get_columns() -> dict[str, callable]:
    return {
        "decoded": decode,
        "preprocessed": preprocess,
        "vit_logits": Infer(),
    }


if __name__ == "__main__":
    main_upload_workflow(
        get_columns_fn=get_columns,
        create_manifest_fn=create_manifest,
        description="Upload large image embedding UDF manifest and add columns",
        default_manifest_name=DEFAULT_MANIFEST_NAME,
        logger=_LOG,
    )
