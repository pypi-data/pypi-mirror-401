# Geneva Backfill Conflicts

## Overview

Geneva backfills operate on a **point-in-time snapshot** of the table. Certain operations can break assumptions that earlier versions (<=0.8.x) relied on, causing backfills to fail or require full reprocessing.

**Geneva 0.9.x** adds handling for these scenarios, reducing unnecessary recomputation of expensive UDF operations.

---

## Sequential Scenarios

These scenarios involve operations that happen **between** backfills, not during a running backfill.

| Scenario | <=0.8.x | >=0.9.x |
|----------|---------|---------|
| Backfill → Compact → Re-backfill | Full reprocessing | Backfill skipped due to implicit WHERE filter and UDF version check |
| Partial backfill → Compact → Resume | Full reprocessing | Incremental backfill due to implicit WHERE and UDF version checks |
| Backfill → alter_columns → Re-backfill | Full reprocessing | Full reprocessing (intentional) |

### Example: Backfill → Compact → Re-backfill

```
Timeline:
1. First backfill runs on column b
   - Reads fragment 0 (id=0) at version N
   - Computes values, writes file_b.lance (field_ids=[10])
   - Commits: fragment 0 now has file_a.lance + file_b.lance

2. User runs compact_files()
   - Compaction reorganizes data: removes deleted rows, merges small fragments
   - Creates NEW fragment with NEW identity (e.g., id=5)
   - Old fragment 0 no longer exists at latest version

3. Second backfill runs on column c
   - Reads fragment 5 at version N+1
   - Computes values, writes file_c.lance (field_ids=[11])
   - DataReplacement commit works normally (fragment 5 exists)
```

**Key insight**: The fragment **identity** (ID) changes during compaction, not just the file structure. In <=0.8.x, this required full reprocessing. In >=0.9.x, the default WHERE filter (`<col> IS NULL`) skips already-computed rows.

### How >=0.9.x Detects What to Reprocess

| | **UDF Version Change** | **Compaction (Same UDF)** |
|---|---|---|
| **Trigger** | `alter_columns` changed UDF from v1 to v2 | Table compacted, fragment IDs changed |
| **Existing Data** | All rows have non-NULL values (computed with v1) | All rows have non-NULL values (computed with v1) |
| **Current UDF** | v2 (different from what computed the data) | v1 (same as what computed the data) |
| **Checkpoint State** | Old checkpoints exist with v1 in key | Old checkpoints exist with old frag IDs |
| **What We Want** | Recompute ALL rows with v2 | Skip all rows (already computed correctly) |
| **WHERE Filter** | DON'T apply `IS NULL` | APPLY `IS NULL` to skip computed rows |
| **Detection** | Find old checkpoint with different `udf_checksum` | Find old checkpoint with SAME `udf_checksum` |

### Detailed Sequential Scenarios

**Scenario A: Partial backfill → Compaction → Resume (same UDF)**
1. Add column with UDF v1
2. Partial backfill (frags 0,1,2 of 10) - checkpoints created with `udf_checksum=v1`
3. Compaction - fragment IDs change
4. Resume backfill with v1
   - Search finds old checkpoints with `udf_checksum=v1`
   - v1 == current v1 → SAME checksum
   - **Apply WHERE filter** → Only NULL rows processed

**Scenario B: Partial backfill → alter_columns → Resume (different UDF)**
1. Add column with UDF v1
2. Partial backfill (frags 0,1,2 of 10) - checkpoints created with `udf_checksum=v1`
3. `alter_columns` changes UDF to v2
4. Resume backfill with v2
   - Search finds old checkpoints with `udf_checksum=v1`
   - v1 != current v2 → DIFFERENT checksum
   - **DON'T apply WHERE filter** → ALL rows recomputed with v2

**Scenario C: Partial backfill → Compaction → alter_columns → Resume**
1. Partial backfill with v1 - checkpoints created with `udf_checksum=v1`
2. Compaction - frag IDs change
3. `alter_columns` to v2
4. Resume backfill with v2
   - Find old checkpoints with v1 checksum
   - v1 != v2 → DIFFERENT checksum
   - **DON'T apply WHERE filter** → ALL rows recomputed with v2

**Scenario D: First backfill (no prior checkpoints)**
1. Add column with UDF v1
2. Start backfill (no prior checkpoints)
   - Search finds NO checkpoints
   - No mismatch (nothing to compare)
   - **Apply WHERE filter** → All NULL rows processed (correct for first backfill)

