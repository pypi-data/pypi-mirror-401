# Backfills Architecture

**Audience:** Sales engineers, support engineers, architects, and new contributors

**Purpose:** Understand how Geneva backfills work at a conceptual level to support customers, debug issues, and contribute to the codebase.

---

## What are Backfills?

Backfills are the process of computing missing values for a column in a table using a User-Defined Function (UDF). Instead of reprocessing an entire table from scratch, backfills intelligently populate values for rows that haven't been computed yet.

**Business Value:**
- **Lazy Computation:** Define columns upfront, compute values later when resources are available
- **Incremental Processing:** Only compute values for new or unprocessed rows
- **Fault Tolerance:** Resume failed jobs from the last checkpoint, not from the beginning
- **Selective Updates:** Use SQL filters to backfill only specific rows

**Geneva's Approach:**
Geneva backfills are built on Lance tables with support for:
- Zero-cost data evolution (add column schema changes without rewriting data)
- Distributed execution via Ray workers
- Checkpoint-based fault tolerance and deduplication
- Selective backfill with WHERE clauses
- Partial commits to show progress before job completion

---

## Current Limitations (v0.8.x and earlier)

> **Warning:** Backfill is optimized for append-only datasets. Be aware of these limitations:

| Operation | Behavior | Impact |
|-----------|----------|--------|
| **Append** | Works as expected | New fragments are processed, existing checkpoints preserved |
| **Merge/Upsert** | Results may not be captured | Rows modified via merge may not trigger reprocessing |
| **Compaction** | Causes reprocessing | Compaction creates new fragments, invalidating existing checkpoints - rows will be reprocessed |

**Recommendations:**
- For append-only workloads: Backfill works reliably with checkpoint-based incremental processing
- For tables with frequent updates: Consider running backfill after update batches complete
- For compacted tables: Expect full reprocessing after compaction operations

---

## High-Level Architecture

**Key Insight:** Unlike materialized views, backfills update the **same table** in place. The column exists in the schema with NULL values, and backfill computes and writes the actual values.

```
┌─────────────────────────────────────────────────────────────────┐
│                        BACKFILL SYSTEM                           │
└─────────────────────────────────────────────────────────────────┘

                    ┌───────────────────────────────┐
                    │        SAME TABLE             │
                    │         (Lance DB)            │
                    │                               │
                    │  ┌─────────────────────────┐  │
                    │  │ Fragment 0              │  │
                    │  │  col_a: [1, 2, 3]       │  │
                    │  │  embedding: [NULL, ...]─┼──┼─── Before: NULL values
                    │  ├─────────────────────────┤  │
                    │  │ Fragment 1              │  │
                    │  │  col_a: [4, 5, 6]       │  │
                    │  │  embedding: [NULL, ...]─┼──┼─── After: Computed values
                    │  ├─────────────────────────┤  │
                    │  │ Fragment 2              │  │
                    │  │  col_a: [7, 8, 9]       │  │
                    │  │  embedding: [NULL, ...] │  │
                    │  └─────────────────────────┘  │
                    └───────────────┬───────────────┘
                                    │
                 ┌──────────────────┴──────────────────┐
                 │                                     │
                 ▼ 1. Read rows                        ▲ 4. Write computed
                                                         column values
┌─────────────────────────────────────────────────────────────────┐
│                      RAY PROCESSING CLUSTER                      │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Worker 1   │  │   Worker 2   │  │   Worker 3   │            │
│  │              │  │              │  │              │            │
│  │  Apply UDF   │  │  Apply UDF   │  │  Apply UDF   │            │
│  │   Process    │  │   Process    │  │   Process    │            │
│  │   Batches    │  │   Batches    │  │   Batches    │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           │ 2. Store checkpoints                 │
│                           ▼                                      │
│                   ┌─────────────────┐                            │
│                   │ CHECKPOINT STORE│                            │
│                   │                 │                            │
│                   │  Deduplication  │                            │
│                   │  Progress Track │                            │
│                   │  Fault Tolerant │                            │
│                   └────────┬────────┘                            │
│                            │ 3. Fragment Writers read ckpts      │
└────────────────────────────┼────────────────────────────────────┘
                             ▼
                     Fragment Writers
                     (commit to same table)
```

### Key Components

1. **Table**: Single Lance table - backfill reads existing columns and writes computed values to the target column
2. **Ray Workers**: Distributed processors that apply the UDF to batches of rows
3. **Checkpoint Store**: Intermediate storage for fault tolerance and deduplication
4. **Fragment Writers**: Specialized writers that commit computed column values back to the same table

