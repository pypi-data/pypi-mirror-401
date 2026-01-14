# Fragment Source Lineage Tracking During Compaction

## Overview

Add metadata tracking for which fragments/datafiles were merged into new fragments during compaction operations. This enables lineage tracking for debugging, auditing, and data governance.

## Approaches

Two approaches are outlined below. **Approach B (Recommended)** reuses existing Lance data structures while storing lineage separately for permanence.

---

## Approach A: New Types in CompactionMetrics

**Strategy: Extend Lance's `compact_files()` to return precise fragment mappings**

The mapping information already exists internally in Lance's `RewriteGroup` struct:
```rust
// In lance/src/dataset/optimize.rs:1004-1007
let rewrite_group = RewriteGroup {
    old_fragments: task.original_fragments.clone(),
    new_fragments: task.new_fragments.clone(),
};
```

Currently this is used for index remapping but discarded before returning. We'll extend `CompactionMetrics` to include this mapping.

### Approach A Data Structures

#### Lance (upstream changes)

```rust
// lance/src/dataset/optimize.rs

/// Mapping of source fragments to a target fragment
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct FragmentLineage {
    pub target_fragment_id: u64,
    pub source_fragment_ids: Vec<u64>,
}

/// Extended to include fragment lineage
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompactionMetrics {
    pub fragments_removed: usize,
    pub fragments_added: usize,
    pub files_removed: usize,
    pub files_added: usize,
    /// NEW: Precise mapping of which source fragments became which target fragments
    pub fragment_lineage: Vec<FragmentLineage>,
}
```

### LanceDB (consumption and persistence)

```rust
// rust/lancedb/src/table.rs

/// Single compaction event's lineage
pub struct CompactionLineageEntry {
    pub compaction_id: String,           // UUID
    pub timestamp: DateTime<Utc>,        // When compaction occurred
    pub source_version: u64,             // Table version before
    pub target_version: u64,             // Table version after
    pub fragment_mappings: Vec<FragmentLineage>,  // Precise source→target mappings
}

/// Complete lineage history
pub struct CompactionLineage {
    pub entries: Vec<CompactionLineageEntry>,  // Newest first
    pub max_entries: Option<usize>,            // Retention limit
}
```

**Storage Key**: `lancedb::compaction_lineage` in manifest config (JSON-serialized)

## Implementation Steps

### Phase 0: Lance Changes (upstream PR)

**File**: `lance/src/dataset/optimize.rs` (in Lance repo)

1. **Add `FragmentLineage` struct** (~line 188, before `CompactionMetrics`):
   ```rust
   #[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
   pub struct FragmentLineage {
       pub target_fragment_id: u64,
       pub source_fragment_ids: Vec<u64>,
   }
   ```

2. **Extend `CompactionMetrics`** (line 188):
   ```rust
   pub struct CompactionMetrics {
       // ... existing fields ...
       #[serde(default)]
       pub fragment_lineage: Vec<FragmentLineage>,
   }
   ```

3. **Populate lineage in `commit_compaction`** (~line 1002-1022):
   ```rust
   for task in completed_tasks {
       metrics += task.metrics;
       // NEW: Build lineage from the rewrite groups
       for new_frag in &task.new_fragments {
           metrics.fragment_lineage.push(FragmentLineage {
               target_fragment_id: new_frag.id,
               source_fragment_ids: task.original_fragments.iter().map(|f| f.id).collect(),
           });
       }
       // ... rest of existing code ...
   }
   ```

4. **Update Python/TypeScript bindings in Lance** to expose `fragment_lineage`

### Phase 1: LanceDB Rust Core (`rust/lancedb/src/table.rs`)

1. **Add types** (~line 3396, after `FragmentSummaryStats`):
   ```rust
   #[derive(Debug, Clone, Serialize, Deserialize)]
   pub struct CompactionLineageEntry {
       pub compaction_id: String,
       pub timestamp: DateTime<Utc>,
       pub source_version: u64,
       pub target_version: u64,
       pub fragment_mappings: Vec<lance::dataset::optimize::FragmentLineage>,
   }

   #[derive(Debug, Clone, Serialize, Deserialize, Default)]
   pub struct CompactionLineage {
       pub entries: Vec<CompactionLineageEntry>,
       pub max_entries: Option<usize>,
   }
   ```
   - Add `chrono`, `uuid` to Cargo.toml if needed

