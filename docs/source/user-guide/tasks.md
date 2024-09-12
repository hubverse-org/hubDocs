# Defining modeling tasks

Every Hub is organized around "modeling tasks" that define how the target data should be modelled in terms of 

1. what factors to use for modelling (e.g. date, location, variant, etc) and 
2. the specific format of the model output.

The [tasks.json configuration file](#tasks-metadata)[^json] for a hub is used to structure the modelling tasks so that model submissions can be rapidly validated.
Modeling tasks are defined for single or multiple rounds[^multiround].
The three components of modeling tasks are:

 - The [`task_ids`{.codeitem} object](#task-id-vars) defines both labels for columns in submission files and the set of valid values for each column.
   Any unique combination of the values define a single modeling task, or target. 
 - The [`output_type`{.codeitem} object](#output-types) defines accepted representations _for each task_.
   More on the different output types can be found in [The Model Output Chapter](model-output.md#formats-of-model-output).
 - The [`target_metadata`{.codeitem} array](#target-metadata) provides additional information about each target.

[^json]: Due to technical issues, we do not currently support json references or yaml metadata files.

[^multiround]: For multiple rounds to share the same tasks without duplicating the `model_tasks` block, `round_id_from_variable` can be set to `true` and the `round_id` should be a column defined in the `task_ids`. See [the `tasks.json` schema](hub-config.md#hub-model-task-configuration-tasks-json-file) for details.


(task-id-vars)=
## Task ID variables
Hubs typically specify that modeling outputs (e.g. forecasts or projections) should be generated for each combination of values across a set of task ID variables.<!-- 2024-09-01
Zhian: I am not sure if this 52-word sentence below adds anything.
It appears to be saying that model outputs can be evaluated for accuracy using truth data, which is also stated below.
For modeling exercises where the model outputs correspond to estimates or predictions of a quantity that could in principle be calculated from observable data, these task ID variables should be sufficient to uniquely identify an observed value for the modeling target that could be compared to model outputs to evaluate model accuracy.
This is discussed more in the section on [target (a.k.a. truth) data](#target-data).
-->
Because they are central to Hubs, task ID variables serve several purposes:

* **Define modelling tasks** of the hub in the hub metadata
* **Identify modelling tasks corresponding to forecasts** in the model outputs
* **Allow alignment of model outputs with truth data** by specifying [target data](#target-data) that can help define methods to calculate outputs from "ground truth" data sources. 

The relationships between these items are illustrated at a high level in the following diagram; sections to follow provide more detail.

```{figure} ../images/hub-data-relations2.jpeg
---
figclass: margin-caption
alt: A diagram showing that hub metadata are specified by the hub itself. Hubverse provides tools to validate submissions and teams provide model output data that conforms to the standards specified in the hub metadata. Hubverse provides tools to build ensembles. Hubs provide time series data and target observation data, and hubverse provides a function to calculate scores.
name: hub-data-relations
---
A modelling hub works as an ecosystem of resources from the hub administrators, modelling teams, and hubverse developers
```

(task-id-use)=
### Usage of task ID variables

**Task ID variables represent columns in model output files.**
It's important to understand that model output files are in **tabular format (e.g. csv or parquet).**
Moreover, these tables are presented in a [long/narrow representation](https://en.wikipedia.org/wiki/Wide_and_narrow_data) where each row of data represents a unique combination of task ID variables and a single value from the model output[^tidy]. 

[^tidy]: This type of data is also known as "tidy data," which is a term coined by Hadley Wickham that's heavily used in the R community. You can read more about the concept in the [Data Tidying Chapter of the R4DS book](https://r4ds.hadley.nz/data-tidy#sec-tidy-data) and [the Tidy Data paper by Wickham (2014)](https://www.jstatsoft.org/article/view/v059i10).

#### Special Task ID variables

Task ID variables are used to parameterize modelling efforts. 
However, some task ID variables serve specific purposes to define submission rounds and targets.
Every hub must have **a single task ID variable that uniquely defines a submission round.**
It has become a convention to use a task ID like `origin_date` or `forecast_date` for this purpose, although this is not a specific restriction.
For example, in [Running Example 1](#running-examples), this task ID is `origin_date`.

There can be **one or more task ID variables to define a modelling "target"** (these are referred to in the [tasks metadata](#tasks-metadata) as a `target_key`).
For example, in our [Running Example 1](#running-example-1), the task ID variables are `target`, `location`, and `origin_date`.
In this example, `target` is the target key and can only take on one value "inc covid hosp".
In other examples, (such as [Running Example 3](#running-example-3)) more than one variable can serve as target keys together.
In example 3, both `outcome_variable` and `outcome_measure` make up the target keys.  



#### Proposed standard of Task ID variables

In general, there are no restrictions on what task ID variables may be named, however when appropriate, we suggest that Hubs adopt the following standard task ID or column names and definitions[^new-vars]:  

* `origin_date`{.codeitem}: the starting point that can be used for calculating a `target_date` via the formula `target_date = origin_date + horizon * time_units_per_horizon` (e.g., with weekly data, `target_date` is calculated as `origin_date + horizon * 7` days).
  Another reasonable choice for `origin_date` is `reference_date`.
* `forecast_date`{.codeitem}: usually defines the date that a model is run to produce a forecast.
* `scenario_id`{.codeitem}: a unique identifier for a scenario
* `location`{.codeitem}: a unique identifier for a location
* `target`{.codeitem}: a unique identifier for the target.
  It is recommended, although not required, that hubs set up a single variable to define the target (i.e., as a target key), with additional detail specified in [the `target_metadata` array](#target-metadata).
* `target_variable`{.codeitem}/`target_outcome`: task IDs making up unique identifiers of a two-part target.
  These task can be used in hubs that want to split up the definition of a target across two variables.
  In this situation, both task IDs will be specified as target keys in [the `target_metadata` array](#tasks-metadata).
* `target_date`{.codeitem}/`target_end_date`: for short-term forecasts, the synonymous task IDs `target_date`/`target_end_date` specify the date of occurrence of the outcome of interest.
  For instance, if models are requested to forecast the number of hospitalizations that will occur on 2022-07-15, the `target_date` is 2022-07-15.
* `horizon`{.codeitem}: The difference between the `target_date` and the `origin_date` in time units specified by the hub (e.g., may be days, weeks, or months)
* `age_group`{.codeitem}: a unique identifier for an age group

[^new-vars]: As Hubs define new modeling tasks, they may need to introduce new task ID variables that have not been used before.
In those cases, the new variables should be added to this list to ensure that the concepts are documented in a central place and can be reused in future efforts.

(output-types)=
## Output types

The `output_type` object defines accepted representations for each task.
More on the different output types can be found in the [formats of model output section](#output-type-table) from the model output chapter.

(target-metadata)=
## Target metadata

Target metadata is an array in the [tasks.json](#tasks-metadata) schema file that defines the characteristics of each target. 
This serves as a logical connection between `task_ids` and corresponding `output_types`:

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
Here is an example of how the target metadata fields might appear in the `tasks.json` schema for a Hub whose target is incident covid hospitalizations. 

```
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

It is composed of the following fields:
* `target_id`{.codeitem}: a short description that uniquely identifies the target.
* `target_name`{.codeitem}: a longer, human readable description of the target, which could be used as a visualization axis label.
* `target_units`{.codeitem}: the unit of observation used for this target. 
* `target_keys`{.codeitem}: a set of one or more name/value pairs that **must match a target defined in the `task_ids`** section of the schema.
Each value, or the combination of values if multiple keys are specified, defines a single target value.
* `description`{.codeitem}: a verbose explanation of the target, which might include details on the measure used for the target or a definition of 'rate', for example. 
* `target_type`{.codeitem}: the target’s statistical data type that **must correspond to the `output_type`** section of the schema.
   
   The following table lists the possible values for `target_type` (rows) and the corresponding `output_type` (columns).
   An `X` indicates that the output type can be used with the target type and a `-` means that it can not be used. 
   We note that for the binary data type row, mean and median `output_type` are X'ed for definitional consistency, but in practice the hubverse recommends using pmf or sample `output_type` as a more natural way to represent these values.

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
  When `is_step_ahead` is `false`, this field will be ignored.