---

## Concurrent Scenarios

These scenarios involve operations that happen **during** a running backfill.

| Scenario | <=0.8.x | >=0.9.x |
|----------|---------|---------|
| Concurrent backfills (different columns) | Completes with potential missing data | Succeeds with version retry and merge |
| `compact_files()`/`optimize()` during backfill | Fails, manual re-run (full reprocessing) | Graceful fail, requires manual re-run |
| `merge_insert`/`delete()` with updates during backfill | Fails, manual re-run (full reprocessing) | Graceful fail, requires manual re-run |
| External compaction (LanceDB Cloud) | Fails, manual re-run (full reprocessing) | Graceful fail, requires manual re-run |

### Safe Operations During Backfill

| Operation | Why It's Safe |
|-----------|---------------|
| `merge_insert` with only INSERTs | Creates new fragments, doesn't modify existing |
| `add()` / append data | Creates new fragments, doesn't modify existing |
| Read operations (`search`, `to_arrow`) | Read-only, no fragment modification |
| Adding new columns | Schema change only, no fragment rewrite |

### How Concurrent Backfills Succeed (>=0.9.x)

When multiple backfills run concurrently on different columns of the same table, version conflicts are handled automatically:

```
Timeline:
1. Backfill-B reads fragment 0 at v5, computes column b, writes file with field_ids=[10]
2. Backfill-C reads fragment 0 at v5, computes column c, writes file with field_ids=[11]
3. Backfill-C commits first → fragment now at v6, has files for field_ids=[1,2,11]
4. Backfill-B tries commit at v5 → VERSION CONFLICT
5. Backfill-B gets latest version (v6) → retries DataReplacement at v6
6. DataReplacement ADDS our file (field_ids=[10]) to fragment → v7 has [1,2,10,11]
```

**Key insight**: DataReplacement **adds** column files to fragments based on field_id - it doesn't replace other columns' files. Each backfill writes to different field_ids, so concurrent commits don't overwrite each other's data.

---

## Error Messages and Recovery

### Error Message

When a conflict occurs, Geneva workers fail with:

```
TypeError: fragments must be an iterable of LanceFragment. Got <class 'NoneType'> instead.
```

This means the fragment Geneva was trying to process no longer exists at the version it was reading.

### Root Cause

1. Geneva backfill starts with point-in-time snapshot at version N
2. Concurrent operation (merge_insert update, compaction, delete) modifies fragments
3. Geneva workers try to read fragments that no longer exist at version N
4. Workers fail with fragment-not-found errors

Note: This is NOT a commit conflict (no `CommitConflict` exception). The failure happens during fragment reading, not during commit. Geneva's version-bumping conflict handling doesn't help because the fragments themselves are gone.

### Recovery

1. Wait for any concurrent operations to complete
2. Re-run the backfill: `tbl.backfill("column_name")`
3. The backfill will process all rows that still need computation

---

## Best Practices

### 1. Avoid fragment-modifying operations during backfill

- Don't run `compact_files()` or `optimize()` while backfill is running
- Don't run `merge_insert` with `when_matched_update_all()` during backfill
- Disable auto-compaction in LanceDB Cloud during backfills

### 2. Sequence your operations

```
1. Complete all data ingestion first
2. Run backfill to compute UDF columns
3. Then run compaction/optimization
```

### 3. Use `merge_insert` safely

- INSERT-only operations are safe during backfill
- UPDATE operations on existing rows will cause conflicts
- New rows will have NULL in UDF columns until next backfill

### 4. Monitor backfill progress

```python
fut = tbl.backfill_async("column_name")
while not fut.done():
    time.sleep(1)
# Check for errors before running subsequent operations
```

### Why We Don't Block at the API Level

API-level blocking won't help because external operations bypass Geneva:

- Direct Lance file manipulation
- LanceDB Cloud/Enterprise (Phalanx) auto-compaction
- External tools accessing the same Lance dataset

---

## Implementation Mechanisms

### Versioned Dataset Opens (GEN-248)

Backfill tasks now read from the **planned version** instead of the latest version:
- `ScanTask._get_table()` uses `self.version` via `attrs.evolve`
- `FragmentWriter.write()` calls `dataset.checkout_version(self.version)`
- Version is passed through `FragmentWriterSession` and `FragmentWriterManager`

