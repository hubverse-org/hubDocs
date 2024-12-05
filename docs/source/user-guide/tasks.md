# Defining modeling tasks

Every hub is organized around a set of "modeling tasks". These modeling tasks define how the target data should be modeled in terms of 

1. what variables to use for modeling (e.g., date, location, variant, etc) and 
2. the specific format of the model output.

The [`tasks.json` configuration file](#tasks-metadata)[^json] for a hub is used to structure the modeling tasks so that model submissions can be rapidly validated.
Modeling tasks are defined for single or multiple rounds[^multiround].
The three components of modeling tasks are:

 - The [`task_ids`{.codeitem} object](#task-id-vars) defines both labels for columns in submission files and the set of valid values for each column.
   Any unique value combination defines a single modeling task or target. 
 - The [`output_type`{.codeitem} object](#output-types) defines accepted representations _for each task_.
   The [model output section](#formats-of-model-output) provides more information on the different output types.
 - The [`target_metadata`{.codeitem} array](#target-metadata) provides additional information about each target.

[^json]: Due to technical issues, we do not currently support [json references](http://niem.github.io/json/reference/json-schema/references/) or yaml metadata files.

[^multiround]: For multiple rounds to share the same tasks without duplicating the `model_tasks` block, `round_id_from_variable` can be set to `true`, and the `round_id` should be a column defined in the `task_ids`. See the [`tasks.json` schema](#tasks-metadata) for details.


(task-id-vars)=
## Task ID variables
Hubs typically specify that modeling outputs (e.g., forecasts or projections) should be generated for each combination of values across a set of task ID variables.
Because they are central to Hubs, task ID variables serve several purposes:

* **Define modeling tasks** of the hub in the hub metadata
* **Identify modelling tasks corresponding to forecasts** in the model outputs
* **Allow alignment of model outputs with [target data](#target-data)** that are derived from "ground truth" data sources. 

The following diagram illustrates the relationships between these items at a high level, and the following sections provide more detail.

```{figure} ../images/hub-data-relations2.jpeg
---
figclass: margin-caption
alt: A diagram showing that hub metadata are specified by the hub itself. Hubverse provides tools to validate submissions, and teams provide model output data that conforms to the standards specified in the hub metadata. Hubverse provides tools to build ensembles. Hubs provide time series and target observation data, and hubverse provides a function to calculate scores.
name: hub-data-relations
---
A modeling hub works as an ecosystem of resources from the hub administrators, modeling teams, and hubverse developers.
```

(task-id-use)=
### Usage of task ID variables

**Task ID variables represent columns in model output files.**
It's important to understand that model output files are in **tabular format (e.g., csv or parquet).**
Moreover, these tables are presented in a [long/narrow representation](https://en.wikipedia.org/wiki/Wide_and_narrow_data) where each row of data represents a unique combination of task ID variables and a single value from the model output[^tidy]. 

[^tidy]: This type of data is also known as "tidy data," a term coined by Hadley Wickham that's heavily used in the R community. You can read more about the concept in the [Data tidying chapter of the R4DS book](https://r4ds.hadley.nz/data-tidy#sec-tidy-data) and the [Tidy Data paper by Wickham (2014)](https://www.jstatsoft.org/article/view/v059i10).

In the `tasks.json` file, task ID variables are a collection of JSON objects
that define required and optional values for these variables. In the example below from [the COVID-19 variant nowcast hub](https://github.com/reichlab/variant-nowcast-hub/blob/main/hub-config/tasks.json), there are four task ID variables defined: `"nowcast_date"`, `"target_date"`, `"location"`, and `"clade"`. 

```json
"task_ids": {
    "nowcast_date": {
        "required": [
            "2024-09-11"
        ],
        "optional": null
    },
    "target_date": {
        "required": null,
        "optional": ["2024-08-11", "2024-08-12", "2024-08-13", "2024-08-14", "2024-08-15", "2024-08-16", "2024-08-17", "2024-08-18", "2024-08-19", "2024-08-20", "2024-08-21", "2024-08-22", "2024-08-23", "2024-08-24", "2024-08-25", "2024-08-26", "2024-08-27", "2024-08-28", "2024-08-29", "2024-08-30", "2024-08-31", "2024-09-01", "2024-09-02", "2024-09-03", "2024-09-04", "2024-09-05", "2024-09-06", "2024-09-07", "2024-09-08", "2024-09-09", "2024-09-10", "2024-09-11", "2024-09-12", "2024-09-13", "2024-09-14", "2024-09-15", "2024-09-16", "2024-09-17", "2024-09-18", "2024-09-19", "2024-09-20", "2024-09-21"]
    },
    "location": {
        "required": null,
        "optional": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"]
    },
    "clade": {
        "required": ["24A", "24B", "24C", "recombinant", "other"],
        "optional": null
    }
}
```

In this particular round, modelers MUST submit predictions with the
`"nowcast_date"` of 2024-09-11 with all of the `"clade"`s (24A, 24B, 24C,
recombinant, and other). Any submissions that contain anything other than those
exact values will result in an error. In contrast, modellers MAY submit
predictions for ANY of the `"target_date"`s between 2024-08-11 and 2024-09-21
and ANY of the states listed in `"location"`. By allowing modelers to submit a
subset of optional values, it means poor-performing models can be omitted so
they do not negatively influence model ensembles.

#### Special task ID variables

Task ID variables are used to parameterize modeling efforts. 
However, some task ID variables serve specific purposes in defining submission rounds and targets.
Every hub must have **a single task ID variable that uniquely defines a submission round.**
It has become a convention to use a task ID formatted in the `YYYY-MM-DD` format (e.g., `origin_date` or `forecast_date`). 
For example, in [Running Example 1](#running-examples), this task ID is `origin_date`.

There can be **one or more task ID variables to define a modeling "target"** (these are referred to in the [tasks metadata](#tasks-metadata) as a `target_key`).
For example, in our [Running Example 1](#running-example-1), the task ID variables are `target`, `location`, and `origin_date`.
In this example, `target` is the target key and can only take on one value, "inc covid hosp".


#### Proposed standard of task ID variables

We strongly suggest that Hubs adopt the following standard task ID or column names and definitions[^new-vars]:  

* `origin_date`{.codeitem}: the starting point that can be used for calculating a `target_date` via the formula `target_date = origin_date + horizon * time_units_per_horizon` (e.g., with weekly data, `target_date` is calculated as `origin_date + horizon * 7` days).
  Another reasonable choice for `origin_date` is `reference_date`.
* `forecast_date`{.codeitem}: usually defines the date a model is run to produce a forecast.
* `scenario_id`{.codeitem}: a unique identifier for a scenario
* `location`{.codeitem}: a unique identifier for a location
* `target`{.codeitem}: a unique identifier for the target.
  It is recommended, although not required, that hubs set up a single variable to define the target (i.e., as a target key), with additional detail specified in the [`target_metadata` array](#target-metadata).
* `target_variable`{.codeitem}/`target_outcome`: task IDs making up unique identifiers of a two-part target.
  These tasks can be used in hubs that want to divide the definition of a target across two variables.
  Both task IDs will be specified as target keys in the [`target_metadata` array](#tasks-metadata).
* `target_date`{.codeitem}/`target_end_date`: for short-term forecasts, one of the synonymous task IDs `target_date`/`target_end_date` specifies the date of occurrence of the outcome of interest.
  For instance, if models are requested to forecast the number of hospitalizations on 2022-07-15, the `target_date` is 2022-07-15.
* `horizon`{.codeitem}: The difference between the `target_date` and the `origin_date` in time units specified by the hub (e.g., days, weeks, or months)
* `age_group`{.codeitem}: a unique identifier for an age group

While there are no general restrictions on task ID column names or definitions, using the above standards ensures that these task IDs are strongly validated against the schema.

[^new-vars]: As Hubs define new modeling tasks, they may need to introduce new task ID variables that have not been used before.
In those cases, the new variables should be added to this list to ensure that the concepts are documented centrally and can be reused in future efforts.

(output-types)=
## Output types

The `output_type` object defines accepted model output representations for each task. These define what kind of model output is expected, what range of values
we expect, if multiple values are expected, what identifies that value, and
whether or not the output type is required for submission.

To illustrate how output types are represented in `tasks.json`, here is an
example of a quantile output type:

```{code-block} json
:lineno-start: 1
:force: true
:lineno-start: 1
"quantile": {
    "output_type_id": {
        "required": [
            0.01,
            0.5,
            0.99,
        ]
    },
    "value": {
        "type": "integer",
        "minimum": 0
    },
    "is_required": true
}
```

From the code block above, you can see that an output type has four components:

1. (line 1) `"quantile"`{.codeitem} the name of the output type representation
   (e.g. `"mean"`, `"quantile"`, `"pmf"`) 
2. (line 2) `"output_type_id"`{.codeitem} In the case of quantiles, the output
   type ID is an indcation of the quantile bins. **Unlike task IDs, all
   `output_type_id`s are required** (see note below).
3. (line 9) `"value"`{.codeitem} the expected value type and range. In this
   case, the values from this model should be non-negative integers.
4. (line 13) `"is_required"`{.codeitem} an indication if this output type is
   required or not. In this example, submissions without this output type would
   fail. 

The [formats of model output section](#output-type-table) from the model output chapter provides more information on the different output types.

:::{note}

In version 4 of the schemas, we have officially disallowed optional output type
IDs. The reason behind this logic is that, unlike task IDs, missing output type
IDs have consequences for downstream model scoring and ensembling.

Specifically, these two scenarios are possible if a complete set of quantile
bins are not included:

1. When teams submit different subsets of quantiles and we use a score like WIS
   to evaluate the model, the scores are different and not comparable when
   computed on different quantiles. So any end-user would have to take some
   care to ensure that they are making a comparison on just a subset of
   required quantiles.
2. When building ensembles, if you just collected all quantile forecasts
   without ensuring that you had a complete set of all quantiles from all
   forecasters, you might combine quantiles from one subset of forecasters for
   some quantiles and have a different combination of forecasters for other
   quantiles.

:::



(target-metadata)=
## Target metadata

Target metadata is an array in the [`tasks.json` schema file](#tasks-metadata) that defines each target's characteristics. 
It serves as a logical connection between `task_ids` and corresponding `output_types`:

```{mermaid}
flowchart LR
    subgraph task-id["task_ids"]
    target
    end
    
    subgraph output-type["output_type"]
    vars["[output type objects]"]
    end

    subgraph target-metadata["target_metadata"]
    subgraph tk["target_keys"]
    tktarget["target"]
    end
    target-type["target_type"]
    end

    tktarget -->|"matches"| target
    target-type -->|"corresponds to"| vars
```

### Example

Here is an example of how the target metadata fields might appear in the `tasks.json` schema for a Hub whose target is incident COVID-19 hospitalizations. 

```json
"target_metadata": [
    {
        "target_id": "inc covid hosp",
        "target_name": "Daily incident COVID hospitalizations",
        "target_units": "count",
        "target_keys": {
            "target": "inc covid hosp"
        },
        "description": "Daily newly reported hospitalizations where the patient has COVID, as reported by hospital facilities and aggregated in the HHS Protect data collection system.",
        "target_type": "discrete",
        "is_step_ahead": true,
        "time_unit": "day"
    }
]
```

### Details

Target metadata comprises the following fields:
* `target_id`{.codeitem}: a short description uniquely identifying the target.
* `target_name`{.codeitem}: a longer, human-readable description of the target, which could be used as a visualization axis label.
* `target_units`{.codeitem}: the unit of observation used for this target. 
* `target_keys`{.codeitem}: a set of one or more name/value pairs that **must match a target defined in the `task_ids`** section of the schema.
Each value, or the combination of values if multiple keys are specified, defines a single target value.
* `description`{.codeitem}: a verbose explanation of the target, which might include details on the measure used for the target or a definition of 'rate', for example. 
* `target_type`{.codeitem}: the target’s statistical data type that **must correspond to the `output_type`** section of the schema.
   
   The following table lists the possible values for `target_type` (rows) and the corresponding `output_type` (columns).
   An `X` indicates that the output type can be used with the target type, and a `-` means that it can not be used. 
   We note that for the binary data type row, mean and median `output_type` are X'ed for definitional consistency, but in practice, the hubverse recommends using pmf or sample `output_type` as a more natural way to represent these values.

   | `target_type` | mean | median | quantile | cdf   | pmf   | sample 
   |--------- | ----------- |----------- | ----------- |----------- |----------- |----------- |
   | continous | X | X | X | X | - | X |
   | discrete | X | X | X | X | X | X |
   | nominal | - | - | - | - | X | X |
   | binary | X | X | - | - | X | X |
   | date | X | X | X | X | X | X |
   | ordinal | - | X | X | X | X | X |
   | compositional | X | X | - | - | - | X |

* `is_step_ahead`{.codeitem}: a Boolean value that indicates whether the target is part of a sequence of values, defined by `time_unit`.
* `time_unit`{.codeitem}: When `is_step_ahead` is `true`, this field should be one of `"day"`, `"week"`, or `"month"`, defining the unit of time steps.
  This field will be ignored when `is_step_ahead` is `false`.