---

## How It Works: Backfill Workflow

### 1. Defining a Column with a UDF

Before backfilling, you need to define a column with an associated UDF:

```python
from geneva import connect, udf
import pyarrow as pa

# Define the UDF
@udf(data_type=pa.list_(pa.float32(), 768))
def compute_embedding(text: str) -> list[float]:
    # Your embedding logic here
    return model.encode(text)

# Connect and add the column
db = connect("path/to/db")
table = db.open_table("my_table")
table.add_columns({"embedding": compute_embedding})
```

At this point, the column exists in the schema but all values are NULL.

### 2. Running the Backfill

```
User Code:
  job_id = table.backfill("embedding", concurrency=16)

Flow:
┌─────────────────────────────────────────────────────────────┐
│ Step 1: VALIDATION                                          │
│   - Verify column exists in table                           │
│   - Load UDF from column metadata                           │
│   - Validate input columns exist in schema                  │
│   - Check type compatibility with UDF annotations           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: PLANNING                                            │
│   - Create ScanTask for each fragment                       │
│   - Check existing checkpoints (skip completed work)        │
│   - Divide fragments into batch-sized tasks                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────────┐
│ Step 3: EXECUTION (Parallel)                                      │
│  Ray Worker 1            Ray Worker 2            Ray Worker 3     │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐ │
│  │Read batch    │        │Read batch    │        │Read batch    │ │
│  │from fragment │        │from fragment │        │from fragment │ │
│  ├──────────────┤        ├──────────────┤        ├──────────────┤ │
│  │Apply UDF to  │        │Apply UDF to  │        │Apply UDF to  │ │
│  │each row      │        │each row      │        │each row      │ │
│  ├──────────────┤        ├──────────────┤        ├──────────────┤ │
│  │Write to      │        │Write to      │        │Write to      │ │
│  │checkpoint    │        │checkpoint    │        │checkpoint    │ │
│  └──────────────┘        └──────────────┘        └──────────────┘ │
└───────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: COMMIT                                              │
│   - Fragment Writers collect checkpointed batches           │
│   - Write data files for each fragment                      │
│   - Partial commit every N fragments (commit_granularity)   │
│   - Final commit creates new table version                  │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- Checkpointing happens at batch level (every `checkpoint_size` rows)
- Partial commits happen at fragment level (every `commit_granularity` fragments)
- Failed jobs resume from the last checkpoint, not from the beginning

### Progress States (Visible in UX)

During a backfill, rows progress through three states that are displayed in the progress UI:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ROW PROGRESS STATES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐      ┌─────────────────┐      ┌─────────────┐          │
│  │ CHECKPOINTED│ ───► │ READY TO COMMIT │ ───► │  COMMITTED  │          │
│  └─────────────┘      └─────────────────┘      └─────────────┘          │
│                                                                         │
│  UDF executed,        Fragment complete,       Written to table,        │
│  result saved to      waiting for commit       visible to queries       │
│  checkpoint store     granularity threshold                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| State | Meaning | Recoverable? |
|-------|---------|--------------|
| **Checkpointed** | UDF has been executed and results saved to checkpoint store. Work is preserved but not yet visible in the table. | Yes - checkpoints survive job failures |
| **Ready to Commit** | All batches for a fragment are checkpointed. The fragment is queued for commit but waiting for `commit_granularity` threshold. | Yes - checkpoints survive job failures |
| **Committed** | Results written to the Lance table as a new version. Data is now visible to queries. | N/A - already persisted |

**Why three states?**
- **Checkpointed** provides fine-grained fault tolerance (per batch)
- **Ready to Commit** batches fragments for efficient writes
- **Committed** makes results visible while avoiding excessive table versions

---

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `col_name` | (required) | Target column to backfill |
| `udf` | None | Override the UDF (uses column's configured UDF if None) |
| `where` | None | SQL expression to filter rows for selective backfill ([datafusion syntax](https://datafusion.apache.org/user-guide/sql/index.html)) |
| `concurrency` | 8 | Number of Ray actor processes for parallel execution |
| `intra_applier_concurrency` | 1 | Threads per process (total parallelism = concurrency × this) |
| `checkpoint_size` | 100 | Rows per checkpoint (controls checkpointing frequency) |
| `task_size` | auto | Rows per worker task (defaults to table.count_rows() // workers // 2) |
| `commit_granularity` | 64 | Number of fragments before partial commit |
| `read_version` | latest | Table version to read from (for time-travel backfills) |

### Parameter Examples

```python
# Standard backfill with increased parallelism
table.backfill("embedding", concurrency=32)