**Result**: Helps when concurrent ops create NEW versions but don't modify the OLD version's fragments. Does NOT help when fragment files are physically deleted/rewritten.

### Graceful Degradation (GEN-248)

When fragment writes fail, the pipeline now:
- Catches exceptions in `FragmentWriterSession.poll_ready()` and `drain()`
- Marks failed fragments with `failed=True` and `failure_reason`
- Tracks failed fragments in `FragmentWriterManager.failed_fragments`
- Continues processing remaining fragments instead of crashing
- Commits successfully written fragments
- Logs summary of failures at cleanup

**Result**: Pipeline completes with partial success. Failed fragments have NULL values but checkpoints are preserved. User can re-run backfill and checkpoints will be reused - only failed fragments need recomputation.

**Key files**: `src/geneva/runners/ray/pipeline.py`

### Default WHERE Filter for Backfill

`backfill()` and `backfill_async()` now default the `where` parameter to `"<col_name> IS NULL"`:
- Automatically skips rows that already have computed values
- Prevents UDF re-execution after compaction or other fragment reorganizations
- Use `where="1=1"` to force reprocessing all rows

**Result**: Even if checkpoint keys don't match (due to version changes), already-computed rows are skipped because they have non-NULL values in the target column.

**Key files**: `src/geneva/table.py`

### Struct Column Handling

Struct columns cannot use the default `<col> IS NULL` filter because:
- A struct with all NULL fields (`{"lpad": None, "rpad": None}`) is NOT equal to NULL
- The `IS NULL` check only matches actual NULL values, not structs with NULL fields
- After a partial backfill with WHERE filter, uncomputed rows have struct-with-NULL-fields, not NULL

**Current Behavior**: For struct columns with no explicit `where` parameter, all rows are reprocessed on each backfill. This is less efficient but correct.

**Why Per-Fragment Data File Checking Doesn't Work**:
We initially tried checking if fragments have data files for the struct column:
- Problem: After a partial backfill with explicit WHERE filter (e.g., `where="a % 2 = 0"`), the fragment HAS data files but contains NULL values for non-matching rows
- The data file check can't distinguish between "fully computed" and "partially computed" fragments
- Result: Fragments were incorrectly skipped, leaving NULL values

**Workarounds for efficient struct column backfill**:
1. Don't use partial backfills with WHERE filters for struct columns
2. If you need partial processing, drop and re-add the column before resuming
3. Use explicit `where="1=1"` to force reprocessing all rows

**Key files**: `src/geneva/table.py`

### UDF Version Change Detection

The default WHERE filter must distinguish between:
1. **Compaction (same UDF)**: Skip already-computed rows
2. **UDF change (via `alter_columns`)**: Recompute all rows with new UDF

**Solution**: Store `udf_checksum` in each fragment's checkpoint DATA. Before applying WHERE filter, use regex search to find all checkpoints for the column and check their stored checksums.

**Algorithm**:
1. Get current UDF checksum from `virtual_column.udf` metadata
2. List checkpoint keys with prefix `udf-{udf_name}_`
3. Regex filter to find keys matching `udf-{name}_ver-.*_col-{column}_.*`
4. Read matching checkpoints and check stored `udf_checksum`
5. If ANY checkpoint has different checksum → UDF changed → don't apply WHERE filter
6. If ALL checkpoints match (or none exist) → apply `<col> IS NULL` filter

**Key files**: `src/geneva/table.py`, `src/geneva/runners/ray/pipeline.py`, `src/geneva/apply/utils.py`

### Input Column Data Change Detection (srcfiles_hash mismatch)

When a UDF's input column is updated (e.g., column `b` is re-backfilled with a new UDF), downstream columns that depend on it should be recomputed. The system detects this by comparing the `srcfiles_hash` in existing checkpoint keys against the current input data files.

**Algorithm**:
1. Before applying the default WHERE filter, check if UDF has input columns
2. Get field IDs for input columns using `_get_relevant_field_ids()`
3. List checkpoint keys for the column with regex filter
4. Extract `srcfiles-{hash}` from existing checkpoint keys
5. Compute current srcfiles hash for first fragment using `get_source_data_files()` and `hash_source_files()`
6. If ANY checkpoint has different srcfiles hash → input data changed → skip WHERE filter

