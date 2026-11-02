# Embodied predictive processing in naturalistic multimodal sensing

Code snapshot for the manuscript revised on **29 October 2026**. This release combines the actual v6 main analysis with the later, separately trained personalization experiment. Their inputs, checkpoints, inference settings, and aggregation rules are distinct.

| Analysis | Current implementation | Evaluation sample | Seeds |
|---|---|---|---|
| Main report estimation | `main_pvrnn/epp_v6/`; original run `20261020T142629_112453Z` | 16 sessions / 11 participants; 11 Participant-LOO folds and 4 Date-LOO folds | 11, 23, 37, 51, 71 |
| Personalized A | `personalization/`; original run `formal_20261028_180424_097163` | 87 training sessions / 22 participants; 34 historical calibration sessions; 11 target sessions, 7 with reports; two independently initialized 40-minute simulations | 11, 23, 37 |

The 21 scientific implementation files checked against those two run manifests are unchanged. New code provides repository entry points and plotting/statistical organization. See `provenance/scientific_source_checks.json`.

## Start here

```bash
python reproduce.py verify
python -m pip install -r requirements.txt
```

The code archive includes source, scientific tests, configuration, aggregate reference statistics, and conceptual figure assets. The separate **reproduction companion** contains the actual aligned input tables, checkpoints, individual outputs, exact plotting tables, and manuscript snapshot. To run the commands below with the research data, merge the companion's contents into this repository root. Existing source files are not replaced.

```bash
# Recompute numerical results from saved outputs; no training or torch needed.
python reproduce.py statistics

# Rebuild current Figures 5–7 from saved outputs.
python reproduce.py figure-data
python reproduce.py figures

# Validate the formal model inputs; full dependencies required.
python reproduce.py check-inputs

# Refit the main five-seed LOO analysis, with the original full budget.
python reproduce.py train-main

# Check the personalization environment and input split.
python reproduce.py personalization-check

# Repeat inference using verified bundled models and calibrated A.
python reproduce.py personalization-all

# Explicitly retrain/recalibrate personalization before running all inference.
python reproduce.py personalization-retrain
```

For statistics alone, install `requirements-summaries.txt`. Training and full personalization inference can take hours. Saved-output recomputation is the shortest route to checking the manuscript numbers. Fresh results are written under `reproduced/` or a new `personalization/results/` directory; original runs remain available.

## Repository map

| Path | Role |
|---|---|
| `docs/CODE_LOGIC_zh.md` | Scientific logic, parameter roles, losses, split boundaries, aggregation |
| `docs/RUN_GUIDE_zh.md` | Execution order, commands, recovery, validation status |
| `docs/DATA_AND_FIGURES.md` | Required files and manuscript/figure mapping; missing original raw exports |
| `docs/API_INDEX.md` | Functions and classes indexed from the actual source |
| `main_pvrnn/` | Unchanged v6 implementation, preprocessing ancestry, configs, original tests |
| `personalization/` | Exact two40 scientific implementation, safe subprocess launcher, original tests |
| `analysis/` | Independent saved-output audits used for the latest manuscript |
| `figures/main/` | Figure 5–6 input preparation and plotting; obsolete v2 Figure 7 removed |
| `figures/common_environment/` | Current Figure 7 plotter, recovered from the 29 October style revision |
| `figures/assets/` | Conceptual vector assets for Figures 1, 2, and 4 |
| `reference_summaries/` | Aggregate research results for inspection without individual input data |
| `provenance/` | Actual run manifests, core source hashes, release scope and verification |

## Reproducibility boundaries

The companion supports refitting from aligned one-second data and from frozen minute tables. Original device exports, complete raw survey files, and the complete original dated dataset tree were not present in the retrieved source archives. Their processing logic is preserved, but full device-export-to-paper reproduction requires those originals.

Figures 1–4 are supplied as final vector assets (Figure 3 is in the companion). Exact original drawing scripts for Figures 1–3 were not recovered. The Figure 4 asset includes the final current D panel; older label-editing scripts are not advertised as rebuilding it. Figures 5–7 have plotting scripts and numeric inputs. Rendering/font differences can change file bytes; the frozen manuscript figures remain available for comparison.

The main run uses session-wise **seed medians** before pooled RMSE and clustered bootstrap. Personalization uses **seed-mean predictions** before errors. E+P physiological errors measure reconstruction using observed physiology; E-only errors compare generated physiology with withheld current physiology. Report readouts are supervised at session endpoints.

Personal calibration uses earlier same-person sessions. Other participants' training records can occur later than a target date; this is not a globally prospective calendar split. Personalized A is a model adaptation variable, not a validated stable trait.

## Historical code retained for source integrity

`main_pvrnn/epp_v6/individual.py`, `chain.py`, the rho grid in `config/epp_v6.json`, and several older analysis scripts remain because the original runner imports them and checks parent files. The current main-paper command runs **`--stage behavior --cohorts 11`**. The old rho/precision, recovery, MixedLM, historical room-mapping, and frozen-v3 branches do not produce the current paper's results. Do not run the original v6 `--stage all` as a substitute for `train-main`.

The earlier 102-session personalization v2, the standalone online-EP extension, and the 80-minute continuous scenario are excluded from the current workflow. Fully adaptive A is machine condition `local10`; the `zero` reference still performs local ER in eight coordinates and is distinct from No-ER.

## Software and attribution

Actual main training: Python 3.13.9, torch 2.12.0, numpy 2.3.5, pandas 2.3.3, scipy 1.16.3, scikit-learn 1.7.2, statsmodels 0.14.5, matplotlib 3.10.6 (original manifest). Personalization records Python 3.13.9, torch 2.12.0+cpu, numpy 2.3.5, pandas 2.3.3. Compatible dependency ranges are supplied, rather than an invented complete historical environment lock. Retraining on another platform does not guarantee identical numeric or checkpoint bytes.

No software license has been assigned in this snapshot. Repository hosting and data availability statements should use the authors' final decisions. No GitHub repository or external publication was created by this packaging step.