# Selective backfill - only process new rows
table.backfill("embedding", where="created_at > '2024-01-01'")

# Memory-intensive UDF - smaller batches
table.backfill("embedding", checkpoint_size=50, concurrency=4)

# Time-travel backfill - read from historical version
table.backfill("embedding", read_version=42)
```

---

## Common Scenarios

### Scenario 1: Adding Embeddings to an Image Table

**Problem:** You have a table with 1M images and need to compute embeddings using a GPU model.

**Solution:**
```python
@udf(data_type=pa.list_(pa.float32(), 768), num_gpus=1)
def image_embedding(image_path: str) -> list[float]:
    return model.encode(load_image(image_path))

table.add_columns({"embedding": image_embedding})

# Backfill with GPU workers
job_id = table.backfill("embedding", concurrency=4)  # 4 GPU workers
```

**What happens:**
1. Ray schedules 4 GPU workers
2. Each worker processes batches of 100 rows (default checkpoint_size)
3. Every 64 fragments, a partial commit shows progress
4. If a worker fails, only the current batch is lost

### Scenario 2: Adding New Rows to an Already-Backfilled Table

**Problem:** You have a table with 1M images that already have embeddings computed via backfill. Now you add 100K new images and need embeddings for just the new rows.

**Solution:**
```python
# Add new data to the table
table.add(new_images_data)

# Run the same backfill command - it automatically processes only new data
job_id = table.backfill("embedding")
```

**What happens:**
1. The planner scans fragments and checks existing checkpoints
2. The 1M already-processed rows are in fragments with valid checkpoints - skipped entirely
3. The 100K new rows are in new fragments without checkpoints - scheduled for processing
4. Only the new fragments are processed and committed

**Key insight:** You don't need a WHERE clause or special handling. The checkpoint system automatically detects which fragments have already been processed and skips them.

### Scenario 3: Selective Backfill with WHERE Clause

**Problem:** You've added rows to the table, but some already have embeddings included (e.g., pre-computed externally). You only want to compute embeddings for rows that are missing them.

**Solution:**
```python
# Only backfill rows where embedding is NULL
table.backfill("embedding", where="embedding IS NULL")
```

**How it works:**
- The WHERE clause is evaluated during task creation
- Rows not matching the filter are marked with `__geneva_backfill_selected = False`
- The UDF is **not called** for non-selected rows (saves compute)
- Non-selected rows retain their existing values

### Scenario 4: Resuming a Failed Backfill

**Problem:** Your backfill job crashed halfway through.

**Solution:**
```python
# Simply run the backfill again - it will resume from checkpoints
job_id = table.backfill("embedding")
```

**What happens:**
1. The planner checks existing checkpoints
2. Already-computed batches are skipped
3. Already-committed fragments are skipped entirely
4. Only remaining work is scheduled

### Scenario 5: Processing Only Recent Data

**Problem:** You have a large table with years of historical data, but you only want to compute embeddings for recent records (e.g., last 30 days). Processing the entire history would be too expensive.

**Solution:**
```python
# Only backfill rows from the last 30 days
table.backfill("embedding", where="created_at > '2024-06-01'")

# Or using a relative date expression
table.backfill("embedding", where="created_at > now() - interval '30 days'")
```

**How it works:**
- The WHERE clause filters rows before UDF execution
- Older rows are skipped entirely - no compute cost
- Useful for prioritizing recent content or phased rollouts

**Use cases:**
- Processing only recent uploads while historical data can wait
- Phased backfill: process recent data first, then expand the date range
- Cost control: limit compute to high-priority data

---

## Quick Reference

**Prerequisites:**
- Column must be defined with `table.add_columns()` before backfilling
- UDF input columns must exist in the table schema
- For GPU UDFs, Ray cluster must have GPU resources available

**Key Operations:**
- `table.add_columns({"col": udf})`: Register a column with its UDF
- `table.backfill("col")`: Compute values for the column
- `table.backfill("col", where="...")`: Selective backfill
- `table.backfill_async("col")`: Non-blocking backfill, returns `JobFuture`
- `table.get_errors(job_id=..., column_name=...)`: Get error records

**Performance Characteristics:**
- **First backfill**: O(n) - must process all rows
- **Incremental backfill**: O(k) where k = new rows (existing rows skipped via checkpoints)
- **Resuming failed job**: O(k) where k = remaining rows
- **Selective backfill**: O(m) where m = matching rows
- **After partial commit**: Results visible immediately

**Async Usage:**
```python
# Start backfill without blocking
fut = table.backfill_async("embedding")

