# Model output

## Directory structure
The `model-output` directory in a modeling hub is required to have the following subdirectory and file structure:

* `team1-modela`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)
   * `<round-id2>-<model_id>.csv` (or parquet, etc)
* `team1-modelb`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)
* `team2-modela`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)

where `model_id` = `team_abbr-model_abbr`

Note that file names are also allowed to contain the following compression extension prefixes: .snappy, .gzip, .gz, .brotli, .zstd, .lz4, .lzo, .bz2, e.g. `<round-id1>-<model_id>.gz.parquet`.

(model-output-format)=
## Formats of model output
```{margin}
Shandross, L., Howerton, E., Contamin, L., Hochheiser, H., Krystalli, A., Consortium of Infectious Disease Modeling Hubs, Reich, N. G., Ray, E.L. (2024). [hubEnsembles: Ensembling Methods in R](https://github.com/hubverse-org/hubEnsemblesManuscript). *(under review for publication)*.
```

```{admonition} Reference
Much of the material in this section has been excerpted and/or adapted from the [hubEnsembles manuscript](https://github.com/hubverse-org/hubEnsemblesManuscript).  
```

Model outputs are a specially formatted tabular representation of predictions. Each row corresponds to a single, unique prediction and each column provides information about what is being predicted, its scope, and its value. Per hubverse convention, there are three groups of columns, each group serving a specific purpose: (1) the "model ID" denotes which model has produced the prediction, (2) the "task IDs" provide details about what is being predicted, and (3) the "model output representation" specifies how the prediction is represented. More detail about each of these is given in the following points:  

   1. Each model should have a unique identifier that is stored in the `model-id` column.
   2. The details of the outcome (the model task) are provided by the modeler, and can be stored in a series of "task ID" columns as described [in this section on task ID variables](#task-id-vars). These "task ID" columns may also include additional information, such as any conditions or assumptions that were used to generate the predictions. Some example variables include `target`, `location`, `reference_date`, and `horizon`. Although there are no restrictions on naming task ID variables, when appropriate, we suggest that Hubs adopt the standard task ID or column names and definitions specified [in the section on usage of task ID variables](#task-id-use).  
   3. "Model output representation" consists of a set of three columns specifying how the model outputs are represented. All three of these columns will be used by all Hubs:  
      1. `output_type` specifies the type of representation of the predictive distribution, namely `"mean"`, `"median"`, `"quantile"`, `"cdf"`, `"cmf"`, `"pmf"`, or `"sample"`.  
      2. `output_type_id` specifies more identifying information specific to the output type.  
      3. `value` contains the model’s prediction.  
     
The following table provides examples that better explain how the "model output representation" columns are used:  

```{margin}
Note on `pmf` model output type: Values are required to sum to 1 across all `output_type_id` values within each combination of values of task id variables. This representation should only be used if the outcome variable is truly discrete; if the categories would represent a binned discretization of an underlying continuous variable  a CDF representation is preferred.
```

```{margin}
Note on `sample` model output type: Depending on the Hub specification, samples with the same sample index (specified by the `output_type_id`) may be assumed to correspond to a single sample from a joint distribution across multiple levels of the task id variables. This is discussed more below.
```

```{margin}
Note on `cdf` model output type and `pmf` output type for ordinal variables: In the hub's `tasks.json` configuration file, the values of the `output_type_id` should be listed in order from low to high.
```
(output-type-table)=
| `output_type` | `output_type_id` | `value` |
| ------ | ------ | ------ | 
| `mean` | NA (not used for mean predictions) | Numeric: the mean of the predictive distribution |
| `median` | NA (not used for median predictions) | Numeric: the median of the predictive distribution |
| `quantile` | Numeric between 0.0 and 1.0: a probability level | Numeric: the quantile of the predictive distribution at the probability level specified by the output_type_id |
| `cdf` | String or numeric: a possible value of the target variable | Numeric between 0.0 and 1.0: the value of the cumulative distribution function of the predictive distribution at the value of the outcome variable specified by the output_type_id |
| `pmf` | String naming a possible category of a discrete outcome variable | Numeric between 0.0 and 1.0: the value of the probability mass function of the predictive distribution when evaluated at a specified level of a categorical outcome variable. |
| `sample` | Positive integer sample index | Numeric: a sample from the predictive distribution.


We emphasize that the `mean`, `median`, `quantile`, `cdf`, and `pmf` representations all summarize the marginal predictive distribution for a single combination of model task id variables. On the other hand, the `sample` representation may capture dependence across combinations of multiple model task id variables by recording samples from a joint predictive distribution. For example, suppose that the model task id variables are “forecast date”, “location” and “horizon”. A predictive mean will summarize the predictive distribution for a single combination of forecast date, location and horizon. On the other hand, there are several options for the distribution from which a sample might be drawn, capturing dependence across different levels of the task id variables, including:
1. the joint predictive distribution across all locations and horizons within each forecast date
2. the joint predictive distribution across all horizons within each forecast date and location
3. the joint predictive distribution across all locations within each forecast date and horizon
4. the marginal predictive distribution for each combination of forecast date, location, and horizon

Hubs should specify the collection of task id variables for which samples are expected to capture dependence; e.g., the first option listed above might specify that samples should be drawn from distributions that are “joint across” locations and horizons.  

More details about sample-output-type can be found in [the page describing sample output type data](../user-guide/sample-output-type.md).
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

(model-output-schema)=
## The importance of a stable model output file schema

> Note the difference in the following discussion between [hubverse schema](https://github.com/hubverse-org/schemas) - the schema which hub config files are validated against - and [`arrow schema`](https://arrow.apache.org/docs/11.0/r/reference/Schema.html) - the mapping of model output columns to data types.

Because we store model output data as separate files but open them as a single [`arrow` dataset](https://arrow.apache.org/docs/r/reference/Dataset.html) using the `hubData` package, for a hub to be [successfully accessed and fully queryable across all columns as an `arrow dataset`](https://arrow.apache.org/docs/r/articles/dataset.html), it is necesssary to ensure that all files conform to the same [`arrow schema`](https://arrow.apache.org/docs/11.0/r/reference/Schema.html) (i.e. share the same column data types) across the lifetime of the hub. This means that additions of new rounds should not change the overall hub schema at a later date (i.e. after submissions have already started being collected). 

Many common task IDs are covered by the [hubverse schema](#model-tasks-tasks-json-interactive-schema), are validated during hub config validation and should therefore have consistent and stable data types. However, there are a number of situations where a single consistent data type cannot be guaranteed, e.g.:
- New rounds introducing changes in custom task ID value data types, which are not covered by the hubverse schema. 
- New rounds introducing changes in task IDs covered by the schema but which accept multiple data types (e.g. `scenario_id` where both `integer` and `character` are accepted or `age_group` where no data type is specified in the hubverse schema).
- Adding new output types, which might introduce `output_type_id` values of a new data type.

While validation of config files will alert hub administrations to discrepancies in task ID value data types across modeling tasks and rounds, any changes to a hub's config which has the potential to change the overall data type of model output columns after submissions have been collected could cause issues downstream and should be avoided. These issues can range from data type casting being required in downstream analysis code that used to work, not being able to filter on columns with data type discrepancies between files before collecting to an inability to open hub model output data as an `arrow` dataset. They are primarily a problem for parquet files, which encapsulate a schema within the file, but have a small chance to cause parsing errors in csvs too.

(output-type-id-datatype)=
### The `output_type_id` column data type

Output types are configured and handled differently than task IDs in the hubverse. 

On the one hand, **different output types can have output type ID values of varying data type** and adhering to these data types is imposed by downstream, output type specific hubverse functionality like ensembling or visualisation.
For example, hubs expect `double` output type ID values for `quantile` output types but `character` output type IDs for a `pmf` output type. 

 On the other hand, the **use of a long format for hubverse model output files requires that these multiple data types are accomodated in a single `output_type_id` column.**
This makes the output type ID column unique within the model output file in terms of how it's data type is determined, configured and validated. 

During submission validation, two checks are performed on the `output_type_id` column:
1. **Subsets of `output_type_id` column values** associated with a given output type are **checked for being able to be coerced to the correct data type defined in the config** for that output type. This ensures correct output type specific downstream handling of the data is possible.
2. The **overall data type of the `output_type_id` column** matches the overall hub schema expectation.

#### Determining the overall `output_type_id` column data type automatically

 To determine the overall `output_type_id` data type, the default behaviour is to automatically **detect the simplest data type that can encode all output type ID values across all rounds and output types** from the config. 
 
 The benefit of this automatic detection is that it provides flexibility to the `output_type_id` column to adapt to the output types a hub is actually collecting. For example, a hub which only collects `mean` and `quantile` output types would, by default, have a `double` `output_type_id` column.

 The risk of this automatic detection however arises if, in subsequent rounds -after submissions have begun-, the hub decides to also start collecting a `pmf` output type. This would change the default `output_type_id` column data type from `double` to `character` and cause a conflict between the `output_type_id` column data type in older and newer files when trying to open the hub as an `arrow` dataset.

### Fixing the `output_type_id` column data type with the `output_type_id_datatype` property

To enable hub administrators to configure and communicate the data type of the `output_type_id` column at a hub level, the hubverse schema allows for the use of an optional `output_type_id_datatype` property.
This property should be provided at the top level of `tasks.json` (i.e. sibling to `rounds` and `schema_version`), can take any of the following values: `"auto"`, `"character"`, `"double"`, `"integer"`, `"logical"`, `"Date"` and can be used to fix the `output_type_id` column data type.

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v3.0.1/tasks-schema.json",
  "rounds": [...],
  "output_type_id_datatype": "character"
}
```
If not supplied or if `"auto"` is set, the default behaviour of automatically detecting the data type from `output_type_id` values is used.

This gives hub administrators the ability to future-proof the `output_type_id` column in their model output files if they are unsure whether they may start collecting an output type that could affect the schema, by setting the column to `"character"` (the safest data type that all other values can be encoded as) at the start of data collection.

