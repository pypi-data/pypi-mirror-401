# THRESHOLD_ONSET

**Phase 0: Action before Knowledge**

कार्य (kārya) happens before ज्ञान (jñāna)

---

## What This Is

A foundational system exploring structure emergence through action, trace, and repetition — **before symbols, meaning, or interpretation**.

**Status:** All phases (0-4) **FROZEN** — foundational construction complete.

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/chavalasantosh/THRESHOLDONSET.git
cd THRESHOLDONSET

# Install dependencies (optional - only for version control tools)
pip install -r requirements.txt
```

**Note:** Core system uses **Python standard library only**. Dependencies are only for optional version control tools.

### Run the System

```bash
python main.py
```

This executes all phases:
1. **Phase 0** (THRESHOLD_ONSET) - Action → residue
2. **Phase 1** (SEGMENTATION) - Boundaries without identity
3. **Phase 2** (IDENTITY) - Identity survives across runs
4. **Phase 3** (RELATION) - Relations persist and stabilize
5. **Phase 4** (SYMBOL) - Pure aliasing layer

### Configuration

Edit `main.py` to configure:

```python
VARIANT = "finite"          # Action variant (see below)
MULTI_RUN_MODE = True       # Multi-run persistence testing
NUM_RUNS = 5                # Number of independent runs
```

**Action Variants:**
- `"noise_baseline"` - Pure random (frozen baseline)
- `"inertia"` - Temporal correlation
- `"random_walk"` - Bounded random walk
- `"oscillator"` - Bounded oscillator
- `"decay_noise"` - Decay toward target + noise
- `"finite"` - Discrete but meaningless (enables exact equality)

See [`docs/EXECUTION_MODES.md`](docs/EXECUTION_MODES.md) for details.

---

## What This System Does (Simple Explanation)

**Think of it like ocean waves:**

1. **Waves appear** (Phase 0: things just happen)
2. **Waves form patterns** (Phase 1: patterns emerge)
3. **You recognize the same wave pattern** (Phase 2: identity persists)
4. **Waves influence each other** (Phase 3: relations connect)
5. **You give names to patterns** (Phase 4: pure aliasing)

**All of this happens BEFORE anyone says "this is a wave" or "this pattern is called 'swell'".**

The system works **exactly like nature works** - structure emerges before language exists.

**For a complete non-technical explanation, see:** [`docs/simple/PHASE0_TO_PHASE3_STORY.md`](docs/simple/PHASE0_TO_PHASE3_STORY.md)

---

## Phase-by-Phase Guide

### Phase 0: THRESHOLD_ONSET (FROZEN FOREVER)

**Purpose:** Prove action can exist without knowledge.

**What it does:**
- Executes structured but meaningless actions
- Produces opaque, structureless residues
- Counts repetitions and collisions

**Outputs:**
- Total residue count
- Unique residue count
- Collision rate

**Status:** ✅ **FROZEN FOREVER** - Action → residue proven

**Freeze Declaration:** [`src/phase0/phase0/PHASE0_FREEZE.md`](src/phase0/phase0/PHASE0_FREEZE.md)

**Key Constraints:**
- ✅ Allowed: Action, residue, repetition, persistence (counts only)
- ❌ Forbidden: Symbols, labels, meaning, interpretation, visualization

---

### Phase 1: SEGMENTATION (FROZEN FOREVER)

**Purpose:** Detect boundaries and patterns without naming them.

**What it does:**
- Detects boundaries in residue sequences (indices only)
- Clusters residues (counts only)
- Measures distances (raw numbers)
- Detects patterns (counts only)

**Outputs:**
- Boundary positions (indices)
- Cluster count and sizes
- Distance measurements
- Repetition count
- Survival count

**Status:** ✅ **FROZEN FOREVER** - Boundaries without identity

**Freeze Declaration:** [`src/phase1/phase1/PHASE1_FREEZE.md`](src/phase1/phase1/PHASE1_FREEZE.md)

**Key Constraints:**
- ✅ Allowed: Boundary detection, clustering, distance measurement, pattern detection
- ❌ Forbidden: Names, labels, symbols, interpretation, visualization

---

### Phase 2: IDENTITY (FROZEN FOREVER)

**Purpose:** Recognize persistent identities without naming them.

**What it does:**
- Measures persistence across multiple runs
- Detects repeatable units
- Assigns identity hashes (internal only)
- Measures stability

**Outputs:**
- Persistent segment hashes
- Identity mappings (hash-based)
- Repeatability counts
- Stability metrics

**Status:** ✅ **FROZEN FOREVER** - Identity survives across runs

**Freeze Declaration:** [`src/phase2/phase2/PHASE2_FREEZE.md`](src/phase2/phase2/PHASE2_FREEZE.md)

**Key Constraints:**
- ✅ Allowed: Persistence measurement, repeatable units, identity hashes (internal)
- ❌ Forbidden: Symbolic naming, linguistic labels, meaning, interpretation

**Note:** Requires multi-run mode to detect cross-run persistence.

---

### Phase 3: RELATION (FROZEN FOREVER)

**Purpose:** Detect how identities connect without naming the connections.

**What it does:**
- Constructs graph structures (hash pairs only)
- Detects interactions, dependencies, influences
- Measures relation persistence across runs
- Measures relation stability

**Outputs:**
- Graph nodes and edges (counts)
- Persistent relation hashes
- Stability ratio
- Edge density variance
- Common edges ratio

**Status:** ✅ **FROZEN FOREVER** - Relations persist and stabilize

**Freeze Declaration:** [`src/phase3/phase3/PHASE3_FREEZE.md`](src/phase3/phase3/PHASE3_FREEZE.md)

**Key Constraints:**
- ✅ Allowed: Graph construction, interaction detection, dependency measurement
- ❌ Forbidden: Symbolic naming, linguistic labels, graph visualization, meaning

**Validation:** Convergence tests passed (see [`test_phase3_convergence.py`](test_phase3_convergence.py))

---

### Phase 4: SYMBOL (FROZEN FOREVER)

**Purpose:** Create pure aliasing layer - reversible symbol mappings.

**What it does:**
- Assigns integer symbols to persistent identities
- Assigns integer symbols to persistent relations
- Creates reversible lookup tables (both directions)
- Adds zero new structure

**Outputs:**
- Identity alias count
- Relation alias count

**Status:** ✅ **FROZEN FOREVER** - Pure aliasing, reversible

**Freeze Declaration:** [`src/phase4/phase4/PHASE4_FREEZE.md`](src/phase4/phase4/PHASE4_FREEZE.md)

**Key Constraints:**
- ✅ Allowed: Integer symbols only (0, 1, 2, 3...), reversible mappings
- ❌ Forbidden: Meaning, interpretation, structural modification, symbol sequences

**Critical Rule:** Removing Phase 4 restores Phase 3 exactly (bit-for-bit, no recomputation).

**Validation:** Freeze validation tests passed (see [`test_phase4_freeze.py`](test_phase4_freeze.py))

---

## Understanding Outputs

### Phase 0 Output Example

```
THRESHOLD_ONSET — Phase 0 (Finite Variant)