# Check status
fut.status()

# Wait for completion
job_id = fut.result()
```

---

## File System Reference (For Support/Diagnosis)

### Checkpoint Store Location

Checkpoints are stored alongside the table in a `_checkpoints` directory:

```
my_table.lance/
├── _versions/
├── _indices/
├── data/
│   └── *.lance
└── _checkpoints/           # Checkpoint storage
    └── *.lance             # One file per checkpoint key
```

**Checkpoint file naming:** Each checkpoint is stored as `{checkpoint_key}.lance` where the key follows this format:

```
udf-{udf_name}_ver-{udf_version}_col-{column}_where-{hash(filter)}_uri-{hash(uri)}_ver-{version}_frag-{frag_id}_range-{start}-{end}
```

Example:
```
udf-embedding_ver-abc123_col-embedding_where-80f7..._uri-d5dd..._ver-42_frag-3_range-0-100.lance
```

Components:
- `udf-{name}`: UDF function name
- `ver-{version}`: UDF version (MD5 hash of pickled function)
- `col-{column}`: Target column name
- `where-{hash}`: Hash of WHERE clause (if any)
- `uri-{hash}`: Hash of dataset URI
- `ver-{version}`: Dataset version number
- `frag-{id}`: Fragment ID being processed
- `range-{start}-{end}`: Row range within the fragment

### Job History & Status

Jobs are tracked in the database's job history:

```python
# List recent jobs
db._history.list()

# Get job status
db._history.get(job_id)

# Job states: PENDING, RUNNING, DONE, FAILED
```

### Error Storage

When UDF execution fails, errors are captured for debugging:

```python
# Get all errors for a job
errors = table.get_errors(job_id="...", column_name="embedding")

# Get row addresses of failed rows (for retry)
failed_addrs = table.get_failed_row_addresses(job_id="...", column_name="embedding")
```

---

## Troubleshooting

### Common Issues and Resolution

#### Backfill Stuck or Running Slowly

**Symptoms:** Progress bar not moving, workers appear idle.

**Diagnosis:**
1. Check Ray dashboard for worker status
2. Look for workers waiting on resources (GPU/memory)

**Resolution:**
- Reduce `concurrency` if workers are memory-constrained
- Check if UDF has resource requirements (`num_gpus`, `num_cpus`)
- Increase `task_shuffle_diversity` to improve load balancing

#### Out of Memory Errors

**Symptoms:** Ray workers killed with OOM, job fails.

**Diagnosis:**
1. Check UDF memory usage per row
2. Review `checkpoint_size` setting

**Resolution:**
```python
# Reduce batch size to use less memory per worker
table.backfill("embedding", checkpoint_size=25, task_size=100)
```

#### UDF Execution Errors

**Symptoms:** Job fails with UDF-related exceptions.

**Diagnosis:**
```python
# Get error details
errors = table.get_errors(job_id=job_id, column_name="embedding")
for e in errors:
    print(e)  # Shows row address, error message, traceback
```

**Resolution:**
- Fix UDF code
- Handle edge cases (NULL inputs, malformed data)
- Consider using error handling configuration:
```python
from geneva.debug.error_store import ErrorHandlingConfig

@udf(data_type=pa.float32(), error_handling=ErrorHandlingConfig(store_errors=True))
def my_udf(x: str) -> float:
    return process(x)
