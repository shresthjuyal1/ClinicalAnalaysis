# Detailed Analysis

All figures below come from [`results/sas_output.pdf`](../results/sas_output.pdf). The code is in [`sas/birdkeeping_lung_cancer.sas`](../sas/birdkeeping_lung_cancer.sas).

## 1. Exploratory data analysis

**Continuous variables (n = 147)**

| Variable | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| Age | 56.97 | 7.35 | 37 | 67 |
| Years smoked | 27.85 | 13.98 | 0 | 50 |
| Cigarettes per day | 15.75 | 9.70 | 0 | 45 |

**Binary variables**

| Variable | 0 | 1 |
|---|---:|---:|
| Lung cancer | 98 (66.7%) controls | 49 (33.3%) cases |
| Sex | 111 (75.5%) male | 36 (24.5%) female |
| Socioeconomic status | 102 (69.4%) low | 45 (30.6%) high |
| Bird keeping | 80 (54.4%) no | 67 (45.6%) yes |

Cigarettes per day clusters at round numbers: 20 (n = 38), 15 (27), 10 and 25 (15 each). This is typical of self-reported smoking. Only 17 subjects (11.6%) report zero cigarettes per day, so the sample is mostly smokers.

## 2. Full logistic regression model

The model estimates the log-odds of lung cancer from all six predictors. It converged (GCONV = 1E-8) and used all 147 observations.

**Overall significance:** the likelihood-ratio test of H₀: all β = 0 gives χ² = 32.94 on 6 df, p < .0001. Together, the predictors explain the outcome significantly better than an intercept-only model.

| Parameter | Estimate | SE | Wald χ² | p | Odds ratio | 95% CI |
|---|---:|---:|---:|---:|---:|---|
| Intercept | −1.9375 | 1.8042 | 1.15 | 0.283 | | |
| Sex (female) | 0.5613 | 0.5312 | 1.12 | 0.291 | 1.75 | 0.62 – 4.96 |
| SES (high) | 0.1054 | 0.4688 | 0.05 | 0.822 | 1.11 | 0.44 – 2.79 |
| **Bird keeping** | **1.3626** | 0.4113 | 10.98 | **0.0009** | **3.91** | **1.75 – 8.75** |
| Age | −0.0398 | 0.0355 | 1.26 | 0.263 | 0.96 | 0.90 – 1.03 |
| **Years smoked** | **0.0729** | 0.0265 | 7.57 | **0.0059** | **1.08** | **1.02 – 1.13** |
| Cigarettes per day | 0.0260 | 0.0255 | 1.04 | 0.308 | 1.03 | 0.98 – 1.08 |

### Interpreting the odds ratios

For a multiple logistic regression, when predictor *k* increases by *c* units and everything else stays the same, the odds of Y = 1 are multiplied by $e^{c\beta_k}$.

- **Bird keeping:** $e^{1.3626} = 3.91$. Holding the other variables constant, bird keepers have an estimated 3.9 times the odds of lung cancer of non-bird keepers. The whole confidence interval lies above 1.
- **Years smoked:** $e^{0.0729} = 1.076$ per year. Over a decade, $e^{10 \times 0.0729} = 2.07$, so the odds roughly double.
- **Socioeconomic status:** $e^{0.1054} = 1.11$, with 95% CI $e^{0.1054 \pm 1.96 \times 0.4688} = (0.44,\ 2.79)$. The interval spans 1 widely, so there is no evidence that SES is associated with lung cancer once the other variables are accounted for.

## 3. Predicted probabilities

The model's linear predictor η converts to a probability through the inverse logit, $p = e^{\eta} / (1 + e^{\eta})$.

**Profile:** a woman (Sex = 1) of average age (56.97), low SES, who has never smoked (Years smoked = Cigarettes per day = 0).

| | η | Predicted probability |
|---|---:|---:|
| Keeps birds | −1.9375 + 0.5613 + 1.3626 − 0.0398(56.97) = −2.281 | **0.093** |
| Does not keep birds | −1.9375 + 0.5613 − 0.0398(56.97) = −3.643 | **0.025** |

The ratio of the two probabilities is about 3.6. The ratio of their odds is exactly $e^{\beta_\text{bird}} = 3.91$, as the model implies.

> **Caveat:** in a case–control design the intercept depends on the chosen ratio of cases to controls. These probabilities are useful for comparing profiles, not as estimates of real-world risk.

## 4. Likelihood-ratio test for bird keeping

The Wald test above tests bird keeping on its own. A drop-in-deviance test compares two nested models directly:

- **Full model** (6 predictors): −2 log L = 154.198
- **Reduced model** (5 predictors, no bird keeping): −2 log L = 165.868

$$G = 165.868 - 154.198 = 11.67 \sim \chi^2_1, \qquad p = 0.00064$$

The test rejects H₀: β_bird = 0. Bird keeping explains variation in lung cancer status that smoking, age, sex and SES do not. Both tests (Wald p = 0.0009, LR p = 0.0006) agree.

Adding bird keeping also improves the model on other criteria:

| | Full | Reduced |
|---|---:|---:|
| AIC | 168.20 | 177.87 |
| c-statistic | 0.775 | 0.723 |
| Concordant pairs | 77.4% | 72.2% |

Coefficients in the reduced model move slightly. Years smoked changes from 0.0729 to 0.0796, and age from −0.0398 to −0.0580. However, the conclusion about smoking does not change, so bird keeping is not acting as a confounder for the smoking effect.

## 5. Study design and causal interpretation

- **Design:** this is an **observational** study, specifically a case–control study. Subjects were not assigned to keep birds; researchers recorded existing exposures among people with and without lung cancer.
- **"Risk factor" ≠ cause:** the analysis shows bird keeping is a statistically significant *risk factor*. That is, it is associated with higher odds of lung cancer after adjusting for the measured covariates. It does not establish that bird keeping *causes* lung cancer. Unmeasured confounders (for example, other household exposures) could explain part or all of the association.
- **What would strengthen the causal case:** replication in other populations, a dose–response relationship (for example, number of birds or years of exposure), and a plausible biological mechanism. One proposed mechanism is inhaling bird dander and dust.

## 6. Notes on this revision

While cleaning up the code for this repository, I corrected three small errors in the original work:

1. **SES confidence interval:** the original `PROC IML` step used the bird-keeping SE (0.4113) in place of the SES SE (0.4688) and had a sign error in the upper bound. This produced (0.50, 2.02). The corrected interval, (0.44, 2.79), matches SAS's own Wald limits.
2. **Likelihood-ratio statistic:** the original code computed G as full − reduced (−11.67). The correct order is reduced − full (+11.67). The p-value calculation already used the positive value, so the conclusion is unchanged.
3. **Typo in the write-up:** the bird-keeping p-value was written as 0.009; the SAS output shows 0.0009.

The original PDFs are kept unchanged in [`results/`](../results) and [`docs/original_writeup.pdf`](original_writeup.pdf).