Total residue count:     200
Unique residue count:     10
Collision rate:           0.9500
```

**What this means:**
- 200 actions produced 200 residues
- Only 10 unique values (high reuse)
- 95% collision rate (same values repeat)

### Phase 1 Output Example

```
THRESHOLD_ONSET — Phase 1

Boundary positions:       [1, 2, 3, ...]
Cluster count:             10
Repetition count:          362
Survival count:            0
```

**What this means:**
- Boundaries detected at specific positions (indices)
- 10 clusters found
- 362 repetitions detected
- No survival across runs (single-run mode)

### Phase 2 Output Example (Multi-Run)

```
THRESHOLD_ONSET — Phase 2 (Multi-Run)

Persistent segments:       99
Identity mappings:          99
Repeatable units:           99
```

**What this means:**
- 99 segments persist across multiple runs
- 99 identities assigned (hash-based, internal)
- 99 repeatable units detected

### Phase 3 Output Example

```
THRESHOLD_ONSET — Phase 3 (Multi-Run)

Node count:                 201
Edge count:                  4950
Persistent relations:        5960
Stability ratio:             1.0000
```

**What this means:**
- 201 nodes in relation graph
- 4950 edges (connections)
- 5960 relations persist across runs
- Perfect stability (1.0 = no variance)

### Phase 4 Output Example

```
THRESHOLD_ONSET — Phase 4 (Multi-Run)