**Example scenario**:
```
1. Table has columns: a (raw data), b (depends on a), c (depends on b)
2. User runs alter_columns to update b's UDF
3. User backfills b with new UDF - b now has different values
4. User backfills c (depends on b)
5. System detects srcfiles_hash mismatch (b's data files changed)
6. Skips default WHERE filter → c recomputed with new b values
```

**Key files**: `src/geneva/table.py`, `src/geneva/apply/utils.py`

### Explicit WHERE Filter Warning

When a user provides an explicit `where` filter (e.g., `where="b IS NULL"`) but the system detects a UDF version or srcfiles hash mismatch, a WARNING is logged. The user's explicit filter takes precedence, but they are informed that some rows may not be reprocessed.

**Behavior**:
- Mismatch detection runs always (not just when `where=None`)
- If explicit filter + mismatch: log WARNING, honor user's filter
- If no explicit filter + mismatch: skip default filter, process all rows
- Recommended workaround: use `where="1=1"` to force reprocessing all rows

**Key files**: `src/geneva/table.py`

### Version-Independent Checkpoint Keys (PR #473)

Checkpoint key format changed to remove dataset version dependency:
- **Old format**: `udf-{name}_ver-{version}_col-{column}_where-{hash}_uri-{hash}_ver-{dataset_version}_frag-{id}_range-{start}-{end}`
- **New format**: `udf-{name}_ver-{version}_col-{column}_where-{hash}_uri-{hash}_srcfiles-{hash}_frag-{id}_range-{start}-{end}`

Key changes:
- Removed `_ver-{dataset_version}` from checkpoint prefix
- Added `_srcfiles-{hash}` - hash of source data files for input columns
- Checkpoints now only invalidate when **input data** changes, not when dataset version changes
- Output field ID validation added to detect schema changes (column drop/re-add)

**Result**: Checkpoints survive dataset version changes (compaction, new data ingestion) as long as the input data files for the fragment remain unchanged.

**Key files**: `src/geneva/checkpoint_utils.py`, `src/geneva/apply/__init__.py`, `src/geneva/apply/task.py`, `src/geneva/runners/ray/pipeline.py`

### Concurrent Backfills: Version Conflict Handling

**Location**: `src/geneva/runners/ray/pipeline.py` - `FragmentWriterManager._commit_if_n_fragments()`

**Version conflict handling flow**:
```python
except OSError as e:
    # Handle version conflict
    if "Commit conflict for version" not in str(e):
        raise e

    # Get latest version from dataset
    latest_ds = lance.dataset(self.ds_uri, storage_options=storage_options)
    latest_version = latest_ds.version

    # Retry DataReplacement at latest version
    version = latest_version
    # Loop continues with retry
```

**Configuration**: `WRITER_STALL_IDLE_ROUNDS = 6` increases stall detection timeout from 15s to 30s to prevent premature writer restarts under resource contention.

**Key files**: `src/geneva/runners/ray/pipeline.py`

### Post-Compaction Handling (Merge Fallback)

When compaction merges column files, the original separate column files are combined. If a backfill then tries to add/update a column using DataReplacement, it may fail because the field_ids in the merged file don't match what DataReplacement expects.

**Why DataReplacement fails after compaction**:

```
Timeline:
1. Partial backfill creates separate column file
   - Fragment 0: file_a.lance (field_ids=[0]) + file_b.lance (field_ids=[10])

2. Compaction merges files
   - Fragment 0: combined.lance (field_ids=[0,10])

3. alter_columns changes UDF to v2

4. Resume backfill recomputes all rows, creates new file
   - New file: file_b_v2.lance (field_ids=[10])

5. DataReplacement tries to commit
   - Looks for existing file with field_ids=[10] to replace
   - Only finds combined.lance with field_ids=[0,10]
   - ERROR: "no changes were made" (can't find matching file)
```

**Error**: `"Expected to modify the fragment but no changes were made. This means the new data files does not align with any existing datafiles."`

**Solution**: `_commit_with_merge_fallback()` catches this error and uses `LanceOperation.Merge` instead:

1. Build complete fragment metadata for ALL fragments
2. For modified fragments:
   - Mask the original files' field_ids (set to -2 = "don't read from here")
   - Add the new column file with correct field_ids
3. Commit using Merge operation (directly sets fragment metadata)

