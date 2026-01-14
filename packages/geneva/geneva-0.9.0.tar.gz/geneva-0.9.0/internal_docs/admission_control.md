# Geneva Admission Control

This document describes how Geneva validates resource availability before starting jobs, preventing jobs from hanging indefinitely when resources aren't available.

> **Note on Experimental APIs:** Parameters starting with `_` (underscore) are experimental and subject to change without notice. This includes `_admission_check` and `_admission_strict`.

## The Problem

When a Geneva job (backfill or materialized view refresh) requires more resources than the cluster has, Ray will queue the job actors indefinitely. This results in:

- Jobs stuck at 0% progress with no clear error message
- Wasted time debugging cluster configuration
- Confusion about whether the job is running or waiting

## Solution Overview

Geneva now performs **admission control** before starting jobs:

1. **Calculate required resources** based on UDF and concurrency settings
2. **Query cluster capacity** (total and available resources)
3. **Decide**: Allow, warn, or reject the job

Admission control applies to:
- **Backfill jobs** (`table.backfill()`)
- **Materialized view refreshes** (`mv.refresh()`) when the view has UDFs

### Decision Outcomes

| Decision | When | What Happens |
|----------|------|--------------|
| **ALLOW** | Resources available | Job starts immediately |
| **WARN** | Resources exist but busy | Job starts, warning logged about potential wait |
| **REJECT** | Resources will never be available | Job fails fast with clear error message |

## What Resources Are Checked

A backfill or matview refresh job requires resources for several components:

| Component | CPU | GPU | Memory | Count |
|-----------|-----|-----|--------|-------|
| Driver task | 0.1 | - | - | 1 |
| JobTracker | 0.1 | - | 128MB | 1 |
| Applier actors | UDF setting | UDF setting | UDF setting | `concurrency` |
| Writer actors | 0.1 | - | 1GB | `concurrency` |
| Queue actors | 0 | - | 0 | `concurrency` |

### Quick Estimation

For a job with `concurrency=N` and a UDF requesting `C` CPUs and `G` GPUs:

```
Total CPUs needed ≈ N × C + N × 0.1 + 0.2
Total GPUs needed = N × G
Total memory ≈ N × (UDF_memory + 1GB) + 128MB
```

**Example**: `concurrency=8`, UDF with `num_cpus=1`, `num_gpus=1`:
- CPUs: 8 × 1 + 8 × 0.1 + 0.2 ≈ **9.0 CPUs**
- GPUs: 8 × 1 = **8 GPUs**

## Per-Node Resource Validation

Beyond checking total cluster capacity, admission control validates that at least one node can satisfy **all** UDF requirements simultaneously. This is critical for heterogeneous clusters.

### The Heterogeneous Cluster Problem

Consider a cluster with two types of nodes:
- **Node A**: 8 CPUs, 4GB memory
- **Node B**: 4 CPUs, 8GB memory

If a UDF requires 8 CPUs **and** 8GB memory:
- Total cluster CPUs: 12 (sufficient)
- Total cluster memory: 12GB (sufficient)
- Max CPUs per node: 8 (sufficient)
- Max memory per node: 8GB (sufficient)

**But no single node can run the UDF!** Node A lacks memory, Node B lacks CPUs.

### How It Works

Admission control tracks resources for each node/worker group and checks if ANY node can satisfy ALL requirements:

```python
# Checks if any node can fit: udf_cpus AND udf_gpus AND udf_memory
cluster.any_node_can_fit(udf_cpus=8.0, udf_gpus=0.0, udf_memory=8*1024*1024*1024)
```

### Error Message

```
ResourcesUnavailableError: UDF requires 8.0 CPUs + 8.0GB memory but no single
node can satisfy all requirements. Reduce UDF resource requirements or add
nodes with sufficient combined resources.
```

## Static/Direct Ray Clusters

For clusters started with `ray start` or a fixed Ray cluster:

### When Jobs Are Rejected

1. **GPU job on CPU-only cluster**: Job requires GPUs but no nodes have GPUs
2. **More GPUs than cluster has**: e.g., 8 GPU job on 4-GPU cluster
3. **More CPUs than cluster has**: e.g., 20 CPU job on 8-CPU cluster
4. **No node can fit UDF**: UDF requires combination of resources no single node has

