Target (Observed) Data
================

## Definitions

_**Target data**_ are the _observed data being modeled_ as the prediction target
in a collaborative modeling exercise.
These data come in two forms:

1. **time series** data[^truth], which are the _observed_ counts or rates partitioned
   for each unique combination of [task id values](#task-id-vars).
2. **oracle output** data are _derived from the time series data_ and represent 
   model output that would have been generated if the target data values had 
   been known ahead of time.

Hubverse tools like [hubVis](https://hubverse-org.github.io/hubVis) make use of
the time series data for visualizations while other hubverse tools like
[hubEvals](https://hubverse-org.github.io/hubEvals) and
[hubEnsembles](https://hubverse-org.github.io/hubEnsembles) make use of the
oracle output data for model evaluations. We describe these formats briefly
here, and give more detail about the oracle outputs in the remainder of this
document.

[^truth]: Time series data is sometimes referred to as "ground truth" data, but
    we no longer use this term in the hubverse.

## Uses of target time series data and oracle output

Each data format is useful for different purposes (see table below).
Modelers will most often estimate model parameters by fitting to the raw
data in time series format. Both data formats may be useful for
different kinds of data visualizations; for example, a plot of time
series predictions in quantile format may use the raw time series data,
while a plot of pmf predictions for a categorical target may use the
oracle output. The primary use case of oracle output is for evaluation.

| Data Format   | Model Estimation | Plotting | Evaluation |
|:--------------|:-----------------|:---------|:-----------|
| Time series   | ✅               | ✅       |            |
| Oracle output |                  | ✅       | ✅         |

Common uses for target time series and oracle output data. A ✅
indicates which data formats are most commonly used for each purpose.


## Time series

The first format is *time series* data. This is often the native or
“raw” format for data. Each row of the data set contains one observed
value of the time series, contained in a column named `observation`.
Here is an example of this form of data, showing selected dates for
Massachusetts (FIPS code 25), drawn from the forecasting example in
`hubExamples`:

| date       | location | observation |
|:-----------|:---------|------------:|
| 2022-11-19 | 25       |          79 |
| 2022-11-26 | 25       |         221 |
| 2022-12-03 | 25       |         446 |
| 2022-12-10 | 25       |         578 |

In settings where a hub is working with multiple observed signals at
each time point (e.g., cases, hospitalizations, and deaths), the values
of those signals will be given in different rows, with a column such as
`signal` indicating what quantity is reported in each row. The only
restrictions that hubverse tools impose on data in this format is that
it should have a column named `observation` and a column with a time
index, such as `date` or `time`.

## Oracle output

Oracle output follows a format that is similar to a [hubverse model
output
file](https://hubverse.io/en/latest/user-guide/model-output.html#example-model-submission-file),
with three main differences:

- Predictions correspond to a distribution that places probability 1 on
  the observed target outcome (see figure below).
- Predictions (e.g., means, quantile values, or pmf category
  probabilities, etc.) are stored in a column named `oracle_value`
  rather than `value`.
- Generally, the columns of the oracle output will
  be a subset of the columns of valid model output for the hub, with
  just those columns that are needed to correctly align `oracle_value`s
  with the corresponding predicted `value`s produced by modelers. 
  We introduce some conventions to avoid duplication of data, described
  in more detail below. 

<!--
library("ggplot2")
withr::with_seed(5, {
  ggplot(data.frame(value = rnorm(1e3, 1), output = "model"), aes(x = value)) +
    geom_density(aes(fill = output)) +
    geom_segment(aes(y = 0, yend = 1, color = output), data = data.frame(value = 2, output = "or
  acle"), size = 2) +
    scale_color_manual(values = 'blue') +
    guides(fill = guide_legend(theme = theme(legend.title = element_blank()))) +
    theme_classic(base_size = 16) +
    labs(y = "probability", x = "model value / oracle value") +
    theme(legend.position = "inside", legend.position.inside = c(0.2, 0.8), legend.spacing = uni
  t(0, "npc"))
    ggsave(here::here("docs/source/images/oracle-model-output.png"), width = 7, height = 4, dpi = 150)
})
--->

```{figure} ../images/oracle-model-output.png
:figclass: margin-caption
:alt: Simplified graph showing two distrbutions called "oracle" and "model". The model distribution spans from below -2 to above 4 with a mean of 1, with probabilities below 0.5. The oracle distribution appears as a single line at 2 that has a probability of 1.

Model and Oracle distributions

Just like model outputs are derived from a model distribtuion, oracle output
values are derived from distributions with a probability of 1 on the observed
target.
```

The oracle output is designed to align with [model
output](#formats-of-model-output) task ID and model output representation
columns. This allows the two to be merged so that `value` can be compared
and evaluated against the corresponding `oracle_value`. The important
difference between the outputs is that the oracle output is necessarily going
to have a subset of the task ID columns as the model output data and, depending
on the hub, may not have either of the model output representation columns.

### Example

Here is an example of this form of data, based on the forecasting
example in `hubExamples`:

| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk inc flu hosp | quantile | `<NA>` | 79 |
| 25 | 2022-11-26 | wk inc flu hosp | quantile | `<NA>` | 221 |
| 25 | 2022-12-03 | wk inc flu hosp | quantile | `<NA>` | 446 |
| 25 | 2022-12-10 | wk inc flu hosp | quantile | `<NA>` | 578 |

In this example, the observed weekly influenza hospitalization count in
MA on the week ending 2022-11-19 was 79. A probability distribution that
places probability 1 on that outcome will have all quantiles equal to
that observed value, so 79 appears as the `oracle_value` for quantile
outputs for that `location` and `target_end_date`. The use of `<NA>` for
the `output_type_id` represents the fact that this `oracle_value` is
relevant for all quantile levels; this convention will be described in
more detail below.

For comparison, here is the corresponding **model output** showing two
horizons from the `Flusight-baseline` model for the `2022-11-19`
reference date (the columns `model_id` and `reference_date` are omitted
for compactness):

| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.05 | 22 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.1 | 31 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.25 | 45 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.5 | 51 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.75 | 57 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.9 | 71 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.95 | 80 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.05 | 5 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.1 | 21 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.25 | 38 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.5 | 51 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.75 | 64 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.9 | 81 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.95 | 97 |

### Task ID columns

The model output can contain any number of task ID columns that are used to
provide details about what is being predicted based on

 - independent task ID variables (e.g. `location`, `target_date`, and
   `age_group`),
 - derived (dependent on other variables) task ID variables (e.g. `horizon`,
   `reference_date`, `origin_date`), and
 - scenario-specific task ID variables (e.g. `scenario_id`).

### Model output representation columns

**The `output_type` and `output_type_id` columns only need to be included if
the hub collects `pmf` or `cdf` outputs.** As was described above, for those
two output types the `oracle_value` depends on the `output_type_id`. On the
other hand, the `oracle_value` is not specific to the quantile level for
quantile forecasts or the sample index for sample forecasts, and so for these
output types (as well as mean and median), the `output_type_id` is not needed
to align observations with predictions.


**The oracle output will contain the independent task ID variables** that are
necessary to match the `oracle_value` column with `value` column of the model
output.

### The `oracle_value` column

Oracle output follows a similar format as model outputs, but the `value`
column is named `oracle_value`, and it contains the value of the
prediction that would be reported if the observed value of the target
was known with certainty. The implications of this vary depending on the
`output_type`:

- **For the `mean`, `median`, `quantile`, and `sample` output types, the
  `oracle_value` is the observed value of the prediction target.** This
  `oracle_value` is the same for all quantile levels and all sample
  indices, since a predictive distribution that places all of its
  probability on the observed outcome will have all quantiles equal to
  that value and all samples from that distribution will be equal to the
  observed value.
- **For `pmf` and `cdf` output types, the `oracle_value` is either `1` or `0`**
    - For the `pmf` output type, the `oracle_value` is `1` when the
      `output_type_id` corresponds to the observed category (indicating a
      probability of 1 for that category) and `0` for other categories.
    - For the `cdf` output type, the `oracle_value` is `0` for any
      `output_type_id` levels that are less than the observed value, and `1`
      for any `output_type_id` levels that are greater than or equal to the
      observed value, corresponding to the step function cdf of a
      probability distribution that places all of its probability at the
      observed value.

### Generating oracle output data

A hub will typically have access to data in time series format, and will
need to convert it to the **oracle output** format for use with any tools
that require it in that format (see the next section). In hubs that
collect mean, median, quantile, or sample predictions for the reported
signal values in the raw time series data, the two formats may be
essentially the same, perhaps with some renaming of columns. However, in
hubs that form predictions for quantities that are derived from the the
raw time series data, such as the peak time or peak incidence, and in
hubs that collect pmf or cdf predictions, the formats will differ more
substantively.


## Examples of the oracle output format

We will illustrate the above concepts using the example forecast data
from `hubExamples` that was discussed briefly in the overview section;
please see the [forecast_data
vignette](https://hubverse-org.github.io/hubExamples/articles/forecast_data.html)
in hubExamples for more detail about these data.

Briefly, this example is for a hub with five task id variables:

- The `location` column contains a FIPS code identifying the location
  being predicted.
- The `reference_date` is a date in ISO format that gives the Saturday
  ending the week the predictions were generated.
- The `horizon` gives the difference between the `reference_date` and
  the target date of the forecasts (`target_end_date`, see next item) in
  units of weeks. Informally, this describes “how far ahead” the
  predictions are targeting.
- The `target_end_date` is a date in ISO format that gives the Saturday
  ending the week being predicted. For example, if the `target_end_date`
  is `"2022-12-17"`, predictions are for a quantity relating to
  influenza activity in the week from Sunday, December 11, 2022 through
  Saturday, December 17, 2022.
- The `target` describes the target quantity for the prediction.

There are three `targets`, all based on measures of weekly influenza
hospitalizations, with forecasts collected in different `output_type`s
for each target, as is summarized in the following table:

| target | output_type | description |
|:---|:---|:---|
| wk inc flu hosp | quantile, median, mean, sample | weekly count of hospital admissions with flu |
| wk flu hosp rate | cdf | week rate of hospital admissions with flu per 100,000 population |
| wk flu hosp rate category | pmf | categorical severity level of the hospital admissions rate, with levels ‘low’, ‘moderate’, ‘high’, and ‘very high’ |

Below, we show snippets of the contents of a `model_out_tbl` with
example forecast submissions and the corresponding **oracle output** for
each `output_type`. We highlight two points about these objects:

- The `reference_date` and `horizon` columns are included in the model
  outputs, but they are not included in the oracle output.
- In this example, the **oracle output** for the `mean`, `median`,
  `quantile`, and `sample` output types are all the same, and they
  contain `<NA>` values for the `output_type_id`. In a hub without `pmf`
  or `cdf` output types, the `output_type` and `output_type_id` columns
  could be omitted and this duplication could be eliminated.

:::{note}

These examples are all collected and filtered from [the `hubExamples` package](https://hubverse.github.io/hubExamples). The model output data set contains over
10,000 rows and the oracle output data has over 200,000 rows.

To make comparisons easier, we have subset the data to Massachusettes (FIPS code
25) with four target end dates between 2022-11-19 and 2022-12-10.

In addition, for the model output data, we are only showing the
`Flusight-baseline` model for the 2022-11-19 reference date and removing the
`model_id` and `reference_date` columns.

:::

### Output type `mean`

:::{table} A subset of **model output** showing `mean` predictions across four horizons
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk inc flu hosp | mean | `<NA>` | 51.18476 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | mean | `<NA>` | 51.39129 |
| 2 | 25 | 2022-12-03 | wk inc flu hosp | mean | `<NA>` | 51.89889 |
| 3 | 25 | 2022-12-10 | wk inc flu hosp | mean | `<NA>` | 52.54409 |
:::

:::{table} The `mean` **oracle output** from 19 November to 10 December 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk inc flu hosp | mean | `<NA>` | 79 |
| 25 | 2022-11-26 | wk inc flu hosp | mean | `<NA>` | 221 |
| 25 | 2022-12-03 | wk inc flu hosp | mean | `<NA>` | 446 |
| 25 | 2022-12-10 | wk inc flu hosp | mean | `<NA>` | 578 |
:::

For the `mean` output type, the `oracle_value` is the numeric value of
the prediction target. Here, the first row of the oracle output
indicates that 79 flu hospitalizations were reported in Massachusettes for the
week ending on 2022-11-19. This can be viewed as the mean of a
“predictive distribution” that is entirely concentrated on that observed
value. The use of `<NA>` for the `output_type_id` matches the convention
for model output with the mean output type.

### Output type `median`

:::{table} A subset of **model output** showing `median` predictions across four horizons
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk inc flu hosp | median | `<NA>` | 51 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | median | `<NA>` | 51 |
| 2 | 25 | 2022-12-03 | wk inc flu hosp | median | `<NA>` | 51 |
| 3 | 25 | 2022-12-10 | wk inc flu hosp | median | `<NA>` | 51 |
:::

:::{table} The `median` **oracle output** from 19 November to 10 December 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk inc flu hosp | median | `<NA>` | 79 |
| 25 | 2022-11-26 | wk inc flu hosp | median | `<NA>` | 221 |
| 25 | 2022-12-03 | wk inc flu hosp | median | `<NA>` | 446 |
| 25 | 2022-12-10 | wk inc flu hosp | median | `<NA>` | 578 |
:::

The `oracle_value` for the `median` output type is the same as for the
`mean` output type: the numeric value of the prediction target. This is
the median of a distribution that is entirely concentrated on that
observed value. Again, the use of `<NA>` for the `output_type_id`
matches the convention for model output with the median output type.

### Output type `quantile`

:::{table} A subset of **model output** showing `quantile` predictions across two horizons
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.05 | 22 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.1 | 31 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.25 | 45 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.5 | 51 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.75 | 57 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.9 | 71 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | quantile | 0.95 | 80 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.05 | 5 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.1 | 21 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.25 | 38 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.5 | 51 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.75 | 64 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.9 | 81 |
| 1 | 25 | 2022-11-26 | wk inc flu hosp | quantile | 0.95 | 97 |
:::

:::{table} The `quantile` **oracle output** from 19 November to 10 December 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk inc flu hosp | quantile | `<NA>` | 79 |
| 25 | 2022-11-26 | wk inc flu hosp | quantile | `<NA>` | 221 |
| 25 | 2022-12-03 | wk inc flu hosp | quantile | `<NA>` | 446 |
| 25 | 2022-12-10 | wk inc flu hosp | quantile | `<NA>` | 578 |
:::

As with the `mean` and `median` output types, the `oracle_value` for a
quantile type is the observed numeric value of the prediction target,
which is the quantile of a predictive distribution that assigns
probablity 1 to that observed value at any quantile probability level. A
model output file would need to have a separate row for each quantile
level reported in the `output_type_id` column. As a space-saving
convention, we use `output_type_id = <NA>` to indicate that this
`oracle_value` applies to all quantile levels.

### Output type `sample`

:::{table} A subset of **model output** showing 6 `sample` predictions across one horizon
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2101 | -2 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2102 | 2 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2103 | 52 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2104 | 47 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2105 | 56 |
| 0 | 25 | 2022-11-19 | wk inc flu hosp | sample | 2106 | 46 |
:::

:::{table} The `sample` **oracle output** from 19 November to 10 December 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk inc flu hosp | sample | `<NA>` | 79 |
| 25 | 2022-11-26 | wk inc flu hosp | sample | `<NA>` | 221 |
| 25 | 2022-12-03 | wk inc flu hosp | sample | `<NA>` | 446 |
| 25 | 2022-12-10 | wk inc flu hosp | sample | `<NA>` | 578 |
:::

As with the above output types, the `oracle_value` for a sample type is
the observed numeric value of the prediction target since all samples
from a predictive distribution that assigns probablity 1 to the observed
value will be equal to that value. A model output file would need to
have a separate row for each sample, with the sample index recorded in
the `output_type_id` column. We use `output_type_id = <NA>` to indicate
that this `oracle_value` applies to all predictive samples.

### Output type `pmf`

:::{table} A subset of **model output** showing `pmf` predictions across three horizons
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk flu hosp rate category | pmf | low | 0.9999997 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate category | pmf | moderate | 0.0000003 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate category | pmf | high | 0.0000000 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate category | pmf | very high | 0.0000000 |
| 1 | 25 | 2022-11-26 | wk flu hosp rate category | pmf | low | 0.9999983 |
| 1 | 25 | 2022-11-26 | wk flu hosp rate category | pmf | moderate | 0.0000017 |
| 1 | 25 | 2022-11-26 | wk flu hosp rate category | pmf | high | 0.0000000 |
| 1 | 25 | 2022-11-26 | wk flu hosp rate category | pmf | very high | 0.0000000 |
| 2 | 25 | 2022-12-03 | wk flu hosp rate category | pmf | low | 0.9997501 |
| 2 | 25 | 2022-12-03 | wk flu hosp rate category | pmf | moderate | 0.0002499 |
| 2 | 25 | 2022-12-03 | wk flu hosp rate category | pmf | high | 0.0000000 |
| 2 | 25 | 2022-12-03 | wk flu hosp rate category | pmf | very high | 0.0000000 |
:::

:::{table} The `pmf` **oracle output** from 19 November to 03 December 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk flu hosp rate category | pmf | low | 1 |
| 25 | 2022-11-19 | wk flu hosp rate category | pmf | moderate | 0 |
| 25 | 2022-11-19 | wk flu hosp rate category | pmf | high | 0 |
| 25 | 2022-11-19 | wk flu hosp rate category | pmf | very high | 0 |
| 25 | 2022-11-26 | wk flu hosp rate category | pmf | low | 0 |
| 25 | 2022-11-26 | wk flu hosp rate category | pmf | moderate | 1 |
| 25 | 2022-11-26 | wk flu hosp rate category | pmf | high | 0 |
| 25 | 2022-11-26 | wk flu hosp rate category | pmf | very high | 0 |
| 25 | 2022-12-03 | wk flu hosp rate category | pmf | low | 0 |
| 25 | 2022-12-03 | wk flu hosp rate category | pmf | moderate | 0 |
| 25 | 2022-12-03 | wk flu hosp rate category | pmf | high | 1 |
| 25 | 2022-12-03 | wk flu hosp rate category | pmf | very high | 0 |
:::

The presence of a `1` for the `oracle_value` in the first row and `0` in the
subsequent three rows indicates that the observed rate category in
Massachusettes on the week of 2022-11-19 was `"low"` while the week of
2022-11-26 was `"moderate"`.

### Output type `cdf`

:::{table} A subset of **model output** showing `cdf` predictions in a single horizon
| horizon | location | target_end_date | target | output_type | output_type_id | value |
|---:|:---|:---|:---|:---|:---|---:|
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.25 | 0.0409498 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.5 | 0.1310412 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.75 | 0.5679516 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 1 | 0.8911202 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 1.25 | 0.9650988 |
| 0 | 25 | 2022-11-19 | wk flu hosp rate | cdf | 1.5 | 0.9850981 |
:::

:::{table} A subset of the `cdf` **oracle output** for 19 November 2022
| location | target_end_date | target | output_type | output_type_id | oracle_value |
|:---|:---|:---|:---|:---|---:|
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.25 | 0 |
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.5 | 0 |
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 0.75 | 0 |
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 1 | 0 |
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 1.25 | 1 |
| 25 | 2022-11-19 | wk flu hosp rate | cdf | 1.5 | 1 |
:::

The presence of a `0` for the `oracle_value` in the first four rows and a
`1` for the `oracle_value` in subsequent rows indicates that the
observed hospitalization rate in the US in the week of 2022-11-19 was
greater than 1 but less than or equal to 1.25. These `oracle_value`s
encode a step function CDF that is equal to 0 when the `output_type_id`
is less than the observed rate and jumps to 1 at the observed rate.

## How hubs should provide access to target time series data and oracle output

Hubs should ensure that standardized procedures for accessing target
data are available. The data formats that a hub provides may depend on
the needs of the specific hub, and which hubverse tools the hub wants to
use. For example, a hub that will not be conducting evaluations by
comparing predictions to observed target values may not need to provide
data in the oracle output format.

Access to target time series data and oracle output can be provided in
either of two ways:

1.  by providing example code for accessing target time series data
    and/or oracle output programmatically
2.  by storing snapshots of the target time series data and/or oracle
    output in the hub repository in the `target-data` folder.

Following general conventions for storage of code related to modeling
hubs, we recommend that any code for data access be provided in a
separate repository following standard language-specific packaging
guidelines, or if the code is small in scope it can be placed within the
`src` folder of the hub’s repository.