**When this triggers**:
- srcfiles_hash mismatch detection runs first and often catches compaction
- But some scenarios (partial backfill → compaction → alter_columns → resume) can still hit the DataReplacement failure
- The Merge fallback ensures these scenarios succeed

**Caveats**:
- Merge requires ALL fragments to be provided, which can cause conflicts with concurrent writes

**⚠️ Open Investigation: Deletions and Row Alignment**

There's a potential concern when compaction **materializes deletions** (physically removes deleted rows):

- Before compaction: Fragment has 100 physical rows, 10 deleted (90 visible)
- After compaction with `materialize_deletions=True`: Fragment has 90 physical rows
- Our new column file was computed from 100 rows (pre-compaction)
- Merge fallback adds the 100-row file to a 90-row fragment

Lance currently does NOT validate that file row counts match fragment physical_rows (see `transaction.rs:2090` TODO in Lance source). Current tests pass, but this potential data misalignment needs further investigation.

**Recommended workaround**: Use `optimize(materialize_deletions=False)` when compacting tables with pending backfills.

**Key files**: `src/geneva/runners/ray/pipeline.py`

---

## Future: Checkpoint Remapping with Compaction Lineage

### Overview

The current solution (version-independent checkpoint keys + default WHERE filter) handles most scenarios effectively. However, there's room for optimization: when fragments are reorganized by compaction, checkpoint keys still reference OLD fragment IDs and can't be found directly.

Currently, this is mitigated by:
- Default WHERE filter (`<col> IS NULL`) skips already-computed rows
- Only NULL rows in reorganized fragments need recomputation

A future optimization would **remap checkpoints** from old fragment layout to new fragment layout, avoiding any recomputation.

### Why Current Solution Is Sufficient

