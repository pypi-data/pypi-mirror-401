# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E fixtures for the large image embedding suite.

This suite mirrors e2e/document_embedding:
  - lightweight test drivers
  - heavy ML deps isolated in udfs/vit_image (uploaded via manifest)
"""

import contextlib
import logging
import os
import random
import subprocess
import sys
import uuid
import warnings
from pathlib import Path

import kubernetes
import pytest
from dataset import load_large_image_rows

from geneva.cluster import K8sConfigMethod
from geneva.cluster.builder import GenevaClusterBuilder, WorkerGroupBuilder

SYNC_CMD = ["uv", "sync", "--index-strategy", "unsafe-best-match"]

# Make UDF modules importable when tests unpickle them
_udfs_dir = Path(__file__).parent / "udfs"
for udf_package in ["vit_image"]:
    udf_path = _udfs_dir / udf_package
    if udf_path.exists() and str(udf_path) not in sys.path:
        sys.path.insert(0, str(udf_path))

with contextlib.suppress(kubernetes.config.config_exception.ConfigException):
    kubernetes.config.load_kube_config()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
warnings.filterwarnings(
    "ignore", "Using port forwarding for Ray cluster is not recommended for production"
)

_LOG = logging.getLogger(__name__)
_MANIFESTS_UPLOADED = False
DEFAULT_MANIFEST_NAME = "large-image-embedding-udfs-v1"


def _upload_all_manifests(bucket_path: str) -> None:
    import textwrap

    _LOG.info("Uploading UDF manifests to %s", bucket_path)

    udfs_dir = Path(__file__).parent / "udfs"
    udf_packages = ["vit_image"]

    for udf_name in udf_packages:
        udf_dir = udfs_dir / udf_name
        upload_script = udf_dir / "upload_manifest.py"

        if not upload_script.exists():
            _LOG.warning("Upload script missing for %s; skipping", udf_name)
            continue

        _LOG.info("Syncing dependencies for '%s'", udf_name)
        sync_result = subprocess.run(
            SYNC_CMD,
            cwd=str(udf_dir),
            capture_output=True,
            text=True,
        )
        if sync_result.returncode != 0:
            _LOG.error("Dependency sync failed for %s", udf_name)
            if sync_result.stderr:
                _LOG.error(textwrap.indent(sync_result.stderr, "    "))
            raise RuntimeError(f"uv sync failed for {udf_name}")

        _LOG.info("Uploading manifest for '%s'", udf_name)
        result = subprocess.run(
            ["uv", "run", "python", "upload_manifest.py", "--bucket", bucket_path],
            cwd=str(udf_dir),
            capture_output=True,
            text=True,
            env=os.environ.copy(),
        )

        if result.stdout:
            _LOG.info(textwrap.indent(result.stdout, f"[{udf_name}] "))
        if result.stderr:
            _LOG.warning(textwrap.indent(result.stderr, f"[{udf_name}] "))

        if result.returncode != 0:
            raise RuntimeError(f"Manifest upload failed for {udf_name}")

        _LOG.info("✓ Uploaded manifest for '%s'", udf_name)


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--csp",
        action="store",
        default="gcp",
        choices=["gcp", "aws"],
        help="Target cloud service provider",
    )
    parser.addoption(
        "--test-slug",
        action="store",
        default=None,
        help="Slug to namespace buckets/resources",
    )
    parser.addoption(
        "--bucket-path",
        action="store",
        default=None,
        help="Override bucket path (gs://... or s3://...)",
    )
    parser.addoption(
        "--num-images",
        action="store",
        type=int,
        default=20,
        help="Number of images to process",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        type=int,
        default=4,
        help="Backfill batch size",
    )


@pytest.fixture(scope="session")
def csp(request) -> str:
    return request.config.getoption("--csp")


@pytest.fixture(scope="session")
def slug(request) -> str:
    return request.config.getoption("--test-slug") or str(random.randint(0, 10000))


@pytest.fixture(scope="session")
def geneva_test_bucket(request, slug, csp) -> str:
    from geneva.config import override_config_kv

    bucket_path = request.config.getoption("--bucket-path")
    if not bucket_path:
        if csp == "gcp":
            bucket_path = f"gs://lancedb-lancedb-dev-us-central1/{slug}/data"
        elif csp == "aws":
            bucket_path = f"s3://geneva-integ-test-devland-us-east-1/{slug}/data"
        else:
            raise ValueError(f"Unsupported CSP: {csp}")
        _LOG.info("Using default bucket path: %s", bucket_path)
    else:
        _LOG.info("Using provided bucket path: %s", bucket_path)

    override_config_kv(
        {
            "job.checkpoint.mode": "object_store",
            "uploader.upload_dir": f"{bucket_path}/zips",
            "job.checkpoint.object_store.path": f"{bucket_path}/checkpoints",
        }
    )

    return bucket_path


@pytest.fixture(scope="session")
def geneva_k8s_service_account(csp: str) -> str:
    return "geneva-service-account"


@pytest.fixture(scope="session")
def region(csp: str) -> str:
    return "us-east-1" if csp == "aws" else "us-central1"


@pytest.fixture(scope="session")
def k8s_config_method(csp: str) -> K8sConfigMethod:
    return K8sConfigMethod.EKS_AUTH if csp == "aws" else K8sConfigMethod.LOCAL


@pytest.fixture(scope="session")
def k8s_namespace(csp: str) -> str:
    return "geneva"


@pytest.fixture(scope="session")
def k8s_cluster_name(csp: str) -> str:
    return "lancedb"


@pytest.fixture(scope="session")
def head_node_selector(csp: str) -> dict:
    return (
        {"geneva.lancedb.com/ray-head": "true"}
    )


@pytest.fixture(scope="session")
def worker_node_selector(csp: str) -> dict:
    return (
        {"geneva.lancedb.com/ray-worker-cpu": "true"}
    )


@pytest.fixture(scope="session")
def num_images(request) -> int:
    return request.config.getoption("--num-images")


@pytest.fixture(scope="session")
def batch_size(request) -> int:
    return request.config.getoption("--batch-size")


@pytest.fixture(scope="session")
def manifest_name() -> str:
    return DEFAULT_MANIFEST_NAME


@pytest.fixture(scope="session")
def image_table(geneva_test_bucket: str, num_images: int) -> tuple:
    import geneva

    conn = geneva.connect(geneva_test_bucket)
    table_name = f"large_image_embedding_{uuid.uuid4().hex}"

    first = True
    for batch in load_large_image_rows(num_images=num_images):
        if first:
            tbl = conn.create_table(table_name, batch, mode="overwrite")
            first = False
        else:
            tbl.add(batch)

    if first:
        pytest.skip("No image rows produced; cannot build test table")

    _LOG.info(
        "Created test table '%s' with %s rows and columns %s",
        table_name,
        len(tbl),
        tbl.schema.names,
    )

    os.environ["GENEVA_TABLE_NAME"] = table_name
    _LOG.info("Set GENEVA_TABLE_NAME=%s", table_name)

    global _MANIFESTS_UPLOADED
    if not _MANIFESTS_UPLOADED:
        _upload_all_manifests(geneva_test_bucket)
        _MANIFESTS_UPLOADED = True
        tbl = conn.open_table(table_name)
        _LOG.info("Schema after manifest upload: %s", tbl.schema.names)

    return conn, tbl, table_name


@pytest.fixture
def standard_cluster(
    image_table: tuple,
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> str:
    conn, _, _ = image_table
    cluster_name = "e2e-large-image-embedding-cluster"

    try:
        kubernetes.config.list_kube_config_contexts()
    except Exception:
        pytest.skip("Kubernetes config not available; skipping cluster-backed tests")

    builder = (
        GenevaClusterBuilder.create(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .portforwarding(True)
        .head_group(
            service_account=geneva_k8s_service_account,
            cpus=1,
            memory="3Gi",
            image="rayproject/ray:2.44.0-py310",
            node_selector=head_node_selector,
        )
        .add_worker_group(
            WorkerGroupBuilder.cpu_worker(cpus=4, memory="8Gi")
            .image("rayproject/ray:2.44.0-py310")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
        )
    )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    conn.define_cluster(cluster_name, cluster)
    _LOG.info("Defined cluster '%s'", cluster_name)
    return cluster_name
