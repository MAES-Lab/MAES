# Contributing to MAES

Thank you for your interest in MAES. This document describes how to engage
with the project — questions, bug reports, ideas, code contributions.

## Status of the project

MAES is **research software** developed by a single independent researcher.
It is not (yet) a community-maintained project. This affects how
contributions are reviewed and merged:

- Substantial architectural changes need discussion before implementation
- Bug fixes are welcome via pull request
- Documentation improvements are highly welcome
- New mechanism implementations from the registry (see
  `docs/MAES_Mechanisms_Master_Inventory.md`) are welcome but should be
  discussed first to ensure consistency

## How to contribute

### 1. Reporting bugs

Open a GitHub issue with the `bug` label. Include:
- Python version (`python --version`)
- NumPy version (`pip show numpy`)
- OS (Windows version, macOS, Linux distro)
- Steps to reproduce
- Expected vs actual behavior
- Full error traceback if any

### 2. Asking questions

Open a GitHub issue with the `question` label. Please first check existing
issues — many architectural questions are already answered there.

### 3. Suggesting ideas

Open a GitHub issue with the `idea` label. The mechanism registry includes
30+ concepts ready for implementation; if you want to implement one, please
say so in the issue before starting work.

### 4. Submitting code

Pull requests are welcome. Please:

- One concern per PR (don't mix bug fix with new feature)
- Match the existing code style (4-space indent, slot-based classes where
  appropriate, NumPy-only)
- Include a self-test for new mechanisms (look at `_self_test()` functions
  in existing modules for examples)
- Update relevant documentation
- Verify your change does not break the existing self-tests:
  ```bash
  python maes_v3_2_singing_tail.py     # should print SELF-TEST PASSED
  python maes_v3_2_ritual_cycle.py     # should print SELF-TEST PASSED
  ```

### 5. Methodological commitments

MAES has architectural principles that constrain what kinds of changes are
acceptable. Contributions that violate these principles will not be merged
regardless of code quality:

- **Endogenous Mechanisms**: no external ML primitives (no PyTorch,
  TensorFlow, transformers, sklearn) in the simulator core. NumPy only.
  (External libraries are fine for analysis scripts, not for the simulator
  itself.)
- **Hands-off methodology**: do not introduce optimization objectives.
  No reward signals, no fitness functions. MAES does not optimize; it
  observes.
- **Principle of continuity**: do not rewrite existing modules. New
  features go as overlays attached non-invasively via `attach_*` functions.

## Collaboration inquiries

For research collaboration (joint papers, conference workshops, visiting
researcher arrangements), open an issue with the `collaboration` label or
contact the author directly through GitHub.

## Code of conduct

Be kind. Be precise. Be honest about what you don't know. That is enough.