```

#### Failed Backfill Won't Resume

**Symptoms:** Re-running backfill reprocesses already-completed work.

**Diagnosis:**
1. Check if checkpoint store is accessible
2. Verify checkpoint files exist in `_checkpoints/`

**Resolution:**
- Ensure same table reference is used (checkpoints are keyed by URI)
- Check for checkpoint store connectivity issues (cloud storage)

#### Type Mismatch Errors

**Symptoms:** `TypeError` or `ArrowInvalid` during UDF execution.

**Diagnosis:**
The error message indicates which column has a type mismatch:
```
UDF 'my_udf' failed with type error: ...
Input batch schema: ...
UDF expects input_columns: ['x']
UDF output type: float32
```

**Resolution:**
- Add type annotations to UDF parameters
- Ensure UDF `data_type` matches actual output
- Check if column types have changed between table versions

#### Missing Input Columns

**Symptoms:** `ValueError: Column 'x' not found in table schema`

**Diagnosis:**
The UDF expects columns that don't exist in the table.

**Resolution:**
- Check column names in UDF signature match table schema
- Use `input_columns` parameter to map different names:
```python
table.add_columns({"output": (my_udf, ["actual_column_name"])})
```

### Error Messages Reference

| Error Message | Meaning | Resolution |
|--------------|---------|------------|
| "Column X is not defined in this table" | Backfilling column not registered | Run `table.add_columns()` first |
| "UDF expects input columns X which are not found" | Missing input column | Check column names, use input_columns mapping |
| "Cannot validate generic pa.Array type" | UDF type annotation too generic | Add specific type annotations |
| "Type mismatch for column X" | Column type doesn't match UDF annotation | Fix type annotations or cast data |

### Performance Troubleshooting

#### Key Metrics to Monitor

1. **Checkpoint creation rate:** How many checkpoints per second?
2. **Partial commit frequency:** Are partial commits happening as expected?
3. **Worker utilization:** Are all workers actively processing?
4. **Memory per worker:** Are workers approaching memory limits?

#### Tuning Recommendations

**1. Tuning `checkpoint_size` for proof-of-life updates**

The `checkpoint_size` controls how frequently you see progress updates. Choose based on your UDF's execution speed:

| UDF Speed | Example | Recommended `checkpoint_size` | Update Frequency |
|-----------|---------|------------------------------|------------------|
| Fast (1000+ rows/sec) | Simple transformations | 120,000 | ~2 minutes |
| Medium (10-100 rows/sec) | API calls, light ML | 1,000 - 10,000 | ~1-2 minutes |
| Slow (1 row per 30s) | Heavy GPU inference | 10 | ~5 minutes |

*Goal: Get progress updates every 1-5 minutes so you know the job is alive.*

**2. Scaling beyond Ray's worker limit**

Ray has a limit of ~10,000 workers. If you're approaching this limit, use `intra_applier_concurrency` to add thread-level parallelism within each worker:

```python
# Instead of 10,000 workers:
table.backfill("col", concurrency=10000)  # May hit Ray limits

# Use threads within fewer workers:
table.backfill("col", concurrency=2000, intra_applier_concurrency=5)  # 2000 workers × 5 threads
```

**3. GPU workloads**

Match `concurrency` to available GPUs and set `num_gpus` in the UDF:

```python
@udf(data_type=pa.list_(pa.float32(), 768), num_gpus=1)
def gpu_embedding(text: str) -> list[float]:
    return model.encode(text)

# If you have 8 GPUs:
table.backfill("embedding", concurrency=8)
```

**4. Frequent failures (suggestion)**

If your UDF is prone to transient failures, consider a smaller `checkpoint_size` to minimize rework when resuming. This is a trade-off against checkpoint overhead.

---

## Implementation Internals

This section provides detailed implementation information for debugging and contributing to the codebase.

### Task Hierarchy

```
ReadTask (abstract base)
└── ScanTask
    - Reads from table with fragment ID
    - Uses Lance scanner with offset/limit
    - Supports WHERE clause filtering
    - Returns batches with _rowaddr column

MapTask (abstract base)
└── BackfillUDFTask
    - Applies single UDF to batches
    - Handles BACKFILL_SELECTED filtering
    - Generates checkpoint keys
    - Manages output schema
```

### Pipeline Components

```
ColumnAddPipelineJob
├── ActorPool[ApplierActor]
│   - Ray remote actors (one per concurrency slot)
│   - Each actor runs CheckpointingApplier
│   - Applies map tasks to read tasks
│   - Stores results in checkpoint store
│
├── FragmentWriterManager
│   ├── FragmentWriterSession (per fragment)
│   │   ├── Ray.remote(FragmentWriter)
│   │   │   - Buffer and sort batches
│   │   │   - Align to physical layout
│   │   │   - Write Lance data file
│   │   │
│   │   ├── Checkpoint queue
│   │   └── Inflight futures
│   │
│   └── Commit coordinator
│       - Track completed fragments
│       - Batch commits (commit_granularity)
│       - Handle version conflicts
│
└── JobTracker
    - Progress tracking
    - Fragment completion metrics
    - Task counts
