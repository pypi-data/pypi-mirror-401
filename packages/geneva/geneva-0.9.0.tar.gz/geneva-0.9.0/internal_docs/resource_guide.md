# Geneva Resource Management Guide

This guide explains how Geneva manages compute resources when running UDF pipelines on Ray clusters. Understanding resource scheduling helps you right-size your cluster and troubleshoot common issues.

## How Resource Scheduling Works

### Ray's Logical Resource Model

Geneva uses Ray for distributed execution. Ray uses a **logical resource model** for scheduling:

- Resources (CPU, memory, GPU) are **requested**, not enforced
- Ray's scheduler places tasks/actors only when requested resources are available
- If resources aren't available, tasks queue indefinitely (no automatic timeout)
- Resources are "freed" when actors complete, not based on actual utilization

**Key insight**: Ray doesn't enforce limits. A task requesting 1 CPU can actually use 4 CPUs at runtime. The resource request is purely for scheduling decisions.

### What Consumes Resources in Geneva

When you run a backfill job, Geneva creates several types of actors:

| Component | Purpose | Typical Resources |
|-----------|---------|-------------------|
| **Driver task** | Orchestrates the backfill job | 0.1 CPU |
| **JobTracker actor** | Tracks job progress and checkpoints | 0.1 CPU, 128MB memory |
| **Applier actors** | Execute your UDF on batches | Based on UDF's `num_cpus`/`num_gpus` |
| **Writer actors** | Write results to storage | ~0.1 CPU, ~1GB memory each |
| **Queue actors** | Buffer data between stages | 0 CPU (no scheduling overhead) |

The number of each actor type depends on the `concurrency` parameter (default: 8). Generally, there is one writer and one queue per applier.

### Resource Calculation Example

For a backfill with `concurrency=4` and a UDF requesting 1 CPU:

```
Driver:    1 task  × 0.1 CPU   = 0.1 CPUs
JobTracker:1 actor × 0.1 CPU   = 0.1 CPUs
Appliers:  4 actors × 1 CPU    = 4 CPUs
Writers:   4 actors × 0.1 CPU  = 0.4 CPUs
Queues:    4 actors × 0 CPU    = 0 CPUs (no scheduling overhead)
                                 -------
Total CPU requested:             ~4.6 CPUs
Total memory:                    ~4 GB (128MB + 4×1GB)
```

If your cluster has fewer than ~5 CPUs available, some actors will wait indefinitely.

## Minimum Requirements for Jobs

### Cluster Sizing Guidelines

| Cluster Size | Head Node | Workers | Total Resources | Recommended Workload |
|--------------|-----------|---------|-----------------|---------------------|
| **Small** (Dev/CI) | 1 CPU, 3GB | 4 × 2 CPU, 4GB | 9 CPUs, 19GB | Small tables, concurrency=2 |
| **Medium** (Staging) | 2 CPU, 4GB | 4 × 4 CPU, 8GB | 18 CPUs, 36GB | Medium tables, concurrency=4 |
| **Large** (Production) | 4 CPU, 8GB | 8+ × 8 CPU, 16GB | 68+ CPUs, 136GB+ | Large tables, default concurrency |

### UDF Resource Configuration

Define resource requirements when creating your UDF:

```python
import geneva

# CPU-only UDF (default: 1 CPU)
@geneva.udf(num_cpus=1)
def my_cpu_udf(text: str) -> str:
    return text.upper()

# GPU UDF for ML inference
@geneva.udf(num_gpus=1, num_cpus=1)
def my_gpu_udf(image: bytes) -> list[float]:
    # Run model inference
    return model.predict(image)

# Lightweight UDF (use fractional CPU)
@geneva.udf(num_cpus=0.5)
def simple_transform(x: int) -> int:
    return x + 1
```

### Controlling Concurrency

The `concurrency` parameter controls how many applier actors run simultaneously:

```python
# Default concurrency (8 appliers)
table.backfill("output_column")

# Lower concurrency for resource-constrained clusters
table.backfill("output_column", concurrency=2)

# Higher concurrency for large clusters with many CPUs
table.backfill("output_column", concurrency=16)
```