Identity alias count:       99
Relation alias count:        5960
```

**What this means:**
- 99 identities have integer aliases
- 5960 relations have integer aliases
- Pure aliasing (no structure added)

---

## Project Structure

```
THRESHOLD_ONSET/
├── main.py                          # Entry point
├── README.md                        # This file
├── requirements.txt                 # Dependencies (optional)
│
├── src/                             # Source code
│   ├── phase0/                      # Phase 0 (FROZEN)
│   │   ├── phase0.py                # Core pipeline
│   │   ├── actions.py               # Action variants
│   │   └── phase0/                  # Phase 0 documentation
│   ├── phase1/                      # Phase 1 (FROZEN)
│   │   ├── phase1.py                # Segmentation pipeline
│   │   ├── boundary.py              # Boundary detection
│   │   ├── cluster.py               # Clustering
│   │   ├── distance.py              # Distance measurement
│   │   └── pattern.py               # Pattern detection
│   ├── phase2/                      # Phase 2 (FROZEN)
│   │   ├── phase2.py                # Identity pipeline
│   │   ├── persistence.py           # Persistence measurement
│   │   ├── repeatable.py            # Repeatable units
│   │   ├── identity.py               # Identity hashes
│   │   └── stability.py             # Stability metrics
│   ├── phase3/                      # Phase 3 (FROZEN)
│   │   ├── phase3.py                 # Relation pipeline
│   │   ├── relation.py               # Relation extraction
│   │   ├── persistence.py           # Relation persistence
│   │   ├── stability.py             # Relation stability
│   │   ├── graph.py                 # Graph construction
│   │   ├── interaction.py           # Interaction detection
│   │   ├── dependency.py             # Dependency measurement
│   │   └── influence.py             # Influence metrics
│   ├── phase4/                      # Phase 4 (FROZEN)
│   │   ├── phase4.py                # Symbol pipeline
│   │   ├── alias.py                 # Alias assignment
│   │   └── phase4/                   # Phase 4 documentation
│   └── tools/                        # Version control tools
│       ├── version_control.py
│       └── watch_version.py
│
├── docs/                            # Project documentation
│   ├── axioms/                      # Core design constraints
│   ├── architecture/                # System architecture
│   ├── simple/                      # Non-technical explanations
│   ├── history/                     # Project history
│   └── README.md                    # Documentation overview
│
├── test_phase3_convergence.py       # Phase 3 validation test
├── test_phase4_freeze.py            # Phase 4 validation test
│
└── versions/                        # Version snapshots (auto)
```

---

## Documentation

### Core Documentation

- **Axioms:** [`docs/axioms/AXIOMS.md`](docs/axioms/AXIOMS.md) - Non-negotiable design constraints
- **Architecture:** [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) - System architecture
- **Phase Status:** [`docs/PHASE_STATUS_CANONICAL.md`](docs/PHASE_STATUS_CANONICAL.md) - Authoritative phase status

### Simple Explanations (Non-Technical)

- **Complete Story:** [`docs/simple/PHASE0_TO_PHASE3_STORY.md`](docs/simple/PHASE0_TO_PHASE3_STORY.md) - What we built (for everyone)
- **Independence Check:** [`docs/simple/INDEPENDENCE_CHECK.md`](docs/simple/INDEPENDENCE_CHECK.md) - Why Phase 4 is safe

### Phase Documentation

Each phase has its own documentation:
- **Phase 0:** `src/phase0/phase0/docs/`
- **Phase 1:** `src/phase1/phase1/`
- **Phase 2:** `src/phase2/phase2/`
- **Phase 3:** `src/phase3/phase3/`
- **Phase 4:** `src/phase4/phase4/`

### Freeze Declarations

All phases are frozen with official declarations:
- **Phase 0:** [`src/phase0/phase0/PHASE0_FREEZE.md`](src/phase0/phase0/PHASE0_FREEZE.md)
- **Phase 1:** [`src/phase1/phase1/PHASE1_FREEZE.md`](src/phase1/phase1/PHASE1_FREEZE.md)
- **Phase 2:** [`src/phase2/phase2/PHASE2_FREEZE.md`](src/phase2/phase2/PHASE2_FREEZE.md)
- **Phase 3:** [`src/phase3/phase3/PHASE3_FREEZE.md`](src/phase3/phase3/PHASE3_FREEZE.md)
- **Phase 4:** [`src/phase4/phase4/PHASE4_FREEZE.md`](src/phase4/phase4/PHASE4_FREEZE.md)

---

## Testing & Validation

### Phase 3 Convergence Test

Validates Phase 3 stability across multiple run counts:

```bash
python test_phase3_convergence.py
```

**What it tests:**
- Gate passes consistently
- Stability ratio stays ≥ threshold
- Metrics converge (no drift)
- No flaky behavior

### Phase 4 Freeze Validation

Validates Phase 4 freeze-worthiness:

```bash
python test_phase4_freeze.py
```

**What it tests:**
- Determinism (same inputs → same outputs)
- Reversibility (removing Phase 4 restores Phase 3)
- Immutability (aliases never change)
- Gate determinism (gate never flakes)

---

## Version Control

The project includes a local version control system (optional):

```bash
python src/tools/watch_version.py
```

**Features:**
- File watching with `watchfiles`
- Content hashing with SHA256
- SQLite metadata storage
- Unified diffs between versions

See [`src/tools/docs/VERSION_CONTROL.md`](src/tools/docs/VERSION_CONTROL.md) for details.

---

## Code Standards

- **Python standard library only** (except optional version control tools)
- **Clean, minimal code**
- **Phase boundaries strictly enforced**
- **Each phase operates independently**
- **Documentation co-located with code**

---

## Philosophy

**Core Axiom:**

> कार्य (kārya) happens before ज्ञान (jñāna)
>
> Function stabilizes before knowledge appears.

**What this means:**

- Action exists before meaning
- Structure emerges before language
- Patterns form before names
- Identity persists before symbols
- Relations connect before interpretation

**The system proves:**

- Things can exist and work together **BEFORE** anyone gives them names
- Structure emerges naturally through action and repetition
- Identity and relations are discovered, not created
- Symbols are pure aliases - reversible, meaningless labels

---

## Current Status

**All Phases: FROZEN FOREVER**

| Phase | Name | Status | Freeze Declaration |
|-------|------|--------|-------------------|
| Phase 0 | THRESHOLD_ONSET | ✅ FROZEN | [`src/phase0/phase0/PHASE0_FREEZE.md`](src/phase0/phase0/PHASE0_FREEZE.md) |
| Phase 1 | SEGMENTATION | ✅ FROZEN | [`src/phase1/phase1/PHASE1_FREEZE.md`](src/phase1/phase1/PHASE1_FREEZE.md) |
| Phase 2 | IDENTITY | ✅ FROZEN | [`src/phase2/phase2/PHASE2_FREEZE.md`](src/phase2/phase2/PHASE2_FREEZE.md) |
| Phase 3 | RELATION | ✅ FROZEN | [`src/phase3/phase3/PHASE3_FREEZE.md`](src/phase3/phase3/PHASE3_FREEZE.md) |
| Phase 4 | SYMBOL | ✅ FROZEN | [`src/phase4/phase4/PHASE4_FREEZE.md`](src/phase4/phase4/PHASE4_FREEZE.md) |

**System:** ✅ **FOUNDATION COMPLETE**

All phases have been validated, frozen, and documented. The foundational construction is complete.

---

## What's Next?

**The foundational system is complete.** All phases (0-4) are frozen and validated.

Any work beyond Phase 4 would be a **new project**, not a continuation of THRESHOLD_ONSET.

**Possible directions:**
- Language emergence (Phase 5+)
- Meaning assignment
- Interpretation layers
- Application-specific extensions

**But these are separate projects** - THRESHOLD_ONSET has proven its point: structure exists before language.

---

## License

This project is a foundational research system exploring structure emergence before language.

---

## Contact & Repository

- **Repository:** https://github.com/chavalasantosh/THRESHOLDONSET.git
- **Author:** ChavalaSantosh

---

## Acknowledgments

This system is built on the principle that **function stabilizes before knowledge appears**.

**The system proves:**
- Action can exist without knowledge
- Structure can emerge without language
- Identity can persist without names
- Relations can connect without interpretation
- Symbols can alias without meaning

**All of this happens before anyone says "this is X" or "this means Y".**

---

**For detailed information, see the documentation in `docs/` and phase-specific documentation in `src/phaseX/`.**
