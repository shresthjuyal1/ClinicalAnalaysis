# Data

The data file is not committed to this repository. The analysis expects it at `data/birdlung.data.txt`.

## Source

Holst, Kromhout & Brand (1988), *British Medical Journal* 297:1319. The data are distributed as **Case Study 20.2 ("Bird Keeping and Lung Cancer")** in Ramsey & Schafer, *The Statistical Sleuth*. They are also available in R as `Sleuth3::case2002`.

## Format

Whitespace-delimited plain text, one subject per row, no header, 147 rows. Columns in order:

| # | Variable | Coding |
|---|---|---|
| 1 | `Lung_Cancer` | 1 = lung cancer case, 0 = control |
| 2 | `Sex` | 1 = female, 0 = male |
| 3 | `Socioeconomic_Status` | 1 = high, 0 = low |
| 4 | `Birdkeeping` | 1 = keeps birds, 0 = does not |
| 5 | `Age` | years |
| 6 | `Years_smoked` | years |
| 7 | `Cigarettes_per_day` | average cigarettes per day |

## Building the file from R

```r
library(Sleuth3)
d <- case2002
out <- data.frame(
  Lung_Cancer          = as.integer(d$LC == "LungCancer"),
  Sex                  = as.integer(d$FM == "Female"),
  Socioeconomic_Status = as.integer(d$SS == "High"),
  Birdkeeping          = as.integer(d$BK == "Bird"),
  Age                  = d$AG,
  Years_smoked         = d$YR,
  Cigarettes_per_day   = d$CD
)
write.table(out, "data/birdlung.data.txt", row.names = FALSE, col.names = FALSE)
```

To check the file, compare its frequencies with the tables in `results/sas_output.pdf`. There should be 49 cases, 36 females, 45 high-SES subjects and 67 bird keepers.
