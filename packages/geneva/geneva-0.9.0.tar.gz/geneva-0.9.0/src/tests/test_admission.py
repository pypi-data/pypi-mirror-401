# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for admission control."""

from unittest.mock import MagicMock, patch

import pyarrow as pa
import pytest

from geneva.runners.ray.admission import (
    AdmissionDecision,
    ClusterResources,
    JobResources,
    NodeCapacity,
    _check_kuberay_admission,
    _check_static_admission,
    _is_kuberay_cluster,
    calculate_job_resources,
    check_admission,
)
from geneva.transformer import UDF
from geneva.utils.ray import GENEVA_AUTOSCALING_RESOURCE


def make_udf(
    num_cpus: float = 1.0,
    num_gpus: float = 0.0,
    memory: int | None = None,
) -> UDF:
    """Create a simple UDF for testing."""

    def identity(x: str) -> str:
        return x

    return UDF(
        func=identity,
        num_cpus=num_cpus,
        num_gpus=num_gpus,
        memory=memory,
        data_type=pa.string(),
    )


class TestCalculateJobResources:
    """Tests for calculate_job_resources."""

    def test_cpu_only_udf(self) -> None:
        udf = make_udf(num_cpus=1.0, num_gpus=0.0)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_cpus == 4.0
        assert resources.applier_gpus == 0.0
        assert resources.concurrency == 4
        assert resources.udf_cpus == 1.0
        assert resources.udf_gpus == 0.0
        # Overhead includes driver (0.1), jobtracker (0.1), and writers (0.1 each)
        # Note: queues use 0 CPU and 0 memory
        assert resources.overhead_cpus == pytest.approx(0.6)

    def test_gpu_udf(self) -> None:
        udf = make_udf(num_cpus=1.0, num_gpus=1.0)
        resources = calculate_job_resources(udf, concurrency=8)

        assert resources.applier_cpus == 8.0
        assert resources.applier_gpus == 8.0
        assert resources.total_gpus == 8.0
        assert resources.udf_gpus == 1.0

    def test_fractional_gpu(self) -> None:
        udf = make_udf(num_cpus=0.5, num_gpus=0.5)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_cpus == 2.0
        assert resources.applier_gpus == 2.0
        assert resources.total_gpus == 2.0

    def test_intra_applier_concurrency(self) -> None:
        udf = make_udf(num_cpus=1.0)
        resources = calculate_job_resources(
            udf, concurrency=4, intra_applier_concurrency=2
        )

        assert resources.applier_cpus == 8.0
        assert resources.udf_cpus == 2.0

    def test_with_memory(self) -> None:
        udf = make_udf(num_cpus=1.0, memory=1024 * 1024 * 1024)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_memory == 4 * 1024 * 1024 * 1024

    def test_string_representation(self) -> None:
        udf = make_udf(num_cpus=2.0, num_gpus=1.0)
        resources = calculate_job_resources(udf, concurrency=4)

        s = str(resources)
        assert "cpus=" in s
        assert "gpus=" in s
        assert "concurrency=4" in s