**Rule of thumb**: Set concurrency so that `concurrency × UDF_cpus < available_cluster_cpus`

### Memory Considerations

- Each writer actor reserves ~1GB memory
- Higher concurrency means more writers, requiring more total memory
- GPU UDFs may need additional memory for model weights

For memory-intensive workloads:

```python
# Process fewer rows at once to reduce memory pressure
table.backfill("output_column", batch_size=16, concurrency=2)
```

## Troubleshooting Guide

### Symptom: Job Hangs at 0% Progress

**Cause**: Actors can't be scheduled due to insufficient resources.

**Diagnosis**:
1. Check if progress bar shows "Rows checkpointed: 0%"
2. Look for repeated log messages about waiting for resources

**Solutions**:
- Reduce `concurrency` parameter
- Reduce UDF's `num_cpus`/`num_gpus` requirements
- Add more workers to the cluster
- Use smaller batch sizes

```python
# Before: hangs on small cluster
table.backfill("col", concurrency=8)  # Needs 8+ CPUs

# After: works on small cluster
table.backfill("col", concurrency=2)  # Needs 2+ CPUs
```

### Symptom: Progress Stalls Partway Through

**Cause**: Some fragments completed but others can't get resources, or actors are crashing.

**Diagnosis**:
1. Note what percentage progress stopped at
2. Check logs for "Writer actor died" or similar errors
3. Look for OOM (out of memory) indicators

**Solutions**:
- Reduce concurrency to free up resources for writers
- Increase cluster memory if seeing OOM errors
- Check if specific fragments have unusually large data

### Symptom: Workers Not Starting (Kubernetes)

**Cause**: Worker pod resource requests exceed node capacity.

**Diagnosis**:
1. Check cluster logs for "Adding N node(s)" repeated messages
2. Worker pods stuck in Pending state
3. Kubernetes events show scheduling failures

**Solutions**:
- Reduce worker CPU/memory requests in cluster configuration
- Ensure worker specs fit on available node instance types
- Check node selector constraints match available nodes

### Symptom: Slow Performance Despite Available Resources

**Cause**: Configuration mismatch or I/O bottlenecks.

**Diagnosis**:
1. Check if concurrency is set too low
2. Monitor network/storage throughput
3. Check batch size settings

**Solutions**:
```python
# Increase parallelism if cluster has capacity
table.backfill("col", concurrency=8)

# Increase batch size for I/O-bound workloads
table.backfill("col", batch_size=64)

# For CPU-bound UDFs, use intra-applier concurrency
table.backfill("col", concurrency=4, intra_applier_concurrency=2)
```

### Symptom: Job Fails After Multiple Retries

**Cause**: Persistent resource issue or bug causing actor crashes.

**Diagnosis**:
1. Check for "max restarts exceeded" error messages
2. Look for the specific fragment that's failing
3. Check for memory errors or exceptions in logs

**Solutions**:
- Identify and fix the root cause (often OOM)
- Increase cluster resources
- Process problematic data separately with lower concurrency

## Quick Reference

### Backfill Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `concurrency` | 8 | Number of parallel UDF executors |
| `batch_size` | 32 | Rows processed per batch |
| `intra_applier_concurrency` | 1 | Parallelism within each applier |

### UDF Decorator Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_cpus` | 1 | CPUs requested per applier actor |
| `num_gpus` | 0 | GPUs requested per applier actor |
| `memory` | None | Memory in bytes (optional) |

### Common Patterns

```python
# Small cluster / CI environment
table.backfill("col", concurrency=2, batch_size=32)

# Medium cluster / staging
table.backfill("col", concurrency=4, batch_size=64)

# Large cluster / production
table.backfill("col", concurrency=8, batch_size=128)

# GPU workload
@geneva.udf(num_gpus=1)
def gpu_inference(data: bytes) -> list[float]:
    ...

table.backfill("embeddings", concurrency=4)  # 4 GPUs needed
```