2. **Modify `compact_files`** (lines 1977-1985):
   ```rust
   async fn compact_files(&self, options: CompactionOptions, ...) -> Result<CompactionMetrics> {
       let source_version = self.version().await?;

       let mut dataset_mut = self.dataset.get_mut().await?;
       let metrics = compact_files(&mut dataset_mut, options, remap_options).await?;

       // Record lineage if fragments changed
       if !metrics.fragment_lineage.is_empty() {
           let target_version = self.version().await?;
           self.record_compaction_lineage(
               source_version,
               target_version,
               &metrics.fragment_lineage,
           ).await?;
       }

       Ok(metrics)
   }
   ```

3. **Add lineage recording** (private method on `NativeTable`):
   ```rust
   async fn record_compaction_lineage(
       &self,
       source_version: u64,
       target_version: u64,
       fragment_mappings: &[FragmentLineage],
   ) -> Result<()>
   ```
   - Read existing lineage from `manifest().config.get(LINEAGE_KEY)`
   - Prepend new entry with UUID and timestamp
   - Apply retention policy (`max_entries`)
   - Write back via `update_config()`

4. **Add public API methods**:
   ```rust
   pub async fn compaction_lineage(&self) -> Result<Option<CompactionLineage>>
   pub async fn set_lineage_retention(&self, max_entries: usize) -> Result<()>
   ```

5. **Add unit tests**:
   - `test_compaction_lineage_tracking` - verify lineage recorded after compaction
   - `test_compaction_lineage_retention` - verify old entries pruned

### Phase 2: Python Bindings

1. **`python/src/table.rs`**: Add PyO3 structs and method bindings
2. **`python/python/lancedb/_lancedb.pyi`**: Add type stubs
3. **`python/python/lancedb/table.py`**: Add to `Table` ABC, `AsyncTable`, and `LanceTable`
4. **`python/tests/test_table.py`**: Add test for lineage API

### Phase 3: TypeScript Bindings

1. **`nodejs/src/table.rs`**: Add napi structs and method
2. **`nodejs/src/table.ts`**: Add TypeScript types
3. **`nodejs/__test__/table.test.ts`**: Add test

## Key Files to Modify

### Lance (upstream)

| File | Changes |
|------|---------|
| `rust/lance/src/dataset/optimize.rs` | Add `FragmentLineage`, extend `CompactionMetrics`, populate in `commit_compaction` |
| `python/src/dataset/optimize.rs` | Expose `fragment_lineage` in Python bindings |

### LanceDB

| File | Changes |
|------|---------|
| `rust/lancedb/src/table.rs` | New types, modify `compact_files`, add `compaction_lineage()` API |
| `rust/lancedb/Cargo.toml` | Add `chrono`, `uuid` dependencies (if not present) |
| `python/src/table.rs` | PyO3 bindings for lineage types |
| `python/python/lancedb/_lancedb.pyi` | Type stubs |
| `python/python/lancedb/table.py` | Python API methods |
| `nodejs/src/table.rs` | napi bindings |

## Persistence Guarantees

- **Survives compactions**: Read-modify-write pattern preserves history
- **Survives mutations**: Append/update/delete don't touch lineage config key
- **Version restore**: Restoring old version restores its lineage state

### Approach A Dependencies

- Lance PR must be merged and LanceDB must update to new Lance version before Phase 1 can begin
- Alternative: Fork Lance locally to develop/test in parallel

---

## Approach B: Reuse FragReuseGroup Structures (Recommended)

**Strategy: Reuse existing Lance data structures, store lineage separately for permanence**

Lance already has well-designed structures for tracking fragment mappings in the `FragmentReuseIndex` system (used for deferred index remapping). We can:
1. Reuse `FragReuseGroup` and `FragDigest` types from `lance-index`
2. Always capture lineage during compaction (regardless of `defer_index_remap` setting)
3. Store in table config for permanent retention (unlike FragReuseIndex which gets trimmed)

### Why This Approach

| Aspect | Approach A | Approach B (Recommended) |
|--------|------------|--------------------------|
| New Lance types | Yes (`FragmentLineage`) | No (reuse existing) |
| Lance PR complexity | Medium | Minimal |
| Type consistency | New parallel hierarchy | Unified with existing |
| Storage | Table config | Table config |
| Trimming | Never | Never |

### Existing Lance Structures to Reuse

Located in `lance-index/src/frag_reuse.rs`:

