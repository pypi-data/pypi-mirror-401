# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

import geneva

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dataset import load_large_image_rows

if TYPE_CHECKING:
    from geneva.table import Table

DEFAULT_MANIFEST = "large-image-embedding-udfs-v1"
DERIVED_COLUMNS = ["decoded", "preprocessed", "vit_logits"]
CLUSTER_NAME_PREFIX = "e2e-large-image-embedding"

_UDF_DIR = _ROOT / "udfs" / "vit_image"


def upload_manifest(bucket: str, table_name: str, manifest_name: str) -> None:
    env = os.environ.copy()
    env["GENEVA_TABLE_NAME"] = table_name
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            "upload_manifest.py",
            "--bucket",
            bucket,
            "--manifest-name",
            manifest_name,
        ],
        cwd=str(_UDF_DIR),
        check=True,
        env=env,
    )


def cluster_name_for_slug(slug: str) -> str:
    return f"{CLUSTER_NAME_PREFIX}-{slug}"


def resolve_dataset_path(
    dataset_path: str, default_bucket: str | None
) -> tuple[str, str]:
    normalized = dataset_path.rstrip("/")
    if normalized.startswith(("gs://", "s3://")):
        bucket_path, _, table_name = normalized.rpartition("/")
        if not bucket_path or not table_name:
            raise ValueError(
                f"Dataset path must include a table name, got: {dataset_path}"
            )
        return bucket_path, table_name
    if "/" in normalized:
        raise ValueError(
            "Dataset path without gs:// or s3:// must be a table name only"
        )
    if default_bucket is None:
        raise ValueError(
            "Dataset path without bucket requires --bucket or --slug to derive a default"
        )
    return default_bucket, normalized


def drop_existing_columns(tbl: Table, columns: list[str]) -> list[str]:
    existing = [col for col in columns if col in tbl.schema.names]
    if existing:
        print(f"Dropping existing columns: {existing}")
        tbl.drop_columns(existing)
    return existing


def worker_replica_override(num_workers: int) -> dict[str, int]:
    if num_workers < 1:
        raise ValueError("num_workers must be >= 1")
    return {
        "replicas": num_workers,
        "minReplicas": num_workers,
        "maxReplicas": num_workers,
    }


def ensure_cluster(
    conn: geneva.Connection,
    csp: str,
    cluster_name: str,
    benchmark_mode: bool,
    num_workers: int | None,
) -> str:
    from geneva.cluster import K8sConfigMethod
    from geneva.cluster.builder import GenevaClusterBuilder, WorkerGroupBuilder

    head_selector = (
        {"geneva.lancedb.com/ray-head": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )
    if benchmark_mode:
        worker_selector = {"geneva-benchmark/ray-worker-cpu": "true"}
    else:
        worker_selector = (
            {"geneva.lancedb.com/ray-worker-cpu": "true"}
            if csp == "aws"
            else {"_PLACEHOLDER": "true"}
        )
    k8s_config_method = (
        K8sConfigMethod.LOCAL if csp == "gcp" else K8sConfigMethod.EKS_AUTH
    )
    service_account = "geneva-service-account"
    region = "us-central1" if csp == "gcp" else "us-east-1"

    builder = (
        GenevaClusterBuilder.create(cluster_name)
        .namespace("geneva")
        .config_method(k8s_config_method)
        .portforwarding(True)
        .head_group(
            service_account=service_account,
            cpus=1,
            memory="3Gi",
            image="rayproject/ray:2.44.0-py310",
            node_selector=head_selector,
        )
        .add_worker_group(
            WorkerGroupBuilder.cpu_worker(cpus=16, memory="16Gi")
            .image("rayproject/ray:2.44.0-py310")
            .service_account(service_account)
            .node_selector(worker_selector)
        )
    )

    if k8s_config_method == K8sConfigMethod.EKS_AUTH:
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    if num_workers is not None:
        worker_cfg = cluster.kuberay.worker_groups[0]
        worker_cfg.k8s_spec_override = worker_replica_override(num_workers)
    conn.define_cluster(cluster_name, cluster)
    return cluster_name


def default_bucket(csp: str, slug: str) -> str:
    if csp == "gcp":
        return f"gs://lancedb-lancedb-dev-us-central1/{slug}/data"
    if csp == "aws":
        return f"s3://geneva-integ-test-devland-us-east-1/{slug}/data"
    raise ValueError(f"Unsupported CSP: {csp}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Geneva benchmark equivalent of Ray large_image_embedding"
    )
    parser.add_argument("--csp", choices=["gcp", "aws"], default="gcp")
    parser.add_argument("--slug", default=None, help="Slug for bucket/cluster names")
    parser.add_argument(
        "--cluster-name",
        default=None,
        help="Override cluster name (defaults to e2e-large-image-embedding-{slug})",
    )
    parser.add_argument("--bucket", default=None, help="Override bucket path")
    parser.add_argument(
        "--dataset-path",
        default=None,
        help="Existing dataset path (gs://.../table or s3://.../table). Skips data write",
    )
    parser.add_argument("--num-images", type=int, default=200, help="Number of images")
    parser.add_argument("--batch-size", type=int, default=8, help="Backfill batch size")
    parser.add_argument(
        "--benchmark-mode",
        action="store_true",
        help="Use benchmark worker node selector",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=None,
        help="Fixed number of Ray workers (replicas/min/max)",
    )
    parser.add_argument(
        "--manifest-name",
        default=DEFAULT_MANIFEST,
        help="Manifest name to use when backfilling",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slug = args.slug or str(uuid.uuid4().hex[:8])
    bucket = args.bucket or default_bucket(args.csp, slug)
    cluster_name = args.cluster_name or cluster_name_for_slug(slug)

    if args.dataset_path:
        dataset_bucket, table_name = resolve_dataset_path(args.dataset_path, bucket)
        if args.bucket and dataset_bucket != args.bucket:
            print(
                f"Dataset path bucket {dataset_bucket} overrides --bucket {args.bucket}"
            )
        bucket = dataset_bucket
        conn = geneva.connect(bucket)
        tbl = conn.open_table(table_name)
        print(f"Using existing table {table_name} in {bucket} with {len(tbl)} rows")
    else:
        conn = geneva.connect(bucket)
        table_name = f"large_image_embedding_{uuid.uuid4().hex}"

        first = True
        for batch in load_large_image_rows(num_images=args.num_images):
            if first:
                tbl = conn.create_table(table_name, batch, mode="overwrite")
                first = False
            else:
                tbl.add(batch)

        if first:
            raise RuntimeError("No image rows produced; cannot run benchmark")

        print(f"Created table {table_name} in {bucket} with {len(tbl)} rows")

    drop_existing_columns(tbl, DERIVED_COLUMNS)

    upload_manifest(bucket, table_name, args.manifest_name)
    tbl = conn.open_table(table_name)

    cluster_name = ensure_cluster(
        conn,
        args.csp,
        cluster_name,
        args.benchmark_mode,
        args.num_workers,
    )

    backfill_concurrency = (
        args.num_workers * 2 if args.num_workers is not None else 8
    )

    start = time.time()
    print(f"num_workers={args.num_workers}, backfill_concurrency={backfill_concurrency}")
    with conn.context(cluster=cluster_name, manifest=args.manifest_name):
        for col in DERIVED_COLUMNS:
            tbl.backfill(
                col,
                batch_size=args.batch_size,
                concurrency=backfill_concurrency,
            )

    runtime = time.time() - start
    print(f"Runtime: {runtime:.2f}s")
    print(f"Wrote results to {bucket}/{table_name} using cluster {cluster_name}")


if __name__ == "__main__":
    main()
