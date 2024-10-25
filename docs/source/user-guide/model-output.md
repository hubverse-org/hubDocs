# Model output

## Directory structure

The `model-output`[^model-output] directory in a modeling hub is required to have the following subdirectory and file structure:

* `team1-modelA`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)
   * `<round-id2>-<model_id>.csv` (or parquet, etc)
* `team1-modelB`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)
* `team2-modelA`
   * `<round-id1>-<model_id>.csv` (or parquet, etc)

where `model_id` = `team_abbr-model_abbr`

Note that file names are also allowed to contain the following compression extension prefixes: .snappy, .gzip, .gz, .brotli, .zstd, .lz4, .lzo, .bz2, e.g. `<round-id1>-<model_id>.gz.parquet`.

[^model-output]: The directory is required, but the name is flexible. You can
    use a custom directory path by setting the `"model_output_dir"` property in the
    `admin.json` file. More details can be found in the `admin.json` schema
    definition.

(model-output-example-table)=
### Example model submission file

Each model submission file will have the same representation for each hub. Here
is an example of a hub that collects mean and quantile forecasts for
one-week-ahead incidence, but probabilities for the timing of a season peak:  

:::{table} An example of a model output submission for modelA
| `origin_epiweek` | `target` | `horizon` | `output_type` | `output_type_id` | `value` |
| ------ | ------ | ------ | ------ | ------ | ------ | 
| EW202242 | weekly rate | 1 | mean     | NA[^batman] | 5 |
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
:::

