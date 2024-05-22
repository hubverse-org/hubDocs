# Model output

## Directory structure
The `model-output` directory in a modeling hub is required to have the following subdirectory and file structure:

* `team1-modela`
   * `<round-id1>.csv` (or parquet, etc)
   * `<round-id2>.csv` (or parquet, etc)
* `team1-modelb`
   * `<round-id1>.csv` (or parquet, etc)
* `team2-modela`
   * `<round-id1>.csv` (or parquet, etc)


(model_output_format)=
## Formats of model output
Model outputs are contributed by teams, and are represented in a rectangular format, where each row corresponds to a unique model output and columns define: (1) the model task, (2) specification of the representation of the model output, and (3) the model output value. More detail about each of these is given in the following points:

* Task ids: A set of columns specifying the model task, as described [here](task_id_vars). The columns used as task ids will vary across different Hubs.

* Model output representation: A set of three columns specifying how the model outputs are represented. All three of these columns will be used by all Hubs:
   1. `output_type` specifies the type of representation of the predictive distribution
   2. `output_type_id` specifies more identifying information specific to the output type
   3. `value` contains the model’s prediction
These are described more in the following table:

```{margin}
Note on `pmf` model output type: Values are required to sum to 1 across all `output_type_id` values within each combination of values of task id variables. This representation should only be used if the outcome variable is truly discrete; if the categories would represent a binned discretization of an underlying continuous variable  a CDF representation is preferred.
```

```{margin}
Note on `sample` model output type: Depending on the Hub specification, samples with the same sample index (specified by the `output_type_id`) may be assumed to correspond to a joint distribution across multiple levels of the task id variables. This is discussed more below.
```
(output_type_table)=
| `output_type` | `output_type_id` | `value` |
| ------ | ------ | ------ | 
| `mean` | NA (not used for mean predictions) | Numeric: the mean of the predictive distribution |
| `median` | NA (not used for median predictions) | Numeric: the median of the predictive distribution |
| `quantile` | Numeric between 0.0 and 1.0: a probability level | Numeric: the quantile of the predictive distribution at the probability level specified by the output_type_id |
| `cdf` | Numeric within the support of the outcome variable: a possible value of the target variable | Numeric between 0.0 and 1.0: the value of the cumulative distribution function of the predictive distribution at the value of the outcome variable specified by the output_type_id |
| `pmf` | String naming a possible category of a discrete outcome variable | Numeric between 0.0 and 1.0: the value of the probability mass function of the predictive distribution when evaluated at a specified level of a categorical outcome variable. |
| `sample` | Positive integer sample index | Numeric: a sample from the predictive distribution.


We emphasize that the `mean`, `median`, `quantile`, `cdf`, and `pmf` representations all summarize the marginal predictive distribution for a single combination of model task id variables. On the other hand, the `sample` representation may capture dependence across combinations of multiple model task id variables by recording samples from a joint predictive distribution. For example, suppose that the model task id variables are “forecast date”, “location” and “horizon”. A predictive mean will summarize the predictive distribution for a single combination of forecast date, location and horizon. On the other hand, there are several options for the distribution from which a sample might be drawn, capturing dependence across different levels of the task id variables, including:
1. the joint predictive distribution across all locations and horizons within each forecast date
2. the joint predictive distribution across all horizons within each forecast date and location
3. the joint predictive distribution across all locations within each forecast date and horizon
4. the marginal predictive distribution for each combination of forecast date, location, and horizon

Hubs should specify the collection of task id variables for which samples are expected to capture dependence; e.g., the first option listed above might specify that samples should be drawn from distributions that are “joint across” locations and horizons.

More details about sample-output-type can be found in [sample-output-type](https://hubverse.io/en/latest/user-guide/sample-output-type.html).
Here is an example for a Hub that collects mean and quantile forecasts for one-week-ahead incidence, but probabilities for the timing of a season peak:


| `origin_epiweek` | `target` | `horizon` | `output_type` | `output_type_id` | `value` |
| ------ | ------ | ------ | ------ | ------ | ------ | 
| EW202242 | weekly rate | 1 | mean     | NA | 5 |
| EW202242 | weekly rate | 1 | quantile | 0.25 | 2 |
| EW202242 | weekly rate | 1 | quantile | 0.5 | 3 |
| EW202242 | weekly rate | 1 | quantile | 0.75 | 10 |
| EW202242 | weekly rate | 1 | pmf | 0 | 0.1 |
| EW202242 | weekly rate | 1 | pmf | 0.1 | 0.2 |
| EW202242 | weekly rate | 1 | pmf | 0.2 | 0.7 |
| EW202242 | peak week | NA | pmf | EW202240 | 0.001 |
| EW202242 | peak week | NA | pmf | EW202241 | 0.002 |
| EW202242 | ... | ... | ... | ... | ... |
| EW202242 | peak week | NA | pmf | EW202320 | 0.013 |
| EW202242 | weekly rate | 1 | sample | 1 | 3 |
| EW202242 | weekly rate | 1 | sample | 2 | 3 |

We will develop tools that support multiple formats for the submissions, including csv, zipped csv, and parquet. Initial data loading functions will load data and return standard data output types for each language (e.g. data frames).


## Other output types
Some other possible model output representations have been proposed, but are not included on the list above. We document these other proposals and the reasons for their omissions here:

* Other output types of point forecasts.  
* Bin probability. Two notes:
   * If the bins have open left endpoints and closed right endpoints, bin probabilities can be calculated directly from CDF values.
   * We considered a system with a more flexible specification of bin endpoint inclusion status, but noted two disadvantages:
      * This additional flexibility would introduce substantial extra complexity to the metadata specifications and tooling
      * It might be beneficial to adopt limited standards that encourage Hubs to adopt settings that are consistent with the common definitions. For example, if a Hub were to adopt bins with open right endpoints, the resulting probabilities would be incompatible with the conventions around cumulative distribution functions.
* Probability of “success” in a setting with a binary outcome
   * This can be captured with a CDF representation if the outcome variable is ordered, or a categorical representation if the outcome variable is not ordered.
* Compositional. For example, we might request a probabilistic forecast of the proportion of hospitalizations next week that are due to influenza A/H1, A/H3, and B.
   * Note that if only point forecasts for the composition were required, a categorical output representation could be used.

## Validating forecast values
Validation of forecast values occurs in two steps:

* The data output types and relatively simple limits on values are specified in a json schema file. For example, if appropriate, we might specify that the value is a non-negative integer.

* Validation of more involved rules that cannot be encoded in a json schema are implemented separately. Examples of such rules include:
   1. A predictive quantile for disease incidence may not be larger than the population size in that location.
   2. The probabilities assigned to bins must be non-negative and must sum to 1 within each model task, up to some specified tolerance.

## File formats
* Considerations about `csv`:
   1. Some projects have run into 100 MB file size limits when using csv formatted files.
* Considerations about `parquet`:
   * Advantages:
      * Speed
      * Size: In combination, splitting files up and using parquet would get around GitHub limits on file sizes
      * Loads only data that are needed
   * Disadvantages:
      * Harder to work with; teams and people who want to work with files need to install additional libraries