### Example Error Messages

```
ResourcesUnavailableError: Job requires 8.0 GPUs but cluster has none.
Either remove GPU requirement from UDF or add GPU nodes to cluster.

ResourcesUnavailableError: Job requires 8.0 GPUs but cluster only has 4.0.
Reduce concurrency to 4 or fewer.

ResourcesUnavailableError: Job requires 20.0 CPUs but cluster only has 8.0.
Reduce concurrency or UDF num_cpus.

ResourcesUnavailableError: UDF requires 8.0 CPUs + 8.0GB memory but no single
node can satisfy all requirements. Reduce UDF resource requirements or add
nodes with sufficient combined resources.
```

### When Jobs Get Warnings

If total resources exist but are currently in use by other jobs:

```
WARNING: Job needs 4.0 GPUs but only 2.0 currently available. Job will wait.
```

### How to Fix

| Issue | Solution |
|-------|----------|
| Need more GPUs | Add GPU nodes or reduce `concurrency` |
| Need more CPUs | Add worker nodes or reduce `concurrency` / `num_cpus` |
| No node can fit UDF | Add larger nodes or reduce UDF requirements |
| Resources busy | Wait for other jobs, or reduce concurrency |

## KubeRay Dynamic Clusters

For Kubernetes clusters managed by the KubeRay operator:

### Key Difference: Clusters Can Scale

KubeRay clusters have `minReplicas` and `maxReplicas` settings. Admission control checks what's **possible at max scale**, not just what's running now.

### When Jobs Are Rejected

1. **GPU job on non-GPU cluster**: No worker groups have GPU resources
2. **More resources than max scale allows**: Even at `maxReplicas`, not enough capacity
3. **No worker group can fit UDF**: UDF requires combination of resources no worker group has

### Example Error Messages

```
ResourcesUnavailableError: Job requires 8.0 GPUs but cluster has no GPU
worker groups configured. Add a GPU worker group to the RayCluster spec.

ResourcesUnavailableError: Job requires 16.0 GPUs but cluster can only
scale to 8.0 GPUs (maxReplicas limit). Reduce concurrency or increase
maxReplicas for GPU worker group.

ResourcesUnavailableError: UDF requires 8.0 CPUs + 8.0GB memory but no
worker group can satisfy all requirements. Reduce UDF resource requirements
or configure worker nodes with sufficient combined resources.
```

### When Jobs Get Warnings

If cluster needs to scale up:

```
WARNING: Cluster will need to scale up (currently 2/8 workers).
Job may wait for nodes to provision.
```

### How to Fix

| Issue | Solution |
|-------|----------|
| No GPU worker group | Add `workerGroupSpec` with GPU resources |
| maxReplicas too low | Increase `maxReplicas` in cluster spec |
| No worker group can fit UDF | Add worker group with larger nodes or reduce UDF requirements |
| Nodes provisioning slow | Pre-warm cluster or wait |

## Configuration

### Controlling Admission Behavior

```python
# Default: Strict admission control (fail fast)
table.backfill("output_col", concurrency=8)

# Disable admission check entirely
table.backfill("output_col", concurrency=8, _admission_check=False)

# Run admission check but only warn (don't fail)
table.backfill("output_col", concurrency=8, _admission_strict=False)
```

The same parameters work for materialized view refreshes:

```python
# Default: Strict admission control
mv.refresh()

# Custom concurrency with admission control
mv.refresh(concurrency=16, intra_applier_concurrency=2)

# Disable admission check for matview refresh
mv.refresh(_admission_check=False)

# Run admission check but only warn
mv.refresh(_admission_strict=False)
```

### Configuration

Admission control settings can be configured via config files, pyproject.toml, or environment variables.

**pyproject.toml** (recommended):

```toml
[geneva.geneva_admission]
check = false
strict = false
timeout = 5.0
```

**Config files** (`.config/geneva.yaml`, `.config/geneva.json`, `.config/geneva.toml`):

```yaml
geneva_admission:
  check: false
  strict: false
  timeout: 5.0
```

**Environment Variables:**