With version-independent checkpoint keys (PR #473) + WHERE filter default:

1. **Dataset Version in Prefix**: **FIXED** (PR #473)
   - Checkpoint keys no longer include dataset version
   - Now use source files hash instead - only invalidates when input data changes
   - Cross-version checkpoint reuse now works

2. **Fragment ID Mismatch**: When fragments reorganize (compaction), checkpoint keys still reference OLD fragment IDs.
   - **Mitigated by**: Default `where="<col> IS NULL"` filter skips already-computed rows
   - Already-computed rows have non-NULL values and are skipped

3. **Practical Workflow**: User re-runs backfill once after compaction conflict:
   - First backfill: Graceful degradation (partial success, some fragments fail)
   - Second backfill: Checkpoints for unchanged fragments are reused; NULL rows in failed fragments recomputed

4. **Idempotent Recovery**: Re-running backfill after a conflict makes progress and completes:
   - Failed fragments from first run retain NULL values (graceful degradation doesn't corrupt data)
   - Second backfill reads current (post-compaction) fragments at latest version
   - Default WHERE filter (`<col> IS NULL`) processes only uncomputed rows
   - Completes successfully if no new conflicts occur during re-run
   - Test coverage: `test_scenario_a_verify_where_filter_skips_computed_rows()`

### Future Optimization: Fragment ID Remapping

For full automatic recovery without any recomputation, would need:

1. **Compaction Lineage API**: Query fragment reorganization history to map old_frag_id → new_frag_id
2. **Checkpoint Key Parsing**: Extract fragment ID from checkpoint keys
3. **Row Address Remapping**: Update `_rowaddr` column values to new fragment layout
4. **Checkpoint Store Update**: Store remapped checkpoints with new fragment IDs

**Design sketch**:

```python
# Parse checkpoint key to extract fragment info
def parse_checkpoint_key(key: str) -> CheckpointKeyInfo:
    # Returns: prefix, frag_id, start, end
    ...

# Remap _rowaddr column to new fragment ID
def remap_checkpoint_rowaddr(batch, new_frag_id) -> RecordBatch:
    # Row address = (frag_id << 32) | local_offset
    # Preserve local_offset, replace fragment ID
    ...

# Remap all checkpoints for a fragment
def remap_checkpoints_for_fragment(store, prefix, old_frag_id, new_frag_id):
    # Find checkpoints, remap, store with new keys
    ...
```

### Compaction Lineage API

**Dependency**: Requires compaction lineage API from Lance.

**Python API types** (from lineage API):

```python
class FragDigest:
    id: int                # Fragment ID
    physical_rows: int     # Number of physical rows
    num_deleted_rows: int  # Number of deleted rows

class FragReuseGroup:
    old_frags: list[FragDigest]  # Source fragments
    new_frags: list[FragDigest]  # Target fragments

class CompactionLineageEntry:
    compaction_id: str
    timestamp: datetime
    source_version: int
    target_version: int
    rewrite_groups: list[FragReuseGroup]
```

**Integration point** in `pipeline.py`:

```python
lineage = table.compaction_lineage()
if not lineage:
    logger.warning("Compaction lineage not available, cannot remap checkpoints")
    return {}

mapping = compute_fragment_mapping_from_lineage(
    lineage=lineage,
    old_frag_ids=list(self.failed_fragments.keys()),
    src_version=self.dst_read_version,
    current_version=current_dataset.version(),
)
```

**Helper function**:
```python
def compute_fragment_mapping_from_lineage(
    lineage: CompactionLineage,
    old_frag_ids: list[int],
    src_version: int,
    current_version: int,
) -> dict[int, set[int]]:
    """
    Compute old fragment ID -> new fragment IDs mapping from compaction lineage.
    """
    result: dict[int, set[int]] = {}
    old_frag_set = set(old_frag_ids)

    # Process lineage entries from oldest to newest (entries are newest-first)
    for entry in reversed(lineage.entries):
        # Only consider compactions between our versions
        if entry.source_version < src_version:
            continue
        if entry.source_version >= current_version:
            break

        for group in entry.rewrite_groups:
            # Extract IDs from FragDigest objects
            old_ids = {f.id for f in group.old_frags}
            new_ids = {f.id for f in group.new_frags}

            # Check if any of our old fragments were sources
            overlap = old_frag_set.intersection(old_ids)
            for old_id in overlap:
                if old_id not in result:
                    result[old_id] = set()
                result[old_id].update(new_ids)

    return result
```

### How Row Address Mapping Works

```
OLD layout:                         NEW layout (after compaction):
Fragment 0: rows 0-99               Fragment 0: rows 0-199 (merged)
Fragment 1: rows 100-199

Checkpoint has:
  key="...frag-0_range-0-50" → batch with _rowaddr=[0,1,2,...,49], computed_col=[v0,v1,...]
  key="...frag-1_range-100-150" → batch with _rowaddr=[100,101,...,149], computed_col=[v100,v101,...]

Remapping:
  Old frag 0, offset 0-99 → New frag 0, offset 0-99 (unchanged)
  Old frag 1, offset 0-99 → New frag 0, offset 100-199 (shifted)

Result: Write computed values to new fragment layout without recomputing
```

### Lance Versioning Behavior

Important Lance behaviors relevant to checkpoint remapping:
- Old fragment files ARE preserved when new versions are created
- `checkout_version()` gives access to fragments as they existed at that version
- Compaction creates new fragments, old fragments remain accessible at old versions
- Row IDs change on compaction unless stable row IDs enabled (`enable_stable_row_ids`)

**Note**: Checkpoint remapping via compaction lineage would **not** require `enable_stable_row_ids`. The fragment mappings come directly from the compaction operation's recorded lineage.

---

## Test Files

### Conflict Behavior Tests: `src/tests/test_merge_insert_conflict.py`

- `test_merge_insert_during_backfill` - INSERT-only to different column is safe
- `test_merge_insert_update_during_backfill` - INSERT+UPDATE to different column
- `test_merge_insert_same_column_conflict` - INSERT to same column causes conflict
- `test_merge_insert_update_same_rows` - UPDATE causes fragment invalidation
- `test_compaction_during_backfill` - Compaction causes fragment invalidation
- `test_delete_during_backfill` - Delete causes fragment invalidation

### WHERE Filter Scenario Tests: `src/tests/test_where_filter_scenarios.py`

- `test_scenario_c_with_retry_after_compaction` - backfill → compact → alter_columns → re-backfill
- `test_explicit_filter_with_udf_change_logs_warning`
- `test_explicit_1_equals_1_forces_reprocessing`
- `test_struct_column_skips_fragments_with_data_files` - struct column skips already-computed fragments
- `test_struct_column_processes_all_if_no_data_files` - struct column processes all when none computed
- `test_struct_column_reprocesses_all_after_alter_columns` - struct column reprocesses after UDF change

### Concurrent Backfill Tests: `src/tests/test_pipeline_concurrent.py`

- 9 concurrent backfills for columns b-j on same table

---

## Related

- Linear ticket: GEN-248