class TestCheckStaticAdmission:
    """Tests for static cluster admission."""

    def test_allow_sufficient_resources(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=1024 * 1024 * 128,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW
        assert "available" in message.lower()

    def test_reject_gpu_on_cpu_cluster(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "GPUs but cluster has none" in message

    def test_reject_more_gpus_than_available(self) -> None:
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=8.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=8,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=4.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=4.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "Reduce concurrency to 4" in message

    def test_reject_more_cpus_than_available(self) -> None:
        job = JobResources(
            applier_cpus=16.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=4.0,
            overhead_memory=0,
            concurrency=16,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "CPUs but cluster only has" in message

    def test_warn_resources_busy(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=2.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW_WITH_WARNING
        assert "currently available" in message

    def test_reject_udf_cpus_exceed_node(self) -> None:
        """Test that UDF requiring more CPUs than any node has is rejected."""
        # UDF needs 8 CPUs but largest node only has 4 CPUs
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=8.0,
            udf_gpus=0.0,
        )
        # 5 nodes × 4 CPUs = 20 CPUs total, but max per node is 4
        cluster = ClusterResources(
            total_cpus=20.0,
            total_gpus=0.0,
            total_memory=20 * 1024 * 1024 * 1024,
            available_cpus=20.0,
            available_gpus=0.0,
            available_memory=20 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message

    def test_reject_udf_memory_exceeds_node(self) -> None:
        """Test that UDF requiring more memory than any node has is rejected."""
        # UDF needs 8GB but largest node only has 4GB
        job = JobResources(
            applier_cpus=1.0,
            applier_gpus=0.0,
            applier_memory=8 * 1024 * 1024 * 1024,
            overhead_cpus=0.2,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=1.0,
            udf_gpus=0.0,
            udf_memory=8 * 1024 * 1024 * 1024,
        )
        # 5 nodes × 4GB = 20GB total, but max per node is 4GB
        cluster = ClusterResources(
            total_cpus=20.0,
            total_gpus=0.0,
            total_memory=20 * 1024 * 1024 * 1024,
            available_cpus=20.0,
            available_gpus=0.0,
            available_memory=20 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message

    def test_reject_heterogeneous_nodes_no_combined_fit(self) -> None:
        """Test that heterogeneous nodes are correctly validated.

        Scenario: 4GB/8CPU nodes + 8GB/4CPU nodes, UDF needs 8GB + 8CPU.
        No single node can satisfy both requirements even though the cluster
        has enough total resources and each requirement is individually met.
        """
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=0.0,
            applier_memory=8 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=8.0,
            udf_gpus=0.0,
            udf_memory=8 * 1024 * 1024 * 1024,
        )
        # Heterogeneous cluster:
        # - Node A: 8 CPUs, 4GB memory (can't fit 8GB memory requirement)
        # - Node B: 4 CPUs, 8GB memory (can't fit 8 CPU requirement)
        cluster = ClusterResources(
            total_cpus=12.0,  # 8 + 4
            total_gpus=0.0,
            total_memory=12 * 1024 * 1024 * 1024,  # 4 + 8
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=12 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=8 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message
        assert "8.0 CPUs" in message
        assert "memory" in message  # Memory value depends on GiB to GB conversion

    def test_allow_heterogeneous_nodes_with_fit(self) -> None:
        """Test that heterogeneous nodes allow jobs when one node can fit."""
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=4 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=4.0,
            udf_gpus=0.0,
            udf_memory=4 * 1024 * 1024 * 1024,
        )
        # Heterogeneous cluster with one node that can fit:
        # - Node A: 8 CPUs, 4GB memory (can fit 4 CPU + 4GB)
        # - Node B: 4 CPUs, 8GB memory (can also fit 4 CPU + 4GB)
        cluster = ClusterResources(
            total_cpus=12.0,
            total_gpus=0.0,
            total_memory=12 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=12 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=8 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW


class TestCheckKuberayAdmission:
    """Tests for KubeRay cluster admission."""

    def test_allow_within_max_scale(self) -> None:
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=8.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=8,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=4.0,
            total_gpus=4.0,
            total_memory=16 * 1024 * 1024 * 1024,
            available_cpus=4.0,
            available_gpus=4.0,
            available_memory=16 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=32.0,
            max_scale_gpus=16.0,
            max_scale_memory=128 * 1024 * 1024 * 1024,
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW_WITH_WARNING
        assert "scale up" in message

    def test_reject_gpu_on_non_gpu_cluster(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=16.0,
            available_gpus=0.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=64.0,
            max_scale_gpus=0.0,
            max_scale_memory=256 * 1024 * 1024 * 1024,
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no GPU worker groups" in message

    def test_reject_exceeds_max_scale(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=16.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=16,
            udf_cpus=0.25,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=4.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=4.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=64.0,
            max_scale_gpus=8.0,
            max_scale_memory=256 * 1024 * 1024 * 1024,
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "maxReplicas" in message


class TestCheckAdmission:
    """Tests for the main check_admission function."""

    def test_routes_to_static_check(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            is_kuberay=False,
        )

        decision, _ = check_admission(job, cluster)
        assert decision == AdmissionDecision.ALLOW

    def test_routes_to_kuberay_check(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=0.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=32.0,
            max_scale_gpus=0.0,
            max_scale_memory=128 * 1024 * 1024 * 1024,
        )

        decision, message = check_admission(job, cluster)
        assert decision == AdmissionDecision.REJECT
        assert "GPU" in message


class TestIsKuberayCluster:
    """Tests for _is_kuberay_cluster detection."""

    def test_detects_geneva_autoscaling_resource(self) -> None:
        """Test detection via geneva_autoscaling resource."""
        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission.ray.cluster_resources",
                return_value={GENEVA_AUTOSCALING_RESOURCE: 1.0, "CPU": 8.0},
            ),
        ):
            assert _is_kuberay_cluster() is True

    def test_not_kuberay_without_resource(self) -> None:
        """Test that cluster is not detected as KubeRay without the resource."""
        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission.ray.cluster_resources",
                return_value={"CPU": 8.0, "GPU": 4.0},
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context", return_value=None
            ),
        ):
            assert _is_kuberay_cluster() is False

    def test_fallback_to_context(self) -> None:
        """Test fallback to Geneva context when Ray resource check fails."""
        mock_ctx = MagicMock()
        mock_ctx.namespace = "test-ns"
        mock_ctx.name = "test-cluster"
        with (
            patch(
                "geneva.runners.ray.admission.ray.is_initialized", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context",
                return_value=mock_ctx,
            ),
        ):
            assert _is_kuberay_cluster() is True

    def test_not_kuberay_without_context(self) -> None:
        """Test that cluster is not detected as KubeRay without context."""
        with (
            patch(
                "geneva.runners.ray.admission.ray.is_initialized", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context", return_value=None
            ),
        ):
            assert _is_kuberay_cluster() is False
