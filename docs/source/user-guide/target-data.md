Target (Observed) Data
================

## Definitions

_**Target data**_ are the _observed data being modeled_ as the prediction target
in a collaborative modeling exercise.
These data come in two forms:

1. **time series** data[^truth], which are the _observed_ counts or rates
   partitioned for each unique combination of [task id values](#task-id-vars).
2. **oracle output** data are _derived from the time series data_ and represent
   model output that would have been generated if the target data values had
   been known ahead of time.

Hubverse tools like [hubVis](https://hubverse-org.github.io/hubVis) make use of
the time series data for visualizations, while other hubverse tools like
[hubEvals](https://hubverse-org.github.io/hubEvals) and
[hubEnsembles](https://hubverse-org.github.io/hubEnsembles) make use of the
oracle output data for model evaluations. We describe these formats briefly
here and give more details about the oracle outputs in the remainder of this
document.

[^truth]: Time series data is sometimes referred to as "ground truth" data, but
    we no longer use this term in the hubverse.

## Uses of target time series data and oracle output

Each data format is useful for different purposes (see table below).
Modelers will most often estimate model parameters by fitting to the raw
data in time series format. Both data formats may be helpful for
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

**Hub administrators:** see [File Formats and Naming](#file-formats-and-naming) and [Target Data Hub Configuration](#target-data-hub-configuration) for setup and performance guidance.

(target-time-series)=
## Time series

The first format is *time series* data. This is often the native or
"raw" format for data. Each row of the data set is a **unit of observation**, and the columns consist of:

1. task ID variables that uniquely define the unit of observation. This must include at least one column representing the date of observation. The column should share the same name across target data and model outputs.
2. an `observation` column that records the observed value

Here is an example of this form of data, showing selected dates for
Massachusetts (FIPS code 25), drawn from the forecasting example in
`hubExamples`:

| target_end_date       | location | observation |
|:-----------|:---------|------------:|
| 2022-11-19 | 25       |          79 |
| 2022-11-26 | 25       |         221 |
| 2022-12-03 | 25       |         446 |
| 2022-12-10 | 25       |         578 |

Here, the unit of observation is a target_end_date and location pair. That is, for each target_end_date and location, there is a single observed value.
In settings where a hub is working with multiple observed targets at
each time point (e.g., cases, hospitalizations, and deaths), the values
of those targets will be part of the unit of observation, with a column such as
`target`, indicating what quantity is reported in each row.


```{table} Time series data with target data included in the unit of observation

| target_end_date       | target | location | observation |
|:-----------|:-------|:---------|------------:|
| 2022-11-19 | cases  | 25       |          79 |
| 2022-11-26 | cases  | 25       |         221 |
| 2022-12-03 | cases  | 25       |         446 |
| 2022-12-10 | cases  | 25       |         578 |
| 2022-11-19 | deaths | 25       |           9 |
| 2022-11-26 | deaths | 25       |          21 |
| 2022-12-03 | deaths | 25       |          46 |
| 2022-12-10 | deaths | 25       |          78 |

```

### Optional `as_of` column to record data versions

Time series data are expected to be compiled from an authoritative upstream
data source after each target date.
Because of reporting delays, the data may initially be represented by one value that could be updated in one or more subsequent versions of the data.

```{table} Data recorded on December 3 for December 3 shows an observation of 420
| *as\_of*     | target_end_date       | location | observation |
|:-------------|:-----------|:---------|------------:|
| *2022-12-03* | 2022-11-19 | 25       |          79 |
| *2022-12-03* | 2022-11-26 | 25       |         221 |
| *2022-12-03* | 2022-12-03 | 25       |         [420]{.bordered} |
```

```{table} Data recorded on December 10 shows that the December 3 observation increased by 26 cases
| *as\_of*     | target_end_date       | location | observation |
|:-------------|:-----------|:---------|------------:|
| *2022-12-10* | 2022-11-19 | 25       |          79 |
| *2022-12-10* | 2022-11-26 | 25       |         221 |
| *2022-12-10* | 2022-12-03 | 25       |        [446]{.bordered} |
| *2022-12-10* | 2022-12-10 | 25       |         578 |
```


If the source data have this pattern of being subsequently updated,
the hubverse recommends recording the date target data were
reported in a column called `as_of`. This will then accurately represent what data were available at a given point in time, and will allow tools like our
[dashboards](dashboards.md) to automatically extract the data that were available for any given model round.

**For configuration details, see [Configuring time-series data](#configuring-time-series-data).**

(target-oracle-output)=
## Oracle output

Oracle output follows a format that is similar to a [hubverse model
output
file](#model-output-example-table),
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
  We introduce some conventions to avoid duplication of data, as described
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
:alt: Simplified graph showing two distributions called "oracle" and "model". The model distribution spans from below -2 to above 4 with a mean of 1, with probabilities below 0.5. The oracle distribution appears as a single line at 2 that has a probability of 1.

Model and Oracle distributions

Just like model outputs are derived from a model distribution, oracle output
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

(oracle-intro-example)=
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
that observed value, so 79 appears as the `oracle_value` for the quantile
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

### Generating oracle output data

A hub will typically have access to data in time series format, and will
need to convert it to the **oracle output** format for use with any tools
that require it in that format (see the next section). In hubs that
collect mean, median, quantile, or sample predictions for the reported
signal values in the raw time series data, the two formats may be
essentially the same, perhaps with some renaming of columns. However,
these data formats will differ more in hubs that form predictions for quantities
that are derived from the raw time series data, such as the peak time or
peak incidence, and in hubs that collect pmf or cdf predictions.


### Task ID columns

**The oracle output should include enough of the task ID variables to uniquely identify which `oracle_values` correspond to which predicted values.** In the [above oracle output example](#oracle-intro-example), the `location`, `target_end_date`, and `target` columns are included because they are necessary to identify _where_ and _when_ a given _target_ was measured as the `oracle_value`.

Similarly, **any task ID variables that are not necessary to match observations with predictions can be omitted from the oracle output.** In the [above oracle output example](#oracle-intro-example), the `horizon`, `model_id`, and `reference_date` columns are not included. Both `horizon` and `reference_date` are related to the `target_end_date` and thus would be redundant. Importantly, _these task ID variables are not applicable for observed data_---they are used for describing model-specific parameters about unknown events. Likewise, in a scenario projection setting, the `scenario_id` can be omitted as there is only one scenario for an observed event[^quanta].

[^quanta]: just don't tell the quantum physicists.

Nonetheless, there are instances in which an output type may require a Task ID variable such as `horizon` to correctly map onto target data, and for such cases there is an option to specify additional task ID variables in the `observable_unit` property (see [Configuring oracle-output data](#configuring-oracle-output-data) for more details).


### Model output representation columns

The `oracle-output` has a unique property, not present in the global or time series properties:

* `has_output_type_ids`: Boolean. Must be `true` if `pmf` or `cdf` output types exist. Can be `false` otherwise. If `true`, the dataset must include `output_type` and `output_type_id` columns. Defaults to `false`.

**The `output_type` and `output_type_id` columns only need to be included if the hub collects `pmf` or `cdf` outputs.** For those two output types, the `oracle_value` depends on the `output_type_id` (see the next section for more detail). On the other hand, the `oracle_value` is not specific to the quantile level for quantile forecasts or the sample index for sample forecasts, and so for these output types (as well as mean and median), the `output_type_id` is not needed to align observations with predictions.

### The `oracle_value` column

Oracle output follows a similar format to model outputs, but the `value`
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

**For configuration details, see [Configuring oracle-output data](#configuring-oracle-output-data).**


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
| wk flu hosp rate | cdf | weekly rate of hospital admissions with flu per 100,000 population |
| wk flu hosp rate category | pmf | categorical severity level of the hospital admissions rate, with levels ‘low’, ‘moderate’, ‘high’, and ‘very high’ |

Below, we show snippets of the contents of a `model_out_tbl` with
example forecast submissions and the corresponding **oracle output** for
each `output_type`. We highlight two points about these objects:

- The `reference_date` and `horizon` columns are included in the model outputs but not in the oracle output (although they could be included if specified under the global or dataset-specific `observable unit` properties).
- In this example, the **oracle output** for the `mean`, `median`,
  `quantile`, and `sample` output types are all the same, and they
  contain `<NA>` values for the `output_type_id`. In a hub without `pmf`
  or `cdf` output types, the `output_type` and `output_type_id` columns
  could be omitted and this duplication could be eliminated.

:::{note}

These examples are all collected and filtered from [the `hubExamples` package](https://hubverse.github.io/hubExamples). The model output data set contains over
10,000 rows, and the oracle output data has over 200,000 rows.

To make comparisons easier, we have subset the data to Massachusetts (FIPS code
25) with one `reference_date` of 2022-11-19 and four target end dates between 2022-11-19 and 2022-12-10.

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
indicates that 79 flu hospitalizations were reported in Massachusetts for the
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
probability 1 to that observed value at any quantile probability level. A
model output file would need to have a separate row for each quantile
level reported in the `output_type_id` column. As a space-saving
convention, we use `output_type_id = <NA>` to indicate that this
`oracle_value` applies to all quantile levels.

### Output type `sample`

:::{table} A subset of **model output** showing 6 `sample` predictions at one horizon
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
from a predictive distribution that assigns probability 1 to the observed
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
Massachusetts on the week of 2022-11-19 was `"low"`. Similarly, the observed rate category for the week of
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

### Optional `as_of` column to record data version source

Oracle output data are most commonly derived from time series data which may be versioned with an `as_of` column. While only a single unique version of an oracle output row (excluding the `oracle_value` column) is allowed, the version (`as_of` value) of the time-series dataset used to derive the `oracle_value` of a particular row can be stored in an optional `as_of` column in oracle output data. This can be useful for tracking the provenance of oracle output data but is not required.

## File formats and naming

Both the *time series* and *oracle output* data are found in [the `target-data/`
directory of a hub](#structure-data-and-code) with the following conventions:

1. time series data MUST be named `time-series`
2. oracle output data MUST be named `oracle-output`
3. files MUST be _either_ `*.csv` or `*.parquet`
4. CSV files MUST be a single continuous file named either `time-series.csv` or
  `oracle-output.csv`
5. parquet files MAY be partitioned (see [partitioning target data](#structure-partitioning-target-data) for details)

For example, this represents a valid time series data set because it is (1)
named "time-series", (3) file extensions end with `.parquet`, and is (5)
partitioned.

```
target-data/
└── time-series/
    ├── as_of=2023-06-03
    │   └── part-0.parquet
    ├── as_of=2023-06-10
    │   └── part-0.parquet
    └── as_of=2023-06-17
        └── part-0.parquet
```

However, if the files above were "csv" files, this would violate (4). For a CSV
time series target file, this is valid:


```
target-data/
└── time-series.csv
```

**Choosing a file format:**

Both CSV and Parquet formats are supported, but they have different characteristics:

- **CSV**: Universal compatibility, human-readable, good for smaller datasets
- **Parquet**: Embedded schema (more robust and reliable), better performance, especially for large datasets and cloud storage (recommended)

(target-data-hub-configuration)=
## Target Data Hub Configuration

This section provides guidance for hub administrators on configuring target data through the `target-data.json` file for optimal performance and usability.

### Performance Considerations

Hub administrators should consider these performance factors when configuring target data:

**File Format Impact:**

Parquet format provides significant performance advantages:
- **Faster queries**: Columnar storage enables efficient filtering
- **Efficient column selection**: Only requested columns are read from disk
- **Better compression**: Reduces storage costs and data transfer
- **Cloud optimization**: Particularly beneficial for S3/GCS where I/O is slower

**For cloud-based hubs**, Parquet format is strongly recommended as it minimizes expensive network operations.

**Configuration Impact:**

Using `target-data.json` (detailed below) provides significant performance benefits:
- **Faster schema creation**: Config-based vs. scanning files, eliminating file I/O
- **Particularly important for cloud hubs**: Avoids slow remote file system operations

The configuration file is optional but **strongly recommended for**:
- Cloud-based hubs (S3, GCS)
- Large datasets
- Hubs prioritizing user experience and data access speed

(configuring-target-data-json)=
### The `target-data.json` configuration file

:::{tip}
For an interactive view of the full `target-data.json` schema, see the [Hub target data configuration interactive schema](#target-data-config).
:::

The `target-data.json` configuration file allows hub administrators to explicitly define target data schemas and properties, improving performance and reliability.

**Why use `target-data.json`?**

Without configuration, hubverse tools must infer schemas by scanning actual data files. This can cause several issues:
- **Inconsistent schema inference**: Different tools or file formats may infer different data types
- **Partition column conflicts**: Parquet partition columns are stored as strings in the file system, which can conflict with the intended data type (e.g., dates stored as strings vs. Date type)
- **Ambiguous data types**: Inference may not always produce the intended type

With `target-data.json`, you get:
- **Deterministic schemas**: Explicit type definitions ensure consistency across all tools
- **Correct data types**: Specify intended types for partition columns and other fields
- **Single source of truth**: One configuration file that all hubverse tools reference

**Configuration structure:**

The file contains two levels of properties:

1. **Global (top-level)**: Default values applying to all target dataset types
2. **Dataset-specific**: Properties for `time-series` and/or `oracle-output` that override global defaults

**Global properties:**

* `observable_unit`: An array of column names whose unique value combinations define the minimum observable unit. Must only include the `date_col`, `target_col` (if present), and any other task ID columns. When versioning is used, unique combinations will also take into account the values in the `as_of` column, though the `as_of` column is never included in the observable unit as it is a versioning column, not a task ID. This property is required.
* `date_col`: The default date column across time-series, oracle-output, and model-output (if present) datasets. Expected to be of type `Date`.
*  `versioned`: Boolean indicating whether all target type datasets use `as_of` versioning by default. If `true`, datasets are expected to have a date `as_of` column indicating the version of each data point. Defaults to `false`. Can be overridden at the dataset level.
* `additional_metadata`: Optional. An object containing hub-specific metadata that isn't part of the standard schema. Use this to store custom information that may be useful for your hub's tooling or documentation. The schema does not validate the contents of this field.

(configuring-time-series-data)=
### Configuring time-series data

Dataset-specific properties for time-series data can be specified under a `"time-series"` key to override global settings.

**Time-series-specific property (no global equivalent):**

* `non_task_id_schema`: Optional. Key-value pairs of non-task ID column names and their R data types, one of (`character`, `double`, `integer`, `logical`, `Date`). Include any columns in the time-series data that do not correspond exactly to a task ID. The `as_of` column does not need to be defined here as it is a reserved column.

**Properties that can override global settings:**

* `observable_unit`: Optional. Names of columns whose unique value combinations define the minimum observable unit for time-series data. Use to override the global `observable_unit` when time-series requires a different set of columns. If not specified or set to `null`, uses the global `observable_unit`.

* `versioned`: Optional. Boolean indicating whether time-series data are versioned using `as_of` dates. Use to override the global `versioned` setting. If not specified, inherits from the global `versioned` property.

Hubverse tools will only validate the content of the columns that make up the unit of observation that match model task IDs. You may also include additional columns that have a 1:1 correspondence with the data---for example, a transformation of counts to rates or a human-readable translation of codes. These should be defined in the `non_task_id_schema` property.

:::{note}
Should you need to validate such additional columns, you can use [custom target data checks](https://hubverse-org.github.io/hubValidations/articles/deploying-custom-functions.html) in hubValidations (see also the guide on [writing custom validation functions](https://hubverse-org.github.io/hubValidations/articles/writing-custom-fns.html)).
:::

(configuring-oracle-output-data)=
### Configuring Oracle-Output Data

Dataset-specific properties for oracle-output data can be specified under an `"oracle-output"` key to override global settings.

**Oracle-output-specific property (no global equivalent):**

* `has_output_type_ids`: Boolean. Must be `true` if `pmf` or `cdf` output types exist. Can be `false` otherwise. If `true`, the dataset must include `output_type` and `output_type_id` columns. Defaults to `false`.

**Properties that can override global settings:**

* `observable_unit`: Optional. Names of task IDs whose unique value combinations define an observable unit in oracle-output data. Each combination of values must be unique once combined with output type IDs if present. Use to override the global `observable_unit` to ensure oracle outputs can be successfully mapped to model outputs for evaluation, particularly when some output types require additional task ID values (see [special case below](#special-case-different-observable-units-between-datasets) for an example). If not specified or set to `null`, uses the global `observable_unit`.

* `versioned`: Optional. Boolean indicating whether oracle-output data are versioned using `as_of` dates. Use to override the global `versioned` setting. If not specified, inherits from the global `versioned` property. Note that oracle-output data is expected to have only a single version of each unique combination of observable unit values, in contrast to time-series which is allowed to have multiple versions. This is to minimize confusion and reduce the risk of downloading multiple observed values and scoring on each of them.

**Important considerations:**

- `output_type` and `output_type_id` columns are only required for `pmf` and `cdf` output types
- For `mean`, `median`, `quantile`, and `sample` outputs, these columns can be omitted

(special-case-different-observable-units-between-datasets)=
**Special case: different observable units between datasets**

In some hubs, oracle-output data may require additional columns in its `observable_unit` that are not present in time-series data.
For example, if your hub collects `pmf` output types with categorical predictions based on `horizon`,
the oracle-output data needs the `horizon` column to determine which pmf category corresponds to the observed outcome.
In this case, the oracle-output observable unit would include `horizon` while the time-series observable unit does not.

This is configured by overriding the global `observable_unit` in the oracle-output dataset-specific configuration.
See the [RFC decision document](https://github.com/reichlab/decisions/blob/main/decisions/2025-06-17-RFC-target-data-metadata.md) for detailed examples.

### Configuration Examples

The following examples demonstrate common `target-data.json` configurations for different hub scenarios.

#### Example 1: Versioned Hub

A basic configuration for a hub that maintains versioned target data:

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
  "observable_unit": ["target_date", "location", "target"],
  "date_col": "target_date",
  "versioned": true
}
```

This configuration defines a global observable unit and versioning for all target datasets.

#### Example 2: Non-Task ID Columns

A configuration that includes additional non-task ID columns with explicit data type declarations:

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
  "observable_unit": ["target_date", "location", "target"],
  "date_col": "target_date",
  "time-series": {
    "non_task_id_schema": {
      "location_name": "character"
    }
  }
}
```

The `non_task_id_schema` property specifies data types for additional columns that provide context alongside task IDs (like human-readable location names).

#### Example 3: Oracle Output with Output Type IDs

A configuration for oracle outputs containing `output_type` and `output_type_id` columns for pmf/cdf structures:

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
  "observable_unit": ["target_date", "location", "target"],
  "date_col": "target_date",
  "oracle-output": {
    "has_output_type_ids": true
  }
}
```

Set `has_output_type_ids` to `true` when your oracle-output data includes `pmf` or `cdf` output types.

#### Example 4: Dataset-Specific Overrides

A configuration demonstrating hierarchical overrides where oracle-output uses different observable units and versioning than time-series data:

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
  "observable_unit": ["target_date", "location", "target"],
  "date_col": "target_date",
  "versioned": true,
  "oracle-output": {
    "observable_unit": ["target_date", "location", "target", "horizon"],
    "versioned": false
  }
}
```

This example shows how oracle-output can override global settings. Here it requires `horizon` in its observable unit (see [special case above](#special-case-different-observable-units-between-datasets)) and disables versioning for oracle-output while keeping it enabled for time-series.

#### Example 5: custom metadata

A configuration showing how to include hub-specific metadata while maintaining schema compliance:

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
  "observable_unit": ["target_date", "location", "target"],
  "date_col": "target_date",
  "additional_metadata": {
    "data_source": "CDC NNDSS",
    "collection_year": 2024,
    "is_provisional": true,
    "reporting_jurisdictions": ["state", "territory"],
    "update_schedule": {
      "frequency": "weekly",
      "day": "Thursday"
    }
  }
}
```

Use `additional_metadata` to store hub-specific information that isn't part of the standard schema but may be useful for your hub's tooling or documentation.

## Access and distribution

Hubs should ensure that standardized procedures for accessing target
data are available. The data formats that a hub provides may depend on
the needs of the specific hub and which hubverse tools the hub wants to
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
guidelines, or if the code is small in scope, it can be placed within the
`src` folder of the hub’s repository.

