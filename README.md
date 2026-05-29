# MAES — Multidimensional Algorithmic Evolution System

**An open multi-agent ALife platform for studying emergent cognitive ecology, dimensional abduction, and communication layers.**

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-NumPy_only-green.svg)](requirements.txt)
[![Status](https://img.shields.io/badge/status-research-orange.svg)]()

---

## What MAES is

MAES is a **single-file Python simulator** (NumPy only, no PyTorch, no transformers) that studies how cognitive, linguistic, and communicative structures emerge in populations of multidimensional agents.

The system is built on a **hands-off methodology**: the experimenter sets initial conditions and observes; the simulator does not optimize for any goal. Agents have cognitive styles, beliefs, internal world-models, can plan paths (A*), debate ideas, form species, leave traces after death, and — in the v3.2 extension — communicate via a two-channel "singing tail" (discrete language + continuous music) and perform structural rituals.

---

## Phase 1 results (80 runs, 4 conditions × 20 seeds, 777 steps each)

The first complete empirical study, completed May 2026, demonstrates the central architectural claim of MAES: **dimensional abduction is a critical driver of system development.**

| Condition | dims | ai_peak | top_idea | species |
|---|---|---|---|---|
| v3.0_A (rich, no planner) | 13 | 32.15 | 1374.24 | 66.9 |
| v3.0_B_d5 (constrained) | 5 | 16.60 | 594.35 | 7.0 |
| v3.1_A (rich, with A*) | 13 | 31.00 | 1368.98 | 43.4 |
| v3.1_B_d5 (constrained, with A*) | 5 | 15.25 | 641.38 | 7.7 |

**Headline findings:**
- **Dimensional abduction (5D→13D) approximately doubles ai_peak and yields a ~9× increase in species diversity.**
- **A\* planning matters less than architecture:** planner adds <5% to ai_peak in either spatial regime.
- **Cognitive Style Ecology Hypothesis:** the equilibrium mixture of cognitive styles (skeptical, analytical, synthetic, intuitive, exploratory) is endogenously determined by space structure, not by initialization. Rich spaces concentrate on skeptical style (~85%); constrained spaces distribute more evenly.

See the [preprint](docs/MAES_preprint_EN_v1.0.pdf) for the full analysis.

---

## Key features

### Core simulator (`maes_v3_1.py`, ~3825 LOC)
- **Multidimensional space with dimensional abduction**: agents start in 5D and the space expands to 13D when collective torque signatures justify it. Directed expansion of the fitness landscape, not fixed dimensionality.
- **5 cognitive styles** (skeptical, analytical, synthetic, intuitive, exploratory) with empirically documented ecological niches.
- **Idea class**: evolving units of knowledge with lineage, age, mutation history, and PCA-hash fingerprints.
- **TorqueTrace**: each agent emits a compressed behavioral fingerprint that propagates as seed for cultural inheritance.
- **A\* planner** sitting on top of reactive physics.
- **Tombstone traces**: dead agents leave influence on living ones (cultural memory).
- **Catastrophes, collective synthesis, theory-of-mind, role physics, knowledge economy.**
- **Built-in ablation framework**.

### v3.2 overlays (under active development)
- **Singing Tail** (`maes_v3_2_singing_tail.py`, 1357 LOC): two-channel communication — discrete LanguageSignature + continuous MusicCarrier.
- **Ritual Cycle** (`maes_v3_2_ritual_cycle.py`, 1390 LOC): 5-phase ritual protocol with irreversible state-change operators.

### Mechanism registry
The full mechanism registry currently catalogues **135 mechanisms** across 14 thematic groups (54 implemented and validated, 43 documented concepts, the remainder under development). See [docs/MAES_Mechanisms_Consolidated.md](docs/MAES_Mechanisms_Consolidated.md).

---

## Quick start

```bash
git clone https://github.com/<MAES-Lab>/maes
cd maes
pip install -r requirements.txt

# Single seed, default config
python maes_v3_1.py --seed 1

# Full Phase 1 ablation (80 runs, ~12 hours on consumer hardware)
python scripts/run_all_777.py

# Analyze results
python scripts/analyze_all.py
```

---

## Reproducibility

Phase 1 results are reproducible end-to-end on a single consumer machine in approximately 12 hours of CPU time. Hardware used:
- Desktop: Intel i9, 32 GB RAM, RTX 4060 Ti 16 GB (GPU unused; NumPy only)
- All 80 main runs + 15 self-development runs complete within budget

Seed-deterministic: re-running with the same seed reproduces final `ai_peak` to floating-point tolerance.

---

## Repository structure

```
maes/
├── maes_v3_1.py              # Core simulator (3825 LOC)
├── maes_v3_2_singing_tail.py # Singing Tail overlay
├── maes_v3_2_ritual_cycle.py # Ritual Cycle overlay
├── scripts/
│   ├── run_all_777.py        # Run full Phase 1 ablation
│   ├── analyze_all.py        # Analyze all JSON outputs
│   └── run_selfdev.py        # Run self-development tests
├── data_777/                 # Phase 1 results (JSON, 95 files)
├── docs/
│   ├── MAES_preprint_EN_v1.0.pdf
│   ├── MAES_preprint_RU_v1.0.pdf
│   └── MAES_Mechanisms_Consolidated.md
├── requirements.txt
├── LICENSE
├── CITATION.cff
└── README.md
```

---

## Citation

If you use MAES in your research, please cite:

```bibtex
@misc{shapoval2026maes,
  author       = {Shapoval, Ilarion I.},
  title        = {{MAES}: Multidimensional Algorithmic Evolution System --- Phase 1 Empirical Study},
  year         = {2026},
  howpublished = {\url{https://github.com/<your-username>/maes}},
  note         = {Preprint available}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

---

## Author and methodology

MAES is developed by **Ilarion I. Shapoval** as an independent research project. The architectural design, mechanism registry, and methodological commitments belong to the author. Software implementation was carried out in iterative collaboration with several large language models of the Anthropic Claude family, with additional assistance from Google Gemini and OpenAI ChatGPT. Empirical analyses are the author's.

---

## License

AGPL-3.0 — see [LICENSE](LICENSE). Free for academic and non-commercial use; derivative works must remain open under the same license.

---

## Contact

For research collaboration inquiries, see contact information in [CITATION.cff](CITATION.cff).