[^batman]: `NA` (without quotes) indicates missingness in R, which is the expected `output_type_id` for a `mean` `output_type`. 
  This is discussed in the [output type table](#output-type-table)


(file-formats)=
### File formats

Hubs can take submissions in tabular data formats, namely `csv` and `parquet`. These
submission formats are _not mutually exclusive_; **hubs may choose between
 `parquet` (Arrow), `csv`, or both**. Both formats have advantages and tradeoffs:

* Considerations about `csv`:
   * Advantages
     * Compatibility: Files are human-readable and are widely supported by many tools
   * Disadvantages:
     * Size: Some projects have run into 100 MB file size limits when using `csv` formatted files.
* Considerations about `parquet`:
   * Advantages:
      * Speed
      * Size: In combination, splitting files up and using `parquet` would get around GitHub limits on file sizes
      * Loads only data that are needed
   * Disadvantages:
      * Compatibility: Harder to work with; teams and people who want to work with files need to install additional libraries

Examples of how to create these file formats in R and Python are listed below in
[the writing model output section](#writing-model-output).

(formats-of-model-output)=
## Formats of model output

```{admonition} Reference
Much of the material in this section has been excerpted or adapted from the [hubEnsembles manuscript](https://github.com/hubverse-org/hubEnsemblesManuscript).[^Shandross-etal]
```

[^Shandross-etal]: Shandross, L., Howerton, E., Contamin, L., Hochheiser, H., Krystalli, A., Consortium of Infectious Disease Modeling Hubs, Reich, N. G., Ray, E.L. (2024). [hubEnsembles: Ensembling Methods in R](https://www.medrxiv.org/content/10.1101/2024.06.24.24309416v1). *(under review for publication)* (Repo: https://github.com/hubverse-org/hubEnsemblesManuscript).

_Model outputs are a specially formatted tabular representation of predictions._
Each row corresponds to a unique prediction, and each column provides information about what is being predicted, its scope, and its value. 
Per hubverse convention, **there are two groups of columns providing metadata about the prediction**[^model-id], followed by **a value column with the actual output**. Each group of columns serves a specific purpose: (1) the **"task ID"** columns provide details about what is being predicted, and (2) the two **"model output representation"** columns specify the type of prediction and identifying information about that prediction. Finally, (3) the **value** column provides the model output of the prediction.  

[^model-id]: When using models for downstream analysis with the [`collect_hub()` function](https://hubverse-org.github.io/hubData/reference/collect_hub.html) in the `hubData` package, one more column called `model_id` is prepended added that identifies the model from its filename. 

As shown in the [model output submission table](#model-output-example-table) above, there are three **"task ID"** columns: `origin_epiweek`, `target`, and `horizon`; and there are two **"model output representation"** columns: `output_type` and `output_type_id` followed by the `value` column.  
More detail about each of these column groups is given in the following points:  


1. **"Task IDs" (multiple columns)**:  The details of the outcome (the model task) are provided by the modeler and can be stored in a series of "task ID" columns as described in this [section on task ID variables](#task-id-vars). These "task ID" columns may also include additional information, such as any conditions or assumptions used to generate the predictions. Some example task ID variables include `target`, `location`, `reference_date`, and `horizon`. Although there are no restrictions on naming task ID variables, we suggest that hubs adopt the standard task ID or column names and definitions specified in the [section on usage of task ID variables](#task-id-use) when appropriate.  
2. **"Model output representation" (2 columns)**: consists of two columns specifying how the model outputs are represented. Both of these columns will be present in all model output data:  
    1. `output_type`{.codeitem} specifies the type of representation of the predictive distribution, namely `"mean"`, `"median"`, `"quantile"`, `"cdf"`, `"cmf"`, `"pmf"`, or `"sample"`.  
    2. `output_type_id`{.codeitem} specifies more identifying information specific to the output type, which varies depending on the `output_type`.  
3. `value`{.codeitem} contains the model’s prediction.  


The following table provides more detail on how to configure the three "model output representation" columns based on each model output type.

(output-type-table)=
:::{table} Relationship between the three model output representation columns with respect to the type of prediction (`output_type`)
| `output_type` | `output_type_id` | `value` |
| ------ | ------ | ------ | 
| `mean` | `NA`/`None` (not used for mean predictions) | Numeric: the mean of the predictive distribution |
| `median` | `NA`/`None` (not used for median predictions) | Numeric: the median of the predictive distribution |
| `quantile` | Numeric between 0.0 and 1.0: a probability level | Numeric: the quantile of the predictive distribution at the probability level specified by the output_type_id |
| `cdf` | String or numeric: a possible value of the target variable | Numeric between 0.0 and 1.0: the value of the cumulative distribution function of the predictive distribution at the value of the outcome variable specified by the output_type_id |
| `pmf` | String naming a possible category of a discrete outcome variable | Numeric between 0.0 and 1.0: the value of the probability mass function of the predictive distribution when evaluated at a specified level of a categorical outcome variable. |
| `sample` | Positive integer sample index | Numeric: a sample from the predictive distribution.
:::

:::{note} 
:name: output-type-caveats

The model output type IDs have different caveats depending on the `output_type`:

`mean` and `median`
: Point estimates do not have an `output_type_id` because you can only have one
point estimate for each combination of task IDs. However, because the
`output_type_id` column is required, something has to go in this place, which
is a missing value. This is encoded as [`NA` in
R](https://www.njtierney.com/post/2020/09/17/missing-flavour/) (which is why
our schemas prior to 4.0.0 encoded these as `["NA"]`) and `None` in Python. See
[The example on writing parquet files](#example-parquet) for details.

`pmf`
: Values are required to sum to 1 across all
`output_type_id` values within each combination of values of task ID variables.
This representation should only be used if the outcome variable is truly
discrete; a CDF representation is preferred if the categories represent a
binned discretization of an underlying continuous variable.

`sample`
: Depending on the hub specification, samples with the same sample index
(specified by the `output_type_id`) may be assumed to correspond to a single
sample from a joint distribution across multiple levels of the task ID
variables — further details are discussed below.


`cdf` (and `pmf` for ordinal variables)
: In the hub's `tasks.json` configuration file, the values of the
`output_type_id` should be listed in order from low to high.

:::

(writing-model-output)=
## Writing model output to a hub

When submitting model output to a hub, it should be placed in a folder with the
name of your model in the model outputs folder specified by the hub
administrator (this is usually called `model-output`). Below are two examples
of writing model output to a hub in R and Python using parquet and CSV files.
In these examples, we are assuming the following variables already exist:

 - `model_out_tbl` is the tabular output from your model formatted as specified
   in [the formats of model output section](#formats-of-model-output).
 - `hub_path` is the path to the hub cloned on your local computer
 - `file_name` is the file name of your model formatted as
   `<round_id>-<model_id>.csv` (or parquet)

(example-csv)=
### Example: model output as CSV

To write to CSV, you would use the `write_csv()` from the `readr` package in R and
the `to_csv()` method in Python. 

#### Writing CSV with R

```r
library("fs")
library("readr")
# ... generate model data ...
outfile <- path(hub_path, "model-output", "team1-modelA", model_id)
write_csv(model_out_tbl, outfile)
```

#### Writing CSV with Python

```python
import pandas as pd
import os.path
# ... generate model data ...
outfile = os.path.join(hub_path, "model-output", "team1-modelA", model_id)
model_out_tbl.to_csv(outfile, index = False, na_rep = "NA")
```

(example-parquet)=
### Example: model output as parquet

Writing to parquet is similar as writing to CSV, but with the caveat that you
additionally need to ensure that the `output_type_id` column matches the
[expected `output_type_id_datatype` property of the schema](#output-type-id-datatype).
In practice, you will need to know whether or not the expected data type is a
**string/character** or a **float/numeric**.


#### Writing parquet with R

```r
library("fs")
library("arrow")
# ... generate model data ...
outfile <- path(hub_path, "model-output", "team1-modelA", model_id)
model_out_tbl$output_type_id <- as.character(model_out_tbl$output_type_id) # or as.numeric()
arrow::write_parquet(model_out_tbl, outfile)
```


#### Writing parquet with Python

```python
import pandas as pd
import os.path
# ... generate model data ...
outfile = os.path.join(hub_path, "model-output", "team1-modelA", model_id)
model_out_tbl["output_type_id"] = model_out_tbl["output_type_id"].astype("string") # or "float"
model_out_tbl.to_parquet(outfile)
```

(model-output-task-relationship)=
## Model output relationships to task ID variables

We emphasize that the `mean`, `median`, `quantile`, `cdf`, and `pmf` representations all **summarize the marginal predictive distribution for a single combination of model task ID variables**. 
In contrast, we cannot assume the same for the `sample` representation.
By recording samples from a joint predictive distribution, **the `sample` representation may capture dependence across combinations of multiple model task ID variables**.

For example, suppose the model task ID variables are “forecast date”, “location”, and “horizon”. 
A predictive mean will summarize the predictive distribution for a single combination of forecast date, location, and horizon. On the other hand, there are several options for the distribution from which a sample might be drawn, capturing dependence across different levels of the task ID variables, including:
1. the joint predictive distribution across all locations and horizons within each forecast date
2. the joint predictive distribution across all horizons within each forecast date and location
3. the joint predictive distribution across all locations within each forecast date and horizon
4. the marginal predictive distribution for each combination of forecast date, location, and horizon

Hubs should specify the collection of task ID variables for which samples are expected to capture dependence; e.g., the first option listed above might specify that samples should be drawn from distributions that are “joint across” locations and horizons.  

More details about sample-output-type can be found in the [page describing sample output type data](../user-guide/sample-output-type.md).

### Omitted output types

Some other possible model output representations have been proposed but not included in the list above. We document these other proposals and the reasons for their omissions here:

#### Point estimates

* Bin probability. Two notes:
   * If the bins have open left endpoints and closed right endpoints, bin probabilities can be calculated directly from CDF values.
   * We considered a system with a more flexible specification of bin endpoint inclusion status but noted two disadvantages:
      * This additional flexibility would introduce substantial extra complexity to the metadata specifications and tooling
      * Adopting limited standards that encourage hubs to adopt settings consistent with the common definitions might be beneficial. For example, if a hub adopted bins with open right endpoints, the resulting probabilities would be incompatible with the conventions around cumulative distribution functions.
* Probability of “success” in a setting with a binary outcome
   * This can be captured with a CDF representation if the outcome variable is ordered or a categorical representation if the outcome variable is not.
* Compositional. For example, we might request a probabilistic estimate of the proportion of hospitalizations next week due to influenza A/H1, A/H3, and B.
   * Note that a categorical output representation could be used if only point estimates for the composition were required.

## Validating prediction values

Before model outputs can be incorporated into a hub, they must be validated. If a hub is centrally stored on GitHub, validation checks will be automatically performed for each submission (via the [`validate_pr()` function](https://hubverse-org.github.io/hubValidations/reference/validate_submission.html) from the `hubValidations` R package).  

Teams can also validate their submissions locally via the function 
[`validate_submissions()`](https://hubverse-org.github.io/hubValidations/reference/validate_submission.html)
from the `hubValidations` R package, which performs two validation tasks:

* Validation based on rules that can easily be encoded in the JSON schema, such as
  ranges of expected values and `output_type_id`s. 

* Validation of more involved rules that cannot be encoded in a json schema are
  implemented separately (such as specific relationships between outputs and
  targets). You can find a table with the details of each check in the [`validate_submission()` documentation](https://hubverse-org.github.io/hubValidations/reference/validate_submission.html#details) and the [`validate_pr()` documentation](https://hubverse-org.github.io/hubValidations/reference/validate_pr.html#details).


(model-output-schema)=
## The importance of a stable model output file schema

```{admonition} NOTE
The following discussion addresses two different types of schemas:
 - [hubverse schema](https://github.com/hubverse-org/schemas)---the schema used for **validating hub configuration files**
 - [Arrow schema](https://arrow.apache.org/docs/11.0/r/reference/Schema.html)---the mapping of model output columns to Arrow data types.

This section concerns parquet files, which encapsulate a schema within the file, but the broader issues have consequences for all output file types.
```


Model output data are stored as separate files, but we use the `hubData` package to open them as a single [Arrow dataset](https://arrow.apache.org/docs/r/reference/Dataset.html).[^trouble]
**It is necessary to ensure that all files conform to the same Arrow schema** (i.e., share the same column data types) across the hub's lifetime.
When we know that all data types conform to the Arrow schema, we can be sure that a hub can be successfully accessed and is fully queryable across all columns as [an Arrow dataset](https://arrow.apache.org/docs/r/articles/dataset.html)
Thus, **additions of new rounds _should not_ change the overall hub schema at a later date** (i.e., after submissions have already started being collected). 

[^trouble]: Even if you do not use `hubData` to read model outputs, uniform schemas are still important if you want to join model output files and do analyses across submissions.

Many common task IDs should have consistent and stable data types because they are validated against the [task IDs in the hubverse schema](#model-tasks-schema) during model submission.
However, there are several situations where a single consistent data type cannot be guaranteed, e.g.:
- New rounds introducing changes in custom task ID value data types, which are not covered by the hubverse schema. 
- New rounds introducing changes in task IDs covered by the schema but which accept multiple data types (e.g., `scenario_id` where both `integer` and `character` are accepted or `age_group` where no data type is specified in the hubverse schema).
- Adding new output types might introduce `output_type_id` values of a new data type.

While config file validation will alert hub administrations to discrepancies in task ID value data types across modeling tasks and rounds, modifications that change the overall data type of model output columns _after submissions have been collected_ could cause downstream issues and _should be avoided_.
Changing the overall data type of model output columns can cause a range of issues (in order of _increasing severity_):
 - data type casting being required in downstream analysis code that used to work, 
 - not being able to filter on columns with data type discrepancies between files before collecting
 - errors when opening hub model output data with popular analytics tools like Arrow, Pandas, and Polars

(output-type-id-datatype)=
### The `output_type_id` column data type

Output types are configured and handled differently than task IDs in the hubverse. 

On the one hand, **different output types can have output type ID values of varying data type**, and adhering to these data types is imposed by downstream, output type-specific hubverse functionality like ensembling or visualization.
For example, hubs expect `double` output type ID values for `quantile` output types but `character` output type IDs for a `pmf` output type. 

 On the other hand, the **use of a long format for hubverse model output files requires that these multiple data types are accommodated in a single `output_type_id` column.**
This characteristic makes the output type ID column unique within the model output file in terms of how its data type is determined, configured, and validated. 

During submission validation, two checks are performed on the `output_type_id` column:
1. **Subsets of `output_type_id` column values** associated with a given output type are **checked for being able to be coerced to the correct data type defined in the config** for that output type. This check ensures that correct output type–specific downstream data handling is possible.
2. The **overall data type of the `output_type_id` column** matches the overall hub schema expectation.

#### Determining the overall `output_type_id` column data type automatically

 To determine the overall `output_type_id` data type, the default behavior is to automatically **detect the simplest data type that can encode all output type ID values across all rounds and output types** from the config. 
 
 The benefit of this automatic detection is that it provides flexibility to the `output_type_id` column to adapt to the output types a hub is collecting. For example, a hub that only collects `mean` and `quantile` output types would, by default, have a `double` `output_type_id` column.

 However, the risk of this automatic detection arises if the hub also starts collecting a `pmf` output type after submissions have begun in subsequent rounds. If this happens, it would change the default `output_type_id` column data type from `double` to `character` and cause a conflict between the `output_type_id` column data type in older and newer files when trying to open the hub as an `arrow` dataset.

### Fixing the `output_type_id` column data type with the `output_type_id_datatype` property

To enable hub administrators to configure and communicate the data type of the `output_type_id` column at a hub level, the hubverse schema allows for using an optional `output_type_id_datatype` property.
This property should be provided at the top level of `tasks.json` (i.e., sibling to `rounds` and `schema_version`) and can take any of the following values: `"auto"`, `"character"`, `"double"`, `"integer"`, `"logical"`, `"Date"` and can be used to fix the `output_type_id` column data type.

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v3.0.1/tasks-schema.json",
  "rounds": [...],
  "output_type_id_datatype": "character"
}
```
If not supplied or if `"auto"` is set, the default behavior of automatically detecting the data type from `output_type_id` values is used.

This feature gives hub administrators the ability to future-proof the `output_type_id` column in their model output files if they are unsure whether they may start collecting an output type that could affect the schema by setting the column to `"character"` (the safest data type that all other values can be encoded as) at the start of data collection.