```rust
/// Digest of a fragment's key properties
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FragDigest {
    pub id: u64,
    pub physical_rows: usize,
    pub num_deleted_rows: usize,
}

/// A group of fragments that were rewritten together
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FragReuseGroup {
    pub changed_row_addrs: Vec<u8>,  // Can be empty for lineage-only use
    pub old_frags: Vec<FragDigest>,  // Source fragments
    pub new_frags: Vec<FragDigest>,  // Target fragments
}
```

### Approach B Data Structures

#### Lance (minimal upstream changes)

```rust
// lance/src/dataset/optimize.rs

// Extend CompactionMetrics to include reuse groups
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompactionMetrics {
    pub fragments_removed: usize,
    pub fragments_added: usize,
    pub files_removed: usize,
    pub files_added: usize,
    /// NEW: Fragment rewrite groups (reuses existing FragReuseGroup type)
    #[serde(default)]
    pub rewrite_groups: Vec<FragReuseGroup>,
}
```

#### LanceDB (consumption and persistence)

```rust
// rust/lancedb/src/table.rs

use lance_index::frag_reuse::{FragDigest, FragReuseGroup};

/// Single compaction event's lineage
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompactionLineageEntry {
    pub compaction_id: String,           // UUID
    pub timestamp: DateTime<Utc>,        // When compaction occurred
    pub source_version: u64,             // Table version before
    pub target_version: u64,             // Table version after
    pub rewrite_groups: Vec<FragReuseGroup>,  // Reuse existing type
}

/// Complete lineage history
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct CompactionLineage {
    pub entries: Vec<CompactionLineageEntry>,  // Newest first
    pub max_entries: Option<usize>,            // Retention limit
}
```

**Storage Key**: `lancedb::compaction_lineage` in manifest config (JSON-serialized)

### Approach B Implementation Steps

#### Phase 0: Lance Changes (minimal upstream PR)

**File**: `lance/src/dataset/optimize.rs`

1. **Import FragReuseGroup** (if not already imported for all code paths):
   ```rust
   use lance_index::frag_reuse::FragReuseGroup;
   ```

2. **Extend `CompactionMetrics`** (line ~188):
   ```rust
   pub struct CompactionMetrics {
       // ... existing fields ...
       #[serde(default)]
       pub rewrite_groups: Vec<FragReuseGroup>,
   }
   ```

3. **Always populate rewrite_groups in `commit_compaction`** (~line 1002):
   ```rust
   for task in completed_tasks {
       metrics += task.metrics;

       // NEW: Always capture rewrite groups for lineage
       metrics.rewrite_groups.push(FragReuseGroup {
           changed_row_addrs: vec![],  // Empty - not needed for lineage
           old_frags: task.original_fragments.iter().map(|f| f.into()).collect(),
           new_frags: task.new_fragments.iter().map(|f| f.into()).collect(),
       });

       // ... existing defer_index_remap logic unchanged ...
   }
   ```

4. **Re-export types** from lance for LanceDB consumption:
   ```rust
   pub use lance_index::frag_reuse::{FragDigest, FragReuseGroup};
   ```

#### Phase 1: LanceDB Rust Core (`rust/lancedb/src/table.rs`)

1. **Add types** (~line 3396):
   ```rust
   use lance::dataset::optimize::{FragDigest, FragReuseGroup};

   #[derive(Debug, Clone, Serialize, Deserialize)]
   pub struct CompactionLineageEntry {
       pub compaction_id: String,
       pub timestamp: DateTime<Utc>,
       pub source_version: u64,
       pub target_version: u64,
       pub rewrite_groups: Vec<FragReuseGroup>,
   }

   #[derive(Debug, Clone, Serialize, Deserialize, Default)]
   pub struct CompactionLineage {
       pub entries: Vec<CompactionLineageEntry>,
       pub max_entries: Option<usize>,
   }
   ```

2. **Modify `compact_files`** (lines 1977-1985):
   ```rust
   async fn compact_files(&self, options: CompactionOptions, ...) -> Result<CompactionMetrics> {
       let source_version = self.version().await?;

       let mut dataset_mut = self.dataset.get_mut().await?;
       let metrics = compact_files(&mut dataset_mut, options, remap_options).await?;

       // Record lineage if fragments changed
       if !metrics.rewrite_groups.is_empty() {
           let target_version = self.version().await?;
           self.record_compaction_lineage(
               source_version,
               target_version,
               &metrics.rewrite_groups,
           ).await?;
       }

       Ok(metrics)
   }
   ```

