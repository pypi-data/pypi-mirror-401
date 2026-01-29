# Warpdatasets - Issues To Fix

## Critical Issues

### 1. Local Raw Data Paths Lost After Publish (FIXED)
**Severity:** Critical
**Status:** Fixed

After publishing a dataset with `--upload` or to S3, the manifest points to S3 URIs. Even though the user has the raw data locally, warpdata cannot use it - it must re-download from S3.

**Fix applied:**
- Publish now automatically saves local artifact paths to `~/.warpdata/local_sources.json`
- Resolver checks local sources first before downloading from S3
- Zero user action required - local paths are preserved automatically

**Also added `warpdata link` command for manual overrides:**
```bash
warpdata link vision/celeba --artifact image=/path/to/img_align_celeba
warpdata link --show
```

**Files changed:**
- `warpdata/cli/commands/publish.py` - auto-save local sources during publish
- `warpdata/cli/commands/link.py` (new) - manual override command
- `warpdata/artifacts/resolver.py` - check local sources first

---

### 2. Cache Organized by Version, Not Content Hash
**Severity:** High
**Status:** Open

The data cache is organized by dataset version hash:
```
~/.warpdata/data/{workspace}/{name}/{version}/objects/...
```

When a dataset version changes (e.g., parquet table update), all artifacts must be re-downloaded even if unchanged.

**Expected behavior:**
- Artifacts cached by content hash (SHA256)
- Same artifact shard reused across versions
- `~/.warpdata/data/objects/{hash[:2]}/{hash[2:4]}/{hash}`

**Current behavior:**
- Each version has its own cache directory
- Republishing dataset requires re-downloading all artifacts

**Files involved:**
- `warpdata/cli/commands/sync.py`
- `warpdata/artifacts/resolver.py`

---

## High Priority Issues

### 3. Filter Parameter Missing from batch_dicts()
**Severity:** High
**Status:** Open

`Table.batch_dicts()` does not support a `filter` parameter for row-level filtering.

**Expected behavior:**
```python
for batch in table.batch_dicts(filter=lambda row: row['split'] == 'train'):
    ...
```

**Current behavior:**
```
TypeError: Table.batch_dicts() got an unexpected keyword argument 'filter'
```

**Files involved:** `warpdata/core/table.py`

---

### 4. Sync Pull Fails for Local-Only Datasets
**Severity:** Medium
**Status:** Open

`warpdata sync pull` fails with "Dataset not found on S3" for datasets that were registered locally but never uploaded.

```bash
$ warpdata sync pull ml/arcagi
Error: Dataset not found on S3: ml/arcagi
```

**Expected behavior:**
- Should recognize this is a local-only dataset
- Or provide clear error message explaining the dataset is local-only

**Files involved:** `warpdata/cli/commands/sync.py`

---

## Medium Priority Issues

### 5. Mode Configuration Was Confusing (FIXED)
**Severity:** Medium
**Status:** Fixed

The mode options (strict/hybrid/local/remote/auto) were confusing.

**Fix applied:**
- Default mode changed from `strict` to `hybrid`
- `hybrid` = local-first, S3 fallback with caching (what users expect)
- `auto` now behaves same as `hybrid`

**Files changed:**
- `warpdata/config/settings.py`
- `warpdata/artifacts/resolver.py`

---

### 6. No Cache Status Per-Dataset
**Severity:** Medium
**Status:** Open

`warpdata cache status` shows global cache stats, but no way to see cache status per-dataset.

**Expected:**
```bash
$ warpdata cache show vision/vesuvius-scrolls
Cached: 7/9 shards (21.5 GB / 25.6 GB)
Missing: train_labels (866 MB), test_images (1.2 GB)
```

**Files involved:** `warpdata/cli/commands/cache.py`

---

### 7. Vesuvius Dataset Had Wrong File Extensions (FIXED)
**Severity:** Medium
**Status:** Fixed

The vesuvius-scrolls dataset had `train_labels` refs with `.png` extension but actual files were `.tif`.

**Fix applied:**
- Republished dataset with correct `.tif` extensions in parquet
- New version: `652524762464`

---

## Low Priority Issues

### 8. to_pandas() Slow for Large Datasets
**Severity:** Low
**Status:** Open

`to_pandas()` for 300k+ rows takes 10+ seconds. May need streaming/chunked loading.

---

### 9. Error Messages Could Be Clearer
**Severity:** Low
**Status:** Partially Fixed

Some error messages were cryptic (e.g., "Unsupported URI scheme: s3" instead of explaining the shard isn't cached).

**Fix applied:** Added clearer error in resolver for remote tar_shards without local cache.

---

## Feature Requests

### F1. Add `warpdata link` Command (IMPLEMENTED)
Allow re-linking artifacts to local paths:
```bash
warpdata link vision/celeba --artifact image=/path/to/img_align_celeba
```
**Status:** Implemented (see Issue #1 fix)

### F2. Content-Addressed Global Cache
Store all shards by content hash, not per-version:
```
~/.warpdata/objects/{hash[:2]}/{hash[2:4]}/{hash}
```

### F3. Publish Without Upload
Allow `warpdata publish --local-only` to create manifests with `local://` or `file://` URIs that reference local files directly.

### F4. Dataset Cloning/Forking
```bash
warpdata clone vision/celeba my-celeba --local
```

---

## Summary

| Issue | Severity | Status |
|-------|----------|--------|
| Local paths lost after publish | Critical | Fixed |
| Cache by version not content | High | Open |
| No filter in batch_dicts | High | Open |
| Sync pull fails for local datasets | Medium | Open |
| Mode confusion | Medium | Fixed |
| No per-dataset cache status | Medium | Open |
| Vesuvius wrong extensions | Medium | Fixed |
| to_pandas slow | Low | Open |
| Error messages unclear | Low | Partial |
