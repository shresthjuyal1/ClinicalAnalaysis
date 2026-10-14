/*============================================================================
  Bird Keeping and Lung Cancer: Multiple Logistic Regression
  ----------------------------------------------------------------------------
  Question : After accounting for smoking, age, sex and socioeconomic status,
             is keeping pet birds associated with higher odds of lung cancer?
  Data     : 147 subjects (49 lung cancer cases, 98 controls)
  Software : SAS 9.4 (SAS OnDemand for Academics), PROC MEANS / FREQ /
             LOGISTIC / IML
  Outputs  : results/sas_output.pdf, results/sas_log.pdf
============================================================================*/

/* Point this at your local copy of the data file (see data/README.md). */
%let datafile = data/birdlung.data.txt;


/*----------------------------------------------------------------------------
  1. Load the data
     Coding (all binary variables are 0/1):
       Lung_Cancer          1 = case,   0 = control
       Sex                  1 = female, 0 = male
       Socioeconomic_Status 1 = high,   0 = low
       Birdkeeping          1 = yes,    0 = no
       Age                  years
       Years_smoked         years
       Cigarettes_per_day   average cigarettes per day
----------------------------------------------------------------------------*/
data birdlung;
    infile "&datafile";
    input Lung_Cancer Sex Socioeconomic_Status Birdkeeping
          Age Years_smoked Cigarettes_per_day;
run;


/*----------------------------------------------------------------------------
  2. Exploratory data analysis
----------------------------------------------------------------------------*/
title 'Descriptive statistics: continuous variables';
proc means data=birdlung n mean std min max;
    var Age Years_smoked Cigarettes_per_day;
run;

title 'Frequency tables: categorical variables';
proc freq data=birdlung;
    tables Lung_Cancer Sex Socioeconomic_Status Birdkeeping;
run;

title 'Distribution of cigarettes per day';
proc freq data=birdlung order=freq;
    tables Cigarettes_per_day / nocum nopercent;
run;


/*----------------------------------------------------------------------------
  3. Full multiple logistic regression model
     logit(P(cancer)) = b0 + b1*Sex + b2*SES + b3*Birdkeeping + b4*Age
                        + b5*Years_smoked + b6*Cigarettes_per_day
----------------------------------------------------------------------------*/
title 'Full model (includes Birdkeeping)';
proc logistic data=birdlung;
    model Lung_Cancer(event='1') = Sex Socioeconomic_Status Birdkeeping
                                   Age Years_smoked Cigarettes_per_day;
run;


/*----------------------------------------------------------------------------
  4. Interpreting a coefficient: odds ratio for high vs. low SES
     OR = exp(b2), 95% Wald CI = exp(b2 +/- 1.96 * SE(b2))
----------------------------------------------------------------------------*/
title 'Odds ratio and 95% CI: high vs. low socioeconomic status';
proc iml;
    b_ses  = 0.1054;
    se_ses = 0.4688;
    odds_ratio = exp(b_ses);
    lower      = exp(b_ses - 1.96*se_ses);
    upper      = exp(b_ses + 1.96*se_ses);
    print odds_ratio lower upper;   /* 1.111 (0.443, 2.785) */
quit;


/*----------------------------------------------------------------------------
  5. Predicted probabilities from the fitted model
     Profile: non-smoking woman, average age (56.97), low SES,
              with and without bird keeping.
     p = exp(eta) / (1 + exp(eta))
----------------------------------------------------------------------------*/
title 'Predicted probability of lung cancer: bird keeper vs. non-bird keeper';
proc iml;
    b0 = -1.9375;  b_sex  = 0.5613;  b_ses = 0.1054;  b_bird = 1.3626;
    b_age = -0.0398;  b_yrs = 0.0729;  b_cig = 0.0260;
    mean_age = 56.9659864;

    /* Sex=1 (female), SES=0 (low), Years_smoked=0, Cigarettes_per_day=0 */
    eta_bird    = b0 + b_sex + b_bird + b_age*mean_age;
    eta_no_bird = b0 + b_sex          + b_age*mean_age;

    p_bird    = exp(eta_bird)    / (1 + exp(eta_bird));     /* 0.0927 */
    p_no_bird = exp(eta_no_bird) / (1 + exp(eta_no_bird));  /* 0.0255 */
    print p_bird p_no_bird;
quit;


/*----------------------------------------------------------------------------
  6. Likelihood-ratio (drop-in-deviance) test for Birdkeeping
     H0: b_bird = 0, comparing nested models.
     G = (-2 log L reduced) - (-2 log L full) ~ chi-square(1)
----------------------------------------------------------------------------*/
title 'Reduced model (excludes Birdkeeping)';
proc logistic data=birdlung;
    model Lung_Cancer(event='1') = Sex Socioeconomic_Status
                                   Age Years_smoked Cigarettes_per_day;
run;

title 'Likelihood-ratio test: does Birdkeeping improve the model?';
proc iml;
    neg2logL_full    = 154.198;
    neg2logL_reduced = 165.868;
    G  = neg2logL_reduced - neg2logL_full;   /* 11.67 */
    df = 1;
    p_value = 1 - probchi(G, df);            /* 0.00064 */
    print G df p_value;
quit;

title;
