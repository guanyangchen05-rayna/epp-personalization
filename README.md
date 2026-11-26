# Embodied predictive processing with multimodal sensing

Code for report estimation, personal calibration, common-environment simulation,
and the supplementary RQ1 ANOVA. This release updates the 29 October 2026 snapshot
with the four-phase simulation run on 25 November and the supplementary ANOVA.

| Analysis | Implementation | Data and aggregation |
| --- | --- | --- |
| Main model comparison | `main_pvrnn/epp_v6/` | 16 report-linked sessions, 11 participants; Participant-LOO and Date-LOO; five-seed median predictions before pooled RMSE |
| Personalization | `personalization/` | 87 training sessions; 34 earlier calibration sessions; 11 held-out sessions, seven with complete reports; three-seed mean outputs before scoring |
| RQ1 supplementary ANOVA | `supplementary/anova/` | Participant-LOO; participant-average MSE; GG correction followed by Holm correction across three outcomes |

## Execution

```bash
python -m pip install -r requirements.txt
python reproduce.py verify
python reproduce.py anova
```

The ANOVA input and checked results are included in the code archive. It runs
without model training or the reproduction companion. `requirements-summaries.txt`
contains the smaller dependency set for numerical summaries.

Aligned sensor inputs, checkpoints, fitted personal offsets, and individual model
outputs are in `EPP_reproduction_companion_20261126.zip`. Its contents use the same
relative paths as this code folder. After merging them into the repository root:

```bash
python reproduce.py statistics
python reproduce.py figure-data
python reproduce.py figures
python reproduce.py check-inputs
python reproduce.py personalization-check
python reproduce.py tests
```

`statistics` recomputes the main results, four-phase simulation contrasts,
held-out personalization metrics, offset comparisons, and ANOVA. `figures` renders
Figure 5 and the current common-environment Figure 6. The removed reconstruction
example remains accessible with `python figures/main/plot_main.py --figure legacy6`.

Model execution uses separate commands:

```bash
python reproduce.py train-main
python reproduce.py personalization-simulate
python reproduce.py personalization-all
python reproduce.py personalization-retrain
```

`personalization-simulate` repeats simulation using the saved networks and
calibrated offsets. `personalization-all` also evaluates held-out sessions.
`personalization-retrain` refits the shared networks and personal offsets before
inference. New outputs use separate run directories.

## Personalization protocol

Each participant's two slow posterior-mean offsets are calibrated from earlier
recordings under a frozen shared network. The other eight adaptive coordinates
are updated locally by ER. The zero reference fixes the two personal coordinates
at zero; fully adaptive A updates all ten coordinates locally.

The changing environment has four ten-sample phases: constant, linear rise,
linear fall, and one normalized sinusoidal cycle. Its independent stable control
remains constant for all 40 samples. The training-derived baseline and amplitudes
are unchanged: 20.7 °C / 923 ppm, with amplitudes of 0.30 °C / 71.5 ppm. The first
nonbaseline sample is minute 11. Response summaries use 11 <= minute < 40.

The recurrent dynamics, shared training, calibration, and local ER follow the
implemented two40 protocol. Only the simulation waveform and its associated
summary/plotting definitions change. The original held-out predictions remain
applicable because those sessions use their recorded environmental inputs.

## Repository structure

| Path | Contents |
| --- | --- |
| `main_pvrnn/` | Main PV-RNN/RNN models, preprocessing, configurations, and original tests |
| `personalization/` | Shared training, history-based calibration, sequential inference, and four-phase scenarios |
| `supplementary/anova/` | Standalone supplementary ANOVA with frozen inputs and reference results |
| `analysis/` | Saved-output summaries and validation |
| `figures/` | Plotting code and vector layout assets |
| `reference_summaries/` | Aggregate results |
| `docs/` | Methods, data paths, and execution details |
| `provenance/` | Source identities, release changes, and verification records |

The main model's ER uses the complete observed sequence. Personalization uses a
trailing window of at most ten retained minutes. E-only withholds physiological
targets; E+P uses them and measures physiological reconstruction. The report head
is supervised at session endpoints; simulated minute-level readouts have no
minute-level report ground truth.

ANOVA is exploratory and supplements the primary session-weighted RMSE analysis.
Participant aggregation does not fully model dependence from overlapping training
sets or shared classroom contexts. Original device exports are not included;
preprocessing from aligned inputs is supported by the companion. Conceptual
figure assets retained from the October snapshot are not a claim that the latest
manuscript's entire layout can be regenerated from Python.

The source data are In-Gauge and En-Gage, calendar-dated version 2:
<https://doi.org/10.25439/rmt.14578908.v2>. No new software or data license is
assigned by this release.