Uses `__` (double underscore) as separator between config section and field name.

| Variable | Default | Description |
|----------|---------|-------------|
| `GENEVA_ADMISSION__CHECK` | `true` | If true, enable admission control; if false, skip all checks |
| `GENEVA_ADMISSION__STRICT` | `true` | If true, reject the job on failure. If false, just warn. |
| `GENEVA_ADMISSION__TIMEOUT` | `3.0` | Timeout in seconds for Ray API calls |

## Troubleshooting

### "Job requires GPUs but cluster has none"

Your UDF has `num_gpus > 0` but the cluster has no GPUs.

**Check your UDF:**
```python
@geneva.udf(num_gpus=1)  # This requires GPUs
def my_udf(x): ...
```

**Fix options:**
1. Remove GPU requirement if not needed: `@geneva.udf(num_gpus=0)`
2. Add GPU nodes to your cluster

### "Job requires X GPUs but cluster only has Y"

You're requesting more GPU parallelism than the cluster supports.

**Fix:**
```python
# Before: needs 8 GPUs
table.backfill("col", concurrency=8)

# After: needs 4 GPUs
table.backfill("col", concurrency=4)
```

### "No single node can satisfy all requirements"

Your UDF requires a combination of resources (CPU + GPU + memory) that no single node has. This commonly happens with heterogeneous clusters.

**Example scenario:**
- Node A: 8 CPUs, 4GB memory
- Node B: 4 CPUs, 8GB memory
- UDF requires: 8 CPUs AND 8GB memory
- Result: Rejected (no single node has both)

**Fix options:**

1. **Reduce UDF requirements:**
```python
# Before: needs 8 CPUs + 8GB
@geneva.udf(num_cpus=8, memory=8*1024*1024*1024)
def my_udf(x): ...

# After: fits on Node A (8 CPUs + 4GB)
@geneva.udf(num_cpus=8, memory=4*1024*1024*1024)
def my_udf(x): ...
```

2. **Add larger nodes** that can satisfy all requirements together

3. **Use homogeneous clusters** where all nodes have the same resources

### Job starts but hangs at low %

If admission control passes but job still hangs:

1. Check Ray dashboard for pending actors
2. Look for memory pressure (OOM kills)
3. Check if writers/queues are stuck

### Matview refresh fails with resource errors

When refreshing a materialized view with UDFs, admission control validates
resources for each UDF. If your matview has multiple UDFs with different
resource requirements, all must pass validation.

> **Note on multi-UDF checking:** Admission control currently checks each UDF
> independently. Since UDFs run sequentially (not in parallel), only the most
> demanding UDF's resources are actually needed at runtime. This means the
> check is **conservative** - it may reject jobs that would run fine. If you
> encounter this, use `_admission_check=False` or `_admission_strict=False`.

**Check your matview's UDFs:**
```python
# List UDFs in the matview query (inspect the source query definition)
# Each UDF's num_cpus, num_gpus, memory settings affect admission control
```

**Fix options:**
1. Reduce concurrency: `mv.refresh(concurrency=4)`
2. Disable admission check: `mv.refresh(_admission_check=False)`
3. Use non-strict mode: `mv.refresh(_admission_strict=False)`

### How to check cluster resources

```python
import ray

# Connect to cluster
ray.init(address="auto")

# See total resources
print(ray.cluster_resources())

# See available resources
print(ray.available_resources())

# See per-node breakdown
for node in ray.nodes():
    if node["Alive"]:
        print(f"Node {node['NodeID'][:8]}: {node['Resources']}")
```

## Implementation Details

Admission control is implemented in `geneva.runners.ray.admission`:

- `calculate_job_resources()` - Compute resources needed for a job
- `get_cluster_resources()` - Query Ray/KubeRay for capacity
- `check_admission()` - Make allow/warn/reject decision
- `validate_admission()` - High-level validation function used by jobs

Integration points in `pipeline.py`:
- `backfill_async()` - Admission control for backfill jobs
- `run_ray_copy_table()` - Admission control for matview refresh jobs

For matview refreshes, admission control validates each UDF defined in the
materialized view query. If a matview has no UDFs (just column selection or
filtering), admission control is skipped.