3. **Add lineage recording** (private method on `NativeTable`):
   ```rust
   async fn record_compaction_lineage(
       &self,
       source_version: u64,
       target_version: u64,
       rewrite_groups: &[FragReuseGroup],
   ) -> Result<()>
   ```

4. **Add public API methods** (same as Approach A)

5. **Add unit tests** (same as Approach A)

#### Phase 2-3: Bindings (same as Approach A)

Python and TypeScript bindings follow the same pattern, but expose `FragDigest` and use `rewrite_groups` instead of `fragment_mappings`.

### Approach B Key Files to Modify

#### Lance (upstream)

| File | Changes |
|------|---------|
| `rust/lance/src/dataset/optimize.rs` | Add `rewrite_groups` field to `CompactionMetrics`, populate in `commit_compaction` |
| `rust/lance/src/lib.rs` | Re-export `FragDigest`, `FragReuseGroup` |

#### LanceDB

| File | Changes |
|------|---------|
| `rust/lancedb/src/table.rs` | Import Lance types, add `CompactionLineageEntry`/`CompactionLineage`, modify `compact_files` |
| `python/src/table.rs` | PyO3 bindings wrapping Lance types |
| `python/python/lancedb/_lancedb.pyi` | Type stubs |
| `python/python/lancedb/table.py` | Python API methods |
| `nodejs/src/table.rs` | napi bindings |

### Approach B Advantages

1. **Consistency**: Uses same types as `FragmentReuseIndex` - familiar to Lance maintainers
2. **Richer metadata**: `FragDigest` includes `physical_rows` and `num_deleted_rows`
3. **Simpler Lance PR**: Just adds a field and populates it; no new type definitions
4. **Future compatibility**: If Lance ever exposes lineage natively, easy to migrate

---

## Python API Definition

### Type Stubs (`python/python/lancedb/_lancedb.pyi`)

#### Approach B Types (Recommended)

```python
from typing import List, Optional
from datetime import datetime

class FragDigest:
    """Digest of a fragment's key properties."""
    @property
    def id(self) -> int:
        """The fragment ID."""
        ...

    @property
    def physical_rows(self) -> int:
        """Number of physical rows in the fragment."""
        ...

    @property
    def num_deleted_rows(self) -> int:
        """Number of deleted rows in the fragment."""
        ...

class FragReuseGroup:
    """A group of fragments that were rewritten together during compaction."""
    @property
    def old_frags(self) -> List[FragDigest]:
        """The source fragments that were merged."""
        ...

    @property
    def new_frags(self) -> List[FragDigest]:
        """The new fragments that were created."""
        ...

class CompactionLineageEntry:
    """Record of a single compaction operation."""
    @property
    def compaction_id(self) -> str:
        """Unique identifier (UUID) for this compaction event."""
        ...

    @property
    def timestamp(self) -> datetime:
        """When the compaction occurred (UTC)."""
        ...

    @property
    def source_version(self) -> int:
        """Table version before compaction."""
        ...

    @property
    def target_version(self) -> int:
        """Table version after compaction."""
        ...

    @property
    def rewrite_groups(self) -> List[FragReuseGroup]:
        """Groups of fragments that were rewritten together."""
        ...

class CompactionLineage:
    """Complete compaction lineage history for a table."""
    @property
    def entries(self) -> List[CompactionLineageEntry]:
        """List of compaction events, newest first."""
        ...

    @property
    def max_entries(self) -> Optional[int]:
        """Maximum entries to retain (None = unlimited)."""
        ...
```

### Table Methods (`python/python/lancedb/table.py`)