```

### Checkpoint Mechanism

#### Checkpoint Key Format

```python
# Checkpoint key components
prefix = f"udf-{udf_name}_ver-{udf_version}_col-{column}_where-{hash(filter)}_uri-{hash(uri)}_ver-{version}"
checkpoint_key = f"{prefix}_frag-{frag_id}_range-{start}-{end}"

# Example
checkpoint_key = "udf-embedding_ver-abc123_col-embedding_where-80f7..._uri-d5dd..._ver-42_frag-3_range-0-100"
```

#### Checkpoint Storage Format

```python
# Stored as PyArrow RecordBatch in Lance files
checkpoint_store[key] = pa.RecordBatch.from_pydict({
    "column_name": [computed_values],
    "_rowaddr": [row_addresses],
})
```

#### Resume Logic

1. **Fragment-level check:** Is there a complete fragment checkpoint?
   - If yes, skip entire fragment
2. **Batch-level check:** Which row ranges are already checkpointed?
   - Compute missing ranges
   - Create tasks only for missing ranges
3. **Task execution:** Apply UDF only to non-checkpointed rows

### Selective Backfill (WHERE Clause)

When a WHERE clause is provided:

1. **Read phase:** Scanner evaluates filter, adds `__geneva_backfill_selected` column
2. **UDF phase:**
   - For SCALAR UDFs: Check mask per-row, skip if not selected
   - For ARRAY/RECORDBATCH UDFs: Filter batch first, expand results back
3. **Write phase:** Merge new values with existing (for non-selected rows)

```python
# In BackfillUDFTask.apply():
if has_backfill_selected:
    mask = batch[BACKFILL_SELECTED]
    # Only call UDF for selected rows
    if udf.arg_type == UDFArgType.SCALAR:
        # Check mask per row
        for idx in range(batch.num_rows):
            if mask[idx]:
                yield udf.func(*args)
            else:
                yield None  # Keep existing value
```

### Commit Strategy

**Partial Commits:**
- Every `commit_granularity` fragments, commit to create a new table version
- Allows progress visibility before job completion
- Uses `lance.LanceOperation.DataReplacement` for atomic fragment updates

**Version Conflict Handling:**
- Uses Lance's built-in conflict detection
- If another writer modifies the table, retry with exponential backoff
- Checkpoints remain valid across version conflicts

### Data Flow Diagram

```
┌──────────────────────┐
│   TABLE (Lance)      │
│   Fragment N         │
└──────────┬───────────┘
           │
           │ ScanTask reads rows
           │ with _rowaddr
           ↓
┌──────────────────────┐
│ CheckpointingApplier │
│ (Ray Actor)          │
│                      │
│  1. Check cached?    │──→ Return cached
│  2. Read batches     │
│  3. Apply UDF        │──→ BackfillUDFTask
│  4. Checkpoint       │
└──────────┬───────────┘
           │
           │ Store checkpoint
           ↓
┌──────────────────────┐
│ CHECKPOINT STORE     │
│ (Lance files)        │
└──────────┬───────────┘
           │
           │ Fragment Writer reads
           ↓
┌──────────────────────┐
│ FragmentWriter       │
│ (Ray Actor)          │
│                      │
│  1. Collect batches  │
│  2. Sort by _rowaddr │
│  3. Write data file  │
└──────────┬───────────┘
           │
           │ DataReplacement commit
           ↓
┌──────────────────────┐
│   TABLE (Lance)      │
│   Fragment N         │
│   - Updated column   │
│   - New version      │
└──────────────────────┘
```

---

## Summary

Geneva backfills provide a robust system for computing column values with UDFs:

### Key Features

1. **Lazy computation:** Define columns upfront, compute later
2. **Distributed execution:** Parallel processing via Ray workers
3. **Checkpoint-based recovery:** Resume from failures without data loss
4. **Selective backfill:** Use SQL filters to process only needed rows
5. **Partial visibility:** See results before job completion via partial commits

### Performance Characteristics

- **Initial backfill:** O(n) for all rows
- **Resume after failure:** O(k) where k = remaining rows
- **Selective backfill:** O(m) where m = matching rows
- **Checkpoint overhead:** Minimal (Lance file writes)

### When to Use Backfills

- Computing embeddings for ML workloads
- Adding derived columns (predictions, transformations)
- Processing new data incrementally
- Recomputing values after UDF logic changes
