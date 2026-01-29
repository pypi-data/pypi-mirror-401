# Execution Modes

**Date:** 2026-01-13  
**Status:** ✅ **IMPLEMENTED**

---

## Overview

THRESHOLD_ONSET supports two execution modes:

1. **Single-Run Mode**: Standard execution with one Phase 0 run
2. **Multi-Run Mode**: Multiple Phase 0 runs to test persistence across independent contexts

---

## Configuration

In `main.py`, configure execution mode:

```python
VARIANT = "finite"  # Action variant to use
MULTI_RUN_MODE = True  # Set to True for multi-run, False for single-run
NUM_RUNS = 5  # Number of runs (only used if MULTI_RUN_MODE = True)
```

---

## Single-Run Mode

**Purpose:** Standard execution for testing individual runs.

**Flow:**
1. Run Phase 0 once with selected variant
2. Run Phase 1 on residues
3. Run Phase 2 on residues + Phase 1 metrics
4. Run Phase 3 on residues + Phase 1 metrics + Phase 2 metrics

**Use Case:** Testing action variants, debugging, single-run analysis.

**Limitation:** Cannot detect cross-run persistence (persistent_segments = 0 expected).

---

## Multi-Run Mode

**Purpose:** Test persistence across multiple independent Phase 0 runs.

**Flow:**
1. Run Phase 0 N times (same variant, independent runs)
2. Run Phase 1 on each run's residues
3. Run Phase 2 (multi-run) on all residue sequences + Phase 1 metrics
4. Run Phase 3 on first run's residues + Phase 1 metrics + Phase 2 metrics

**Use Case:** Testing persistence, identity survival, cross-context stability.

**Advantage:** Enables detection of persistent segments across runs.

---

## Phase 2 Differences

### Single-Run Phase 2 (`run_phase2`)
- Tests persistence within a single sequence
- Uses `phase2()` function
- Limited to repeatability within one run
- Cannot detect cross-run persistence

### Multi-Run Phase 2 (`run_phase2_multi_run`)
- Tests persistence across multiple runs
- Uses `phase2_multi_run()` function
- Detects segments that appear in multiple runs
- Enables persistent_segment_hashes > 0

---

## Expected Results

### Single-Run Mode
- **Phase 0**: Collision rate varies by variant
- **Phase 1**: Repetition count > 0 (with finite variant)
- **Phase 2**: Repeatable units > 0, persistent segments = 0
- **Phase 3**: Nodes > 0, edges = 0 (no stable relations)

### Multi-Run Mode
- **Phase 0**: Same as single-run (repeated N times)
- **Phase 1**: Same as single-run (repeated N times)
- **Phase 2**: Repeatable units > 0, **persistent segments > 0**
- **Phase 3**: Nodes > 0, **edges > 0** (stable relations emerge)

---

## When to Use Each Mode

**Use Single-Run Mode when:**
- Testing new action variants
- Debugging individual phases
- Quick validation
- Understanding single-run behavior

**Use Multi-Run Mode when:**
- Testing persistence
- Validating identity survival
- Testing cross-context stability
- Full system validation

---

## Implementation Details

### Multi-Run Persistence Detection

Multi-run mode enables Phase 2 to:
1. Compare segments across multiple runs
2. Identify segments that appear in 2+ runs
3. Assign identity hashes to persistent segments
4. Measure cluster stability across runs

This is the **only way** to detect true persistence in the current system.

---

## Notes

- Both modes respect all phase gates
- Both modes maintain Phase 0 compliance
- Multi-run mode requires more computation
- Multi-run mode is necessary for persistence detection
- Single-run mode is sufficient for repeatability testing

---

## Future Enhancements

Potential improvements:
- Configurable NUM_RUNS via command-line
- Parallel execution of multiple runs
- Statistical aggregation across runs
- Adaptive run count based on convergence
