# Sample output type

## Introduction

The sample `output_type` can represent a probabilistic distribution through a collection of possible future observed values ("samples") that originate from a predictive model. Depending on the model's setup and the hub's configuration settings, different information may be requested or required to identify each sample.

In the hubverse, a "[modeling task](tasks.md)" is defined by a unique combination of task ID column values. You can think of each modeling task as a specific part of the space defined by the [task ID variables](#task-id-vars)[^1] that we are interested in predicting. Each modeling task results in a single prediction. (Note that this concept is similar to that of a ["forecast unit" in the scoringutils R package](https://epiforecasts.io/scoringutils/reference/set_forecast_unit.html).)

[^1]: (AKA task IDs, task ID columns) Column(s) in model output that provide details about what is being predicted. Common examples include `target`, `location`, `reference_date`, and `horizon`. These "task ID" columns may also include additional information, such as any conditions or assumptions used to generate the predictions.

We will use the following `model_output` data to help solidify the concept of a modeling task. (The mean `output_type` is used for demonstration purposes due to its simplicity.)

| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 |  1 | MA | mean | NA| - |
| 2024-03-15 |  2 | MA | mean | NA| - |
| 2024-03-15 |  3 | MA | mean | NA| - |

In this table, the task ID columns are `origin_date`, `horizon`, and `location`. There are three modeling tasks (one per row): horizon 1, horizon 2, and horizon 3—all for Massachusetts and origin date 2024-03-15. The first row, for example, represents a single slice of task ID space, a prediction for one week ahead in Massachusetts, resulting in one predicted value.

## Sampling modeling tasks

While the mean output type produces a single predicted value per modeling task, the sample output type captures uncertainty by providing multiple possible values for each task. Each sample represents one possible outcome, and together, the collection of samples describes a distribution of predicted values.

How modeling tasks relate to each other determines the structure of this distribution. When modeling tasks are treated independently, samples for each task form a univariate (single-variable) distribution. When modeling tasks are grouped together, samples capture a multivariate (joint) distribution across the group of tasks.

## Marginal distributions

In many settings, predictions will be made for individual modeling tasks, with no notion of modeling tasks being related to each other or collected into sets (for more on this, see the [compound modeling tasks section](#compound-modeling-tasks)). When predictions are assumed to be made for individual modeling tasks, every modeling task is treated as distinct. In mathematical terms, these samples represent draws from marginal predictive distributions.

Now, suppose we wanted to collect samples for each of the modeling tasks defined in the previous section. The table below shows a dataset with three groups (indicated by `compound_idx`[^2] values 1, 2, and 3) and three samples per group. In this case, the only difference between the modeling tasks here are the horizon. The [`output_type_id` column](#column-details)[^3] contains sample indices that are unique across an entire model output file, not just within each group, so each group has distinct indices (1-3, 4-6, and 7-9 respectively). When sampling from marginal distributions, each group corresponds to a single modeling task, so all task ID values are identical within each group. Notice how each group represents samples for a single modeling task.

[^2]: The `compound_idx` column indicates which rows belong to the same group. In the marginal case shown here, each group contains samples for one modeling task. This column is not a task ID variable and is not typically present in actual model output data. Validation works this column out from the config (see [validating samples](#sample-validation)).

[^3]: A column in model output that specifies identifying information specific to the output type. For samples, an integer or string providing a unique identifier for the sample (see [allowed sample IDs](#sample-output-type-ids)). This is important for samples originating from a joint distribution, so that rows that have the same `output_type_id` are presumed to represent a single sample from a joint distribution. Examples are given later in the text.

|compound_idx| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | 1 | MA | sample | 1| - |
| 1 | 2024-03-15 | 1 | MA | sample | 2| - |
| 1 | 2024-03-15 | 1 | MA | sample | 3| - |
| 2 | 2024-03-15 | 2 | MA | sample | 4| - |
| 2 | 2024-03-15 | 2 | MA | sample | 5| - |
| 2 | 2024-03-15 | 2 | MA | sample | 6| - |
| 3 | 2024-03-15 | 3 | MA | sample | 7| - |
| 3 | 2024-03-15 | 3 | MA | sample | 8| - |
| 3 | 2024-03-15 | 3 | MA | sample | 9| - |

In this type of setting, a hub will specify a minimum and maximum number of required samples per group in the configuration for the prediction task. When samples originate from marginal distributions, each group corresponds to a single modeling task, but as we will see in the [compound modeling tasks section](#compound-modeling-tasks), a group can span multiple modeling tasks. The associated configuration might look like the following:

```{code-block} json
"output_type": {
    "sample": {
        "output_type_id_params": {
            "type": "integer",
            "min_samples_per_task": 3,
            "max_samples_per_task": 3
        },
        "value": {
            "type":"double",
            "minimum": 0
        },
        "is_required": true
    }
}
```

More specifically, the `"output_type_id_params"` property specifies that sample `output_type_id`s must be [integer sample IDs](#sample-output-type-ids), and there must be exactly (i.e., no more or less than) 3 samples per modeling task (group). The `"value"` specification refers to the predicted values contained in the "value" column (e.g., they must be storable as numeric "double" format and be no less than zero). The `"is_required"` property specifies that samples are a required output type.

Note that samples use an `"output_type_id_params"` block to define allowable values through parameters (like min/max). Other output types use an `"output_type_id"` block that lists required and optional values explicitly. One example for the mean output type is shown below; more information and examples can be found on the [Hub configuration files page](#tasks-metadata) in the `tasks.json` file section.

```{code-block} json
    "mean": {
        "output_type_id": {
            "required": null
        },
        "value": {
            "type": "double",
            "minimum": 0
        },
        "is_required": true
    }
```

(sample-output-type-ids)=
### Allowed sample IDs

The `"type"` property of `"output_type_id_params"` sets which values the `output_type_id` column may hold for samples. Every sample row must have a non-empty `output_type_id`.

`"integer"`
: Each sample ID is a non-negative integer, written with digits only and without leading zeros, such as `"0"` or `"12"`. Values such as `"s1"`, `"1.5"`, `"1.0"`, `"01"` and `"-1"` fail validation.

`"character"`
: Each sample ID has at most `"max_length"` characters. It may contain only ASCII letters, digits, underscores (`_`), hyphens (`-`) and periods (`.`), such as `"s1"` or `"3fa9c2e12_001"`. The second example combines a hash of the `model_id` and round ID (`3fa9c2e1`), the modeling task index (`2`) and the sample index within the modeling task (`001`), so that IDs from different models and rounds do not collide. A hub using IDs like this needs a `"max_length"` of at least 13.

A submission with a sample ID that breaks these rules fails validation, and the other sample checks do not run.

(sample-output-type-id-scope)=
### Scope of sample IDs

A sample ID identifies one draw from a model's predictive distribution. Rows that share a sample ID belong to the same draw, so they are sampled jointly.

Sample IDs are scoped to one model output file, which holds the predictions of one model for one round. Validation checks sample IDs within that file only, so two files can use the same sample IDs.

```{important}
In model output combined across models or rounds, the same sample ID can refer to unrelated draws. To separate draws, group rows by `model_id`, round ID and `output_type_id` together.
```

A hub that wants sample IDs to be distinct across all of its model output can use character IDs that encode the model and the round, such as the `"3fa9c2e12_001"` example above. Validation does not check that such IDs are distinct across files.

```{admonition} Reusing sample IDs across compound modeling tasks
:class: caution

To ensure samples are properly interpreted, independently drawn samples need their own unique sample IDs within a submission, even when they are for different [compound modeling tasks](#compound-modeling-tasks). For example, in a hub whose `compound_taskid_set` includes `location`, a model may sample each location in a separate run. If the numbering restarts at each location, so that every location has samples `1` to `100`, each sample ID appears in every location's rows. Hubverse tools then interpret those samples as joint across locations. Validation cannot catch this error, because [coarser samples](#sample-validation) (i.e., samples joint across additional task IDs) are valid.
```

(compound-modeling-tasks)=
## Compound modeling tasks

In the previous section, we saw that when sampling from marginal distributions, each sample is drawn from a single modeling task. In some settings, however, modeling hubs may wish to capture relationships between modeling tasks by sampling from a joint distribution. This means drawing values for multiple modeling tasks at once as a coherent set.

Consider three common scenarios:
- **Trajectories over time**: A model might predict values across multiple time horizons as a coherent path. Rather than drawing each horizon's prediction independently, the model draws an entire trajectory, a sample from a joint distribution over horizons.
- **Trajectories over locations**: A model making predictions for multiple locations might draw the trajectories together (or perhaps even draw trajectories across both time and space), resulting in a sample from a joint distribution over locations.
- **Variant proportions**: A model predicting proportions of multiple disease variants might draw all variant proportions together, a sample from a joint distribution across variants.

In all cases, joint sampling introduces additional dimensions to the predictive distribution. Instead of a univariate distribution at each modeling task, we have a multivariate distribution spanning multiple modeling tasks. We refer to this as **response dependence** across the task IDs that vary within a group, because the predicted values (responses) for different modeling tasks are statistically dependent.

Within a group of jointly sampled modeling tasks, some task ID values remain constant (defining which group we're in), while others vary (defining the multiple modeling tasks covered by the joint distribution). The `"compound_taskid_set"` specifies which task IDs remain constant within a group. Task IDs not in this set vary within the group and are sampled jointly, introducing response dependence across those task IDs. A **compound modeling task** is thus a group of related predictions defined by the compound task ID set. In other words, any variables not included in the `"compound_taskid_set"` are assumed to be part of a multivariate outcome. At the limit, an empty compound task ID set (`[]`) holds no task ID constant, so every task ID varies within the group and all of them are sampled jointly.

Consider the following model output[^4] submission file from a hub reporting on **variant** proportions observed in **Massachusetts** (`location`) on **2024-03-15** (`origin_date`) for **1 and 2 week predictions** (`horizon`). There are four variants (`AA`, `BB`, `CC`, and `DD`) represented over two horizons, with two sample predictions for each of the eight combinations; this results in a total of 16 rows of sample output type predictions.

| origin_date | horizon | variant |location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | 1 | AA | MA | sample | - | - |
| 2024-03-15 | 1 | AA | MA | sample | - | - |
| 2024-03-15 | 1 | BB | MA | sample | - | - |
| 2024-03-15 | 1 | BB | MA | sample | - | - |
| 2024-03-15 | 1 | CC | MA | sample | - | - |
| 2024-03-15 | 1 | CC | MA | sample | - | - |
| 2024-03-15 | 1 | DD | MA | sample | - | - |
| 2024-03-15 | 1 | DD | MA | sample | - | - |
| 2024-03-15 | 2 | AA | MA | sample | - | - |
| 2024-03-15 | 2 | AA | MA | sample | - | - |
| 2024-03-15 | 2 | BB | MA | sample | - | - |
| 2024-03-15 | 2 | BB | MA | sample | - | - |
| 2024-03-15 | 2 | CC | MA | sample | - | - |
| 2024-03-15 | 2 | CC | MA | sample | - | - |
| 2024-03-15 | 2 | DD | MA | sample | - | - |
| 2024-03-15 | 2 | DD | MA | sample | - | - |

[^4]: In model output files, an entry of "-" stands in for specific values to be provided by the submitter. They are not assumed to be identical.

Notice that this example submission file could be displaying predictions with any number of response dependence structures (or none at all) since we are not given the `output_type_id` values or `compound_taskid_set`. The following subsection provides five possible combinations of compound modeling tasks that this model output data may be representing. Different samples are distinguished from each other by using light and dark gray to highlight adjacent samples.

### Examples of different `compound_taskid_set` configurations

#### Example A: No response dependence across task IDs
***Each group = one modeling task***

This is equivalent to the marginal distributions case described earlier, included here for comparison. Each group contains a single modeling task, with no response dependence across any task IDs.

<div class="heatMap1">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s2 | - |
| 2 | 2024-03-15 | MA | 1 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 1 | BB | sample | s4 | - |
| 3 | 2024-03-15 | MA | 1 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 1 | CC | sample | s6 | - |
| 4 | 2024-03-15 | MA | 1 | DD | sample | s7 | - |
| 4 | 2024-03-15 | MA | 1 | DD | sample | s8 | - |
| 5 | 2024-03-15 | MA | 2 | AA | sample | s9 | - |
| 5 | 2024-03-15 | MA | 2 | AA | sample | s10 | - |
| 6 | 2024-03-15 | MA | 2 | BB | sample | s11 | - |
| 6 | 2024-03-15 | MA | 2 | BB | sample | s12 | - |
| 7 | 2024-03-15 | MA | 2 | CC | sample | s13 | - |
| 7 | 2024-03-15 | MA | 2 | CC | sample | s14 | - |
| 8 | 2024-03-15 | MA | 2 | DD | sample | s15 | - |
| 8 | 2024-03-15 | MA | 2 | DD | sample | s16 | - |

</div>

```{attention}
Rows with the same `compound_idx` value indicate distinct sample predictions made for the same group. When samples originate from marginal distributions, each group contains a single modeling task. For example, each pair of rows with the same `compound_idx` correspond to the same modeling task, but are each from one of sixteen distinct sample draws "s#" (e.g., "s1" and "s2" are two distinct sample draws for {origin_date: "2024-03-15", horizon: "1", location: "MA", variant: "AA"}).
```

The table above shows eight unique modeling tasks, with two sample predictions for each. A unique combination of `origin_date`, `location`, `horizon`, and `variant` defines each modeling task.

To configure this dependence structure, all task IDs are included in the `compound_taskid_set`:

```{code-block} json
:lineno-start: 1
:emphasize-lines: 6
"output_type_id_params": {
    "type": "character",
    "max_length": 6,
    "min_samples_per_task": 2,
    "max_samples_per_task": 2,
    "compound_taskid_set": ["origin_date", "location", "horizon", "variant"]
}
```

#### Example B: Response dependence across variants
***Joint distribution across variants***

This is the first example of a true compound modeling task, where each group contains multiple modeling tasks sampled jointly. Here, **the proportions of all four variants at a given date, location, and horizon are sampled together** from a joint distribution, with response dependence across `variant` only.

<div class="heatMap2">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | CC | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | DD | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | CC | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | DD | sample | s2 | - |
| 2 | 2024-03-15 | MA | 2 | AA | sample | s3 | - |
| 2 | 2024-03-15 | MA | 2 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 2 | CC | sample | s3 | - |
| 2 | 2024-03-15 | MA | 2 | DD | sample | s3 | - |
| 2 | 2024-03-15 | MA | 2 | AA | sample | s4 | - |
| 2 | 2024-03-15 | MA | 2 | BB | sample | s4 | - |
| 2 | 2024-03-15 | MA | 2 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 2 | DD | sample | s4 | - |

</div>

```{attention}
Rows are grouped so dependent samples for each modeling task are together. The first four rows correspond to the first sample ("s1") for the first compound modeling task (`compound_idx` = 1), covering all four variants. The second four rows correspond to the second sample ("s2") for the same compound modeling task.
```

The table above shows two unique compound modeling tasks (shown with the `compound_idx` column), with two independent sample draws for each, identified by `output_type_id` (s1, s2, s3, s4, making a total of four sample predictions). Each compound modeling task is defined by a fixed combination of `origin_date`, `horizon`, and `location` values, while the values of `variant` vary.

To configure this dependence structure, `variant` is excluded from the `compound_taskid_set`:

```{code-block} json
:lineno-start: 1
:emphasize-lines: 6
"output_type_id_params": {
    "type": "character",
    "max_length": 6,
    "min_samples_per_task": 2,
    "max_samples_per_task": 2,
    "compound_taskid_set": ["origin_date", "location", "horizon"]
}
```

#### Example C: Response dependence across horizons
***Trajectories over time***

Here, `horizon` is the only variable with response dependence. This could be described as **"trajectories of variant proportions over time in Massachusetts, with each variant treated independently from each other."**

<div class="heatMap4">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s2 | - |
| 2 | 2024-03-15 | MA | 1 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 2 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 1 | BB | sample | s4 | - |
| 2 | 2024-03-15 | MA | 2 | BB | sample | s4 | - |
| 3 | 2024-03-15 | MA | 1 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 2 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 1 | CC | sample | s6 | - |
| 3 | 2024-03-15 | MA | 2 | CC | sample | s6 | - |
| 4 | 2024-03-15 | MA | 1 | DD | sample | s7 | - |
| 4 | 2024-03-15 | MA | 2 | DD | sample | s7 | - |
| 4 | 2024-03-15 | MA | 1 | DD | sample | s8 | - |
| 4 | 2024-03-15 | MA | 2 | DD | sample | s8 | - |

</div>

The table above shows four unique compound modeling tasks (shown with the `compound_idx` column) and two independent sample draws for each, identified by `output_type_id` (s1-s8, making a total of eight sample predictions). Each compound modeling task is defined by a fixed combination of `origin_date`, `location`, and `variant` values, while `horizon` varies.

To configure this dependence structure, `horizon` is excluded from the `compound_taskid_set`:

```{code-block} json
:lineno-start: 1
:emphasize-lines: 6
"output_type_id_params": {
    "type": "character",
    "max_length": 6,
    "min_samples_per_task": 2,
    "max_samples_per_task": 2,
    "compound_taskid_set": ["origin_date", "location", "variant"]
}
```

(sample-example-d)=
#### Example D: Response dependence across horizons and variants
***Joint distribution across both horizons and variants***

Here, there is response dependence across both the `horizon` and `variant` variables. Each sample represents a grouped collection of possible values for all four variants across both prediction horizons.

<div class="heatMap3">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | CC | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | DD | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | CC | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | DD | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | CC | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | DD | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | CC | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | DD | sample | s2 | - |

</div>

The table above shows one unique compound modeling task (shown with the `compound_idx` column value) and two unique sample draws, identified by `output_type_id` (s1 and s2). This single compound modeling task can be described as predictions for **"Massachusetts with the `origin_date` of `2024-03-15`"**, with a fixed combination of `origin_date` and `location` values, while both `horizon` and `variant` vary.

To configure this dependence structure, both `horizon` and `variant` are excluded from the `compound_taskid_set`:

```{code-block} json
:lineno-start: 1
:emphasize-lines: 6
"output_type_id_params": {
    "type": "character",
    "max_length": 6,
    "min_samples_per_task": 2,
    "max_samples_per_task": 2,
    "compound_taskid_set": ["origin_date", "location"]
}
```

#### Example E: Response dependence across all task IDs
***Joint distribution across every task ID***

This is the limiting case of Example D. No task ID is held constant, so every task ID varies within a group and all of them are sampled jointly. Only a hub whose rounds are not identified by a task ID can declare an empty set (see [the round ID variable](#compound-taskid-set-round-id)). In this example, `origin_date` is therefore an ordinary task ID, and each round's round ID comes from its `round_id`.

The submission file is the one shown in [Example D](#sample-example-d). It reports on a single `origin_date` and a single `location`, so holding those two task IDs constant and holding none constant describe the same file. The two configurations diverge when a submission covers more than one location. Under Example D, a sample draw may cover one location or several. Under Example E, every sample draw must cover every location in the submission.

To configure this dependence structure, no task IDs are included in the `compound_taskid_set`:

```{code-block} json
:lineno-start: 1
:emphasize-lines: 6
"output_type_id_params": {
    "type": "character",
    "max_length": 6,
    "min_samples_per_task": 2,
    "max_samples_per_task": 2,
    "compound_taskid_set": []
}
```

### Configuration of `compound_taskid_set`

Different models may generate samples for different compound modeling tasks. For example, some might simulate data from all horizons sequentially, making predictions that consider what has happened at past horizons. Such a model would create output data like that of Examples C and D in the previous subsection, which have response dependence across horizons. Other models might only simulate draws from each horizon independently from other time points; these models would have output data similar to that of Examples A or B, which have no response dependence across horizons.

A hub should specify a `compound_taskid_set` field in the configuration for the sample `output_type` to indicate the task ID columns that define separate sample index values in the `output_type_id` column. **The `output_type_id` column allows a modeler to show which rows of model output belong to the same sample.** The field is optional, and when it is omitted it defaults to all task ID variables, the configuration of Example A.

```{warning}
Omitting `compound_taskid_set` and setting it to `[]` have opposite effects.

| `"compound_taskid_set"` | resolves to | meaning |
|:--- |:--- |:--- |
| omitted | all task IDs | each modeling task is its own compound modeling task (Example A); submissions with joint samples also pass |
| `[]` | no task IDs | every sample must be joint across every task ID (Example E) |

To configure a hub where samples are not required to be joint across any task ID, omit the field. Setting it to `[]` does the opposite: a submission passes only if every sample is joint across every task ID, so most submissions fail. In a hub whose rounds are not identified by a task ID, `validate_config()` accepts an empty set, so the mistake only shows when submissions start failing validation.
```

Sometimes, multiple `compound_taskid_set` specifications may be valid for a single model output file; in this case, it is important to indicate which one applies to the given submission file so that the contents are correctly interpreted. The following table[^5] shows how different specifications of the `compound_taskid_set` field would impact the validity of each example submission A, B, C, and D in the previous subsection.

<!-- accessible table derived from
https://www.w3.org/WAI/tutorials/tables/irregular/#table-with-two-tier-headers
-->
<table>
  <colgroup span="4"></colgroup>
  <tr>
    <td rowspan="1"></td>
    <th colspan="4" scope="colgroup"><strong>Example submission passing validation</strong></tj>
  </tr>
  <tr>
    <th scope="col"><strong><code>"compound_taskid_set"</code> in schema</strong></tj>
    <th scope="col"><strong>A (o_d,l,h,v)</strong></th>
    <th scope="col"><strong>B (o_d,l,h)</strong></th>
    <th scope="col"><strong>C (o_d,l,v)</strong></th>
    <th scope="col"><strong>D (o_d,l)</strong></th>
  </tr>
  <tr>
    <th scope="row"><code>["origin_date", "location", "horizon", "variant"]</code></th>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <th scope="row"><code>["origin_date", "location", "horizon"]</code></th>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
  </tr>
  <tr>
    <th scope="row"><code>["origin_date", "location", "variant"]</code></th>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <th scope="row"><code>["origin_date", "location"]</code></th>
    <td>❌</td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
  </tr>
  <tr>
    <th scope="row"><code>[]</code></th>
    <td>❌</td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
  </tr>
</table>

[^5]: The letters in parentheses shown in the column names indicate the actual composition of the compound task ID set in the examples from the previous subsection, where 1) o_d is origin_date, 2) l is location, 3) h is horizon, and 4) v is variant.

<br>

In general, a submission will pass validation if the task ID variables that define a compound modeling task (as implied by the sample ID values present in the `output_type_id` column) are also present in the `"compound_taskid_set"`. For the example of [`"origin_date"`, `"location"`, `"horizon"`] in the second row of the table above:
- Both Submissions B and D would pass validation since when the data are grouped by the `"compound_taskid_set"` variables you can always find a group of rows that have the same `output_type_id`.
- Submissions A and C would fail validation since when the data are grouped by the `"compound_taskid_set"` variables, there would be no rows that share an `output_type_id`.

Under Example A's `compound_taskid_set`, Submission A matches the set and Submissions B to D are [coarser](#sample-validation), so all four pass. Submission A is [finer](#sample-validation) than every other set in the table, so it fails under each of them.

```{caution}
[**Derived task IDs**](#derived-task-id-variables) are a type of task IDs whose values depend wholly on that of other task ID variables. A common example is the `target_end_date` task ID, which tends to be derived from the combination of the `reference_date` (or `origin_date`) and `horizon` task IDs.

These derived task IDs must be properly configured, or they can cause problems when validating compound modeling tasks by throwing errors when they should not. *If **all** the task ID variables a derived task ID is derived from are part of the `compound_taskid_set`, then that derived task ID must also be a part of the `compound_taskid_set`; otherwise, that derived task ID should be excluded.*

For example, if `reference_date` and `horizon` are both part of the `compound_taskid_set`, then the derived task ID `target_end_date` should be part of the `compound_taskid_set`. However, if, say, `horizon` displays response dependence and is thus not part of the `compound_taskid_set`, then `target_end_date` should also be excluded from the `compound_taskid_set`.
```

(compound-taskid-set-round-id)=
#### The round ID variable

When a round sets `round_id_from_variable` to `true`, every sample `compound_taskid_set` in that round must include the task ID named by `round_id` (see [`tasks.json` configuration](#tasks-metadata)). Each model output file covers a single round, so the round ID variable holds one value throughout the file. A sample therefore cannot be joint across it. Every set in Examples A to D includes `origin_date`, so they are valid whether or not `origin_date` identifies the rounds. Example E is valid only if it does not. An empty set is only valid when `round_id_from_variable` is `false`.

From hubAdmin 2.0.0, `validate_config()` reports an error for a set that leaves out the round ID variable, including an empty set. It also reports an error for a modeling task that does not have the round ID variable as a task ID. Omitting `compound_taskid_set` remains valid. Validating submissions against an empty set requires hubValidations 3.0.0 or later.

(sample-validation)=
### Validating samples

The examples in this section come from a hub that collects trajectories over horizons for three locations, `MA`, `CT` and `TX`. Its `compound_taskid_set` is `["origin_date", "location"]`, which leaves out `horizon`. Each sample is therefore a trajectory: it is joint across `horizon`. Each submission covers one `origin_date` and horizons 1 and 2, and may leave out any of the locations.

#### How validation splits samples

Validation matches each row of a submission to a compound modeling task by the row's values of the task IDs in `compound_taskid_set`. It then groups the rows by `output_type_id` and `compound_idx`.

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be", "fontSize": "18px"}}
flowchart LR
    set["<b>1. compound_taskid_set</b><br><br>origin_date, location"] --> idx["<b>2. compound_idx</b><br><br>one per unique combination of<br>origin_date and location<br>values in the config"]
    idx --> rows["<b>3. Match rows</b><br><br>each row gets the<br>compound_idx of its<br>origin_date and location"]
    rows --> slices["<b>4. Group rows</b><br><br>rows are grouped by<br>output_type_id and<br>compound_idx into slices"]
```

In step 2, validation numbers each combination of `origin_date` and `location` values that the config allows. In this hub, the config allows one `origin_date` and three locations, so there are three compound modeling tasks:

| origin_date | location | compound_idx |
|:---:|:---:|:---:|
| 2024-03-15 | MA | 1 |
| 2024-03-15 | CT | 2 |
| 2024-03-15 | TX | 3 |

In the simplest submission, each sample is a trajectory for one location. In step 3, validation uses the table above to assign each row a `compound_idx`, by matching the row's `origin_date` and `location` values. The table below shows the submission with that column added.

<table class="table spl-slices">
  <caption>Each solid box is one sample, and each dashed box inside it is one slice. Every second sample ID is in bold. The row colour shows the <code>compound_idx</code>.</caption>
  <thead>
    <tr>
      <th>origin_date</th>
      <th>location</th>
      <th>horizon</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
      <th>compound_idx (added)</th>
    </tr>
  </thead>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1 spl-last"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1 spl-last"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2 spl-first"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s3</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td>s3</td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2 spl-first"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td><strong>s4</strong></td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s4</strong></td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
</table>

In step 4, validation groups the rows by `output_type_id` and `compound_idx`. Each group is a **slice**. In this submission, all the rows of a sample are assigned the same `compound_idx`, so each sample is one slice.

#### Coarser samples pass

A team may instead sample `MA` and `CT` jointly. In the submission below, samples `"s1"` and `"s2"` are joint across `horizon` and `location`, with rows for `MA` and `CT`. They are joint across `location`, which is in `compound_taskid_set`, so they are **coarser**.

<table class="table spl-slices">
  <caption>Each solid box is one sample, and each dashed box inside it is one slice. Every second sample ID is in bold. The row colour shows the <code>compound_idx</code>.</caption>
  <thead>
    <tr>
      <th>origin_date</th>
      <th>location</th>
      <th>horizon</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
      <th>compound_idx</th>
    </tr>
  </thead>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
</table>

In step 3, the `MA` rows of sample `"s1"` are assigned `compound_idx` 1, and its `CT` rows are assigned `compound_idx` 2. In step 4, they are therefore grouped into two slices. Each slice of a coarser sample is a complete trajectory for one location, so the submission passes validation.

#### Samples are counted per compound modeling task

```{margin} Samples per compound_idx
<p class="spl-hist-title">First submission</p>
<div class="spl-hist">
  <div class="spl-hist-row"><span class="spl-hist-label">1 (MA)</span><span class="spl-hist-bar cidx-1" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">2 (CT)</span><span class="spl-hist-bar cidx-2" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
</div>

<p class="spl-hist-title">Coarser submission</p>
<div class="spl-hist">
  <div class="spl-hist-row"><span class="spl-hist-label">1 (MA)</span><span class="spl-hist-bar cidx-1" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">2 (CT)</span><span class="spl-hist-bar cidx-2" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
</div>
```

Validation counts samples per compound modeling task, not per sample ID. Each slice counts as one sample of its `compound_idx`.

The two submissions above count the same. The first submission has four samples, and each sample is one slice, so each `compound_idx` has two slices. The coarser submission has two samples, but each sample is grouped into two slices. It also has four slices, two in each `compound_idx`. Both submissions therefore have two samples per compound modeling task.

`"min_samples_per_task"` and `"max_samples_per_task"` apply to this count.

In short, samples are counted only against `compound_taskid_set`, regardless of their actual dependence structure.

#### Finer samples fail

In a hub collecting trajectories, each sample must be joint across `horizon`. A sample that is not joint across `horizon` is **finer**. A team that samples each horizon separately submits finer samples.

The submission below has the same rows as the first submission, but a new sample ID at each horizon. In the first submission, each sample has rows for horizons 1 and 2, a complete trajectory. Here, each sample has a row for one horizon only. No sample is a complete trajectory, so the submission fails validation.

<table class="table spl-slices">
  <caption>Each solid box is one sample, and every second sample ID is in bold. The row colour shows the <code>compound_idx</code>. Each dotted box marks the rows of one <code>compound_idx</code>.</caption>
  <thead>
    <tr>
      <th>origin_date</th>
      <th>location</th>
      <th>horizon</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
      <th>compound_idx</th>
    </tr>
  </thead>
  <tbody class="spl-unit">
    <tr class="cidx-1 spl-first spl-last"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1 spl-first spl-last"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1 spl-first spl-last"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s3</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1 spl-first spl-last"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td><strong>s4</strong></td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-gap"><tr><td colspan="7"></td></tr></tbody>
  <tbody class="spl-unit">
    <tr class="cidx-2 spl-first spl-last"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s5</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-first spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s6</strong></td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-first spl-last"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s7</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-first spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s8</strong></td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
</table>

So a coarser sample can be split into slices by `compound_idx`, and each slice is still a valid draw of one location's trajectory. Finer samples cannot be combined into trajectories. Horizons 1 and 2 were never drawn together, so the data does not record how they depend on each other.

#### Mixed dependence structures pass

A model may sample jointly across the locations within each region. In this hub, `MA` and `CT` are in the same region, and `TX` is the only location in its region. In the submission below, samples `"s1"` and `"s2"` are coarser, with rows for `MA` and `CT`, as in the coarser example. Samples `"s3"` and `"s4"` are joint across `horizon` only, with rows for `TX`. Each compound modeling task has two samples, and the submission passes validation.

```{margin} Samples per compound_idx
<div class="spl-hist">
  <div class="spl-hist-row"><span class="spl-hist-label">1 (MA)</span><span class="spl-hist-bar cidx-1" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">2 (CT)</span><span class="spl-hist-bar cidx-2" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">3 (TX)</span><span class="spl-hist-bar cidx-3" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
</div>
```

<table class="table spl-slices">
  <caption>Each solid box is one sample, and each dashed box inside it is one slice. Every second sample ID is in bold. The row colour shows the <code>compound_idx</code>.</caption>
  <thead>
    <tr>
      <th>origin_date</th>
      <th>location</th>
      <th>horizon</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
      <th>compound_idx</th>
    </tr>
  </thead>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-3 spl-first"><td>2024-03-15</td><td>TX</td><td>1</td><td>sample</td><td>s3</td><td>-</td><td><strong>3</strong></td></tr>
    <tr class="cidx-3 spl-last"><td>2024-03-15</td><td>TX</td><td>2</td><td>sample</td><td>s3</td><td>-</td><td><strong>3</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-3 spl-first"><td>2024-03-15</td><td>TX</td><td>1</td><td>sample</td><td><strong>s4</strong></td><td>-</td><td><strong>3</strong></td></tr>
    <tr class="cidx-3 spl-last"><td>2024-03-15</td><td>TX</td><td>2</td><td>sample</td><td><strong>s4</strong></td><td>-</td><td><strong>3</strong></td></tr>
  </tbody>
</table>

Mixed dependence structures pass only when the dependence structure of every sample matches `compound_taskid_set` or is coarser than it. A finer sample fails the submission, whatever the other samples are joint across.

#### Partly overlapping samples fail

Mixed dependence structures have a second limit: samples must not partly overlap. In the submission below, samples `"s1"` and `"s2"` are both joint across `horizon` and `location`. Sample `"s1"` has rows for `MA` and `CT`, and sample `"s2"` has rows for `CT` and `TX`. The two samples share `CT`, but `"s1"` also has rows for `MA` and `"s2"` for `TX`. Samples like these **partly overlap**, and the submission fails validation. Samples that have rows for any location in common must have rows for the same set of locations.

```{margin} Samples per compound_idx
<div class="spl-hist">
  <div class="spl-hist-row"><span class="spl-hist-label">1 (MA)</span><span class="spl-hist-bar cidx-1" style="--n: 1"></span><span class="spl-hist-n">1</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">2 (CT)</span><span class="spl-hist-bar cidx-2" style="--n: 2"></span><span class="spl-hist-n">2</span></div>
  <div class="spl-hist-row"><span class="spl-hist-label">3 (TX)</span><span class="spl-hist-bar cidx-3" style="--n: 1"></span><span class="spl-hist-n">1</span></div>
</div>
```

<table class="table spl-slices">
  <caption>Each solid box is one sample, and each dashed box inside it is one slice. Every second sample ID is in bold. The row colour shows the <code>compound_idx</code>.</caption>
  <thead>
    <tr>
      <th>origin_date</th>
      <th>location</th>
      <th>horizon</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
      <th>compound_idx</th>
    </tr>
  </thead>
  <tbody class="spl-slice">
    <tr class="cidx-1 spl-first"><td>2024-03-15</td><td>MA</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
    <tr class="cidx-1"><td>2024-03-15</td><td>MA</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>1</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2 spl-last"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td>s1</td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-2 spl-first"><td>2024-03-15</td><td>CT</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
    <tr class="cidx-2"><td>2024-03-15</td><td>CT</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>2</strong></td></tr>
  </tbody>
  <tbody class="spl-slice">
    <tr class="cidx-3"><td>2024-03-15</td><td>TX</td><td>1</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>3</strong></td></tr>
    <tr class="cidx-3 spl-last"><td>2024-03-15</td><td>TX</td><td>2</td><td>sample</td><td><strong>s2</strong></td><td>-</td><td><strong>3</strong></td></tr>
  </tbody>
</table>

A hub that accepts partly overlapping samples, for example from ensembles, can skip this check with the `allow_overlapping_samples` argument of the hubValidations validation functions. The other checks still split and count samples by compound modeling task, so the counts can become uneven. The submission above still fails, because `CT` has two samples while `MA` and `TX` have one each. Partly overlapping samples pass only when every compound modeling task ends up with the same number of samples.

In short, mixed dependence structures must still split evenly against `compound_taskid_set`. No sample can be finer than it, samples that have rows for any location in common must have rows for the same set of locations (unless the hub allows partly overlapping samples), and every `compound_idx` in the submission must have the same number of samples.

#### Dependence structure in submission, validation and analysis

The tables above show each submission in two views. The solid boxes show the modeler's view: rows that share an `output_type_id` come from one joint draw, so the boxes show the dependence structure of the model that drew the samples. The colours, `compound_idx` values and dashed slices show the same samples through the hub's `compound_taskid_set`, the view validation takes.

Evaluation usually takes the same view. A joint score, such as the energy score, is computed for each compound modeling task of the `compound_taskid_set` it is given, usually the hub's. An analysis can also use its own view, but only for models whose samples are all at least as coarse as that view. For example, an analysis can score samples jointly across all locations, using only the models in which every sample is joint across all locations.

| | View | What happens |
|---|---|---|
| Submitting | The model's own, recorded by which rows share an `output_type_id` | Each sample is joint across `horizon`, and can also be joint across `location`. A submission can mix dependence structures if its samples do not partly overlap, unless the hub allows partly overlapping samples. |
| Validating | `compound_taskid_set` | Rows are matched to compound modeling tasks by their values of its task IDs. Rows are grouped by `output_type_id` and `compound_idx` into slices. Each slice is checked and counted as a sample of its compound modeling task. |
| Analysing | `compound_taskid_set`, or a view the analysis chooses | Rows of one model and round that share an `output_type_id` are read as one joint draw (see [scope of sample IDs](#sample-output-type-id-scope)). Analyses that group samples by `compound_taskid_set`, such as joint scoring in hubEvals, split coarser samples by location. An analysis of the dependence between `MA` and `CT` uses the samples as submitted. |

### Number of samples vs. `output_type_id`

The total number of samples per individual modeling task in the above examples can always be determined by the number of times that each unique combination of task ID variables (i.e., each individual modeling task) appears in the submission. For Submissions A, B, C, and D above, even though the number of unique values of `output_type_id` changes, all examples have two samples per individual modeling task since each task ID set appears exactly twice in the provided data (i.e., a unique combination of "origin_date", "location", "horizon", "variant").

### Relationship to `output_type`

Compound modeling tasks are a general conceptual property of the way targets for a hub are defined. As such, they could be configured for a specific target, for all output types, not just samples. However, at the present time, we choose to only implement the concept of compound modeling tasks for the sample `output_type`, to facilitate data format validation for samples. In mathematical terms, this means that all output types may collect predictions from marginal distributions, but only samples can collect predictions from joint distributions.

At a later time, the hubverse may revisit a way to more generally define compound modeling tasks, as they can be used for different things. For example, compound modeling tasks defined for a compositional data target could

 - validate that all of the proportions in a set of "mean" `output_types` sum to 1.
 - be used to evaluate the proportions in a set of "mean" `output_types`, since evaluating each modeling task independently would result in inappropriate duplication of scores for what should be viewed as a single multivariate outcome.

<br>

Documentation about tests for other output types can be found in [Validation Pull Requests on GitHub](https://hubverse-org.github.io/hubValidations/articles/validate-pr.html#validate_pr-check-details).
