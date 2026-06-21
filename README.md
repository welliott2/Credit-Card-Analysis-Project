# Credit Card Default: Does Demographic Data Add Predictive Signal?

## Background

At my current job, I am in charge of a credit card analytics project (but without any demographic
context attached to it). This made me curious about a question I couldn't easily test
at work: **once you already know how someone has been paying their bills, does knowing
who they are (age, education, marital status, sex) tell you anything more about
whether they'll default?**

This project uses the [UCI Default of Credit Card Clients dataset](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
(30,000 Taiwanese credit card accounts from 2005) to test that question directly,
since it includes both transactional/behavioral data (payment history, bill amounts)
and demographic data (age, education, marital status, sex) for the same accounts.

## The Question

Is payment behavior alone enough to explain default risk, or does demographic data
add meaningful signal on top of it?

## Data Cleaning Notes

The dataset's documentation doesn't fully match the data itself. Rather than silently
dropping or guessing at these values, I made the following explicit, disclosed
decisions:

- **EDUCATION**: documented as 1-4 (graduate school, university, high school, other),
  but the data also contains codes 0, 5, and 6. I recoded all of these into a single
  explicit "Unknown" category (345 records) rather than merging them into an existing
  label or dropping them.
- **MARRIAGE**: documented as 1-3 (married, single, other), but the data also contains
  code 0. I recoded this into an explicit "Unknown" category (54 records).
- **PAY_0 (and related PAY_2-PAY_6 columns)**: documented scale starts at -1 ("pay
  duly"), but the data contains a -2 value (2,759 records in PAY_0 alone) with no
  official definition. Rather than merge -2 into -1 (which would assume it means the
  same thing as "paid on time"), I kept it as its own category, since it's plausibly
  a different status entirely (no balance that month) and conflating the two
  could obscure a real difference in behavior.

## Findings

**Payment behavior is the dominant predictor.** Default rate by most recent payment
status (PAY_0) ranges from **12.8%** (paid on time) up to **77.8%** (3+ months
delinquent), with a clean, orderly gradient in between. This is by far the strongest
single signal in the dataset.

**Demographics alone show a real, smaller effect.** Default rate varies:
- By education: 19.2% (graduate school) to 25.2% (high school)
- By marital status: 20.9% (single) to 26.0% (other)
- By sex: 20.8% (female) to 24.2% (male)

These spreads are real, but an order of magnitude smaller than the behavioral effect.

**Demographics still matter *within* a given behavior group.** Looking only at
accounts that paid on time last month (PAY_0 = 0, the largest single group at 14,737
accounts), default rate still ranges from **3.6%** to **14.2%** depending on
education level. In other words, even after controlling for recent payment behavior,
demographic differences persist.

**A caution on the combined breakdown**: once you slice by payment status *and*
education simultaneously, several resulting groups are very small (some with only
1-3 accounts). Those cells produce extreme-looking rates (100% default on a
single account) that aren't reliable patterns, just small-sample noise. Worth
keeping in mind when reading the detailed table in the analysis output.

## Conclusion

Demographic data is not the primary driver of credit default risk (payment behavior
dominates by a wide margin). But demographic data isn't noise either: it adds a real,
measurable secondary signal that persists even after accounting for recent payment
behavior. For an analysis that only has access to transactional data (as I do in my
current role), this suggests behavioral signal alone will capture most, but not all,
of the picture.

## Project Structure

credit-risk-demographics/

├── data/

├── src/

│   ├── load_cc_data.py           # Pulls the dataset from the UCI repository

│   ├── explore_taiwan_cc_data.py # Initial inspection of raw category values

│   ├── clean_taiwan_cc_data.py   # Cleaning/recoding, documented above

│   └── analyze_taiwan_cc_data.py # Default rate comparisons (behavioral vs. demographic)

├── README.md

└── requirements.txt

## Tools

Python, pandas. (Tableau Public dashboard: link to be added.)

## Data Source

Yeh, I-Cheng. (2016). Default of Credit Card Clients [Dataset]. UCI Machine Learning
Repository. https://doi.org/10.24432/C55S3H