```python
from typing import Optional

class Table(ABC):
    """Abstract base class for LanceDB tables."""

    @abstractmethod
    def compaction_lineage(self) -> Optional[CompactionLineage]:
        """
        Get the compaction lineage history for this table.

        Returns the history of fragment merges that occurred during compaction
        operations. Each entry shows which fragments were merged into which
        new fragments, along with version and timestamp information.

        Returns
        -------
        Optional[CompactionLineage]
            The lineage history, or None if no compactions have been recorded.

        Examples
        --------
        >>> lineage = table.compaction_lineage()
        >>> if lineage:
        ...     for entry in lineage.entries:
        ...         print(f"Compaction at {entry.timestamp}")
        ...         for group in entry.rewrite_groups:
        ...             old_ids = [f.id for f in group.old_frags]
        ...             new_ids = [f.id for f in group.new_frags]
        ...             print(f"  {old_ids} -> {new_ids}")
        """
        ...

    @abstractmethod
    def set_lineage_retention(self, max_entries: int) -> None:
        """
        Configure the maximum number of compaction lineage entries to retain.

        Older entries beyond this limit will be removed. This helps manage
        storage overhead for tables with frequent compactions.

        Parameters
        ----------
        max_entries : int
            Maximum number of lineage entries to keep. Must be positive.

        Examples
        --------
        >>> # Keep only the last 50 compaction records
        >>> table.set_lineage_retention(50)
        """
        ...


class AsyncTable:
    """Async implementation of Table."""

    async def compaction_lineage(self) -> Optional[CompactionLineage]:
        """Get the compaction lineage history for this table."""
        return await self._inner.compaction_lineage()

    async def set_lineage_retention(self, max_entries: int) -> None:
        """Configure the maximum number of lineage entries to retain."""
        await self._inner.set_lineage_retention(max_entries)


class LanceTable(Table):
    """Synchronous wrapper around AsyncTable."""

    def compaction_lineage(self) -> Optional[CompactionLineage]:
        """Get the compaction lineage history for this table."""
        return LOOP.run(self._table.compaction_lineage())

    def set_lineage_retention(self, max_entries: int) -> None:
        """Configure the maximum number of lineage entries to retain."""
        LOOP.run(self._table.set_lineage_retention(max_entries))
```

### PyO3 Bindings (`python/src/table.rs`)

#### Approach B (Recommended)

```rust
#[pyclass(get_all)]
#[derive(Clone, Debug)]
pub struct FragDigest {
    pub id: u64,
    pub physical_rows: usize,
    pub num_deleted_rows: usize,
}

#[pyclass(get_all)]
#[derive(Clone, Debug)]
pub struct FragReuseGroup {
    pub old_frags: Vec<FragDigest>,
    pub new_frags: Vec<FragDigest>,
}

#[pyclass(get_all)]
#[derive(Clone, Debug)]
pub struct CompactionLineageEntry {
    pub compaction_id: String,
    pub timestamp: String,  // ISO 8601 format
    pub source_version: u64,
    pub target_version: u64,
    pub rewrite_groups: Vec<FragReuseGroup>,
}

#[pyclass(get_all)]
#[derive(Clone, Debug)]
pub struct CompactionLineage {
    pub entries: Vec<CompactionLineageEntry>,
    pub max_entries: Option<usize>,
}

#[pymethods]
impl Table {
    pub fn compaction_lineage<'py>(self_: PyRef<'py, Self>) -> PyResult<Bound<'py, PyAny>> {
        let inner = self_.inner_ref()?.clone();
        future_into_py(self_.py(), async move {
            let native = inner.as_native().ok_or_else(|| {
                PyRuntimeError::new_err("compaction_lineage is only supported on native tables")
            })?;
            match native.compaction_lineage().await.infer_error()? {
                Some(lineage) => Ok(Some(CompactionLineage::from(lineage))),
                None => Ok(None),
            }
        })
    }

    pub fn set_lineage_retention<'py>(
        self_: PyRef<'py, Self>,
        max_entries: usize,
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self_.inner_ref()?.clone();
        future_into_py(self_.py(), async move {
            let native = inner.as_native().ok_or_else(|| {
                PyRuntimeError::new_err("set_lineage_retention is only supported on native tables")
            })?;
            native.set_lineage_retention(max_entries).await.infer_error()?;
            Ok(())
        })
    }
}
```

## Example Usage

### Approach B (Recommended)

```python
import lancedb

db = lancedb.connect("./my_db")
table = db.open_table("my_table")

# After some data operations and compaction...
table.compact_files()

# Retrieve lineage
lineage = table.compaction_lineage()
if lineage:
    print(f"Found {len(lineage.entries)} compaction events")

    for entry in lineage.entries:
        print(f"\nCompaction {entry.compaction_id}")
        print(f"  Time: {entry.timestamp}")
        print(f"  Version: {entry.source_version} → {entry.target_version}")

        for group in entry.rewrite_groups:
            # Access rich fragment metadata
            old_ids = [f.id for f in group.old_frags]
            new_ids = [f.id for f in group.new_frags]
            old_rows = sum(f.physical_rows for f in group.old_frags)
            new_rows = sum(f.physical_rows for f in group.new_frags)
            print(f"  Fragments {old_ids} ({old_rows} rows) → {new_ids} ({new_rows} rows)")

# Configure retention to keep last 100 compaction records
table.set_lineage_retention(100)
```
