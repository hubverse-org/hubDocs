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

[^2]: The `compound_idx` column indicates which rows belong to the same group. In the marginal case shown here, each group contains samples for one modeling task. This column is not a task ID variable and is not typically present in actual model output data.

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

Give each independent draw its own sample ID. Rows that share an ID are one draw, so restarting the numbering at each location describes samples that are joint across locations.

A sample ID identifies a draw only within one model output file, which holds the predictions of one model for one round. Validation checks sample IDs within that file only. Two files can therefore use the same sample IDs, and in model output combined across models or rounds, the same ID can refer to unrelated draws. A draw in combined model output is identified by its `model_id`, its round ID and its `output_type_id` together.

A hub that wants sample IDs to be distinct across all of its model output can use character IDs that encode the model and the round, such as the `"3fa9c2e12_001"` example above. Validation does not check that such IDs are distinct across files.

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

Notice that this example submission file could be displaying predictions with any number of response dependence structures (or none at all) since we are not given the `output_type_id` values or `compound_taskid_set`. The following subsection provides four possible combinations of compound modeling tasks that this model output data may be representing. Different samples are distinguished from each other by using light and dark gray to highlight adjacent samples.

### Examples of different `compound_taskid_set` configurations

(sample-example-a)=
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

(sample-example-b)=
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

This is the limiting case of Example D. No task ID is held constant, so every task ID varies within a group and all of them are sampled jointly. Only a hub whose rounds are not identified by a task ID can declare an empty set (see [the round ID variable](#compound-taskid-set-round-id)).

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
Omitting `compound_taskid_set` and setting it to `[]` configure the two ends of the range: the finest compound modeling task and the coarsest.

| `"compound_taskid_set"` | resolves to | meaning |
|:--- |:--- |:--- |
| omitted | all task IDs | each modeling task is its own compound modeling task (Example A); jointly sampled submissions also pass |
| `[]` | no task IDs | every task ID is sampled jointly (Example E) |

Setting the field to `[]` to express "this hub has no compound task IDs to declare" therefore configures the coarsest structure instead of the finest. In a hub whose rounds are not identified by a task ID, the configuration is valid, so the mistake is not caught when the config is validated. It surfaces later, when submissions that are not jointly sampled across every task ID are rejected for describing a finer compound modeling task than the hub accepts.
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

To put it another way, samples can only describe "coarser" compound modeling tasks than those defined using the `compound_taskid_set` field. This is why all example submissions in the first row of the table pass validation, yet Example Submission A fails validation when the `compound_taskid_set` does not contain all four task ID variables.

```{caution}
[**Derived task IDs**](#derived-task-id-variables) are a type of task IDs whose values depend wholly on that of other task ID variables. A common example is the `target_end_date` task ID, which tends to be derived from the combination of the `reference_date` (or `origin_date`) and `horizon` task IDs.

These derived task IDs must be properly configured, or they can cause problems when validating compound modeling tasks by throwing errors when they should not. *If **all** the task ID variables a derived task ID is derived from are part of the `compound_taskid_set`, then that derived task ID must also be a part of the `compound_taskid_set`; otherwise, that derived task ID should be excluded.*

For example, if `reference_date` and `horizon` are both part of the `compound_taskid_set`, then the derived task ID `target_end_date` should be part of the `compound_taskid_set`. However, if, say, `horizon` displays response dependence and is thus not part of the `compound_taskid_set`, then `target_end_date` should also be excluded from the `compound_taskid_set`.
```

(compound-taskid-set-round-id)=
#### The round ID variable

When a round sets `round_id_from_variable` to `true`, every sample `compound_taskid_set` in that round must include the task ID named by `round_id` (see [`tasks.json` configuration](#tasks-metadata)). Each model output file covers a single round, so the round ID variable holds one value throughout the file. A sample therefore cannot be joint across it. In Examples A to D, `origin_date` would serve as the round ID variable, which is why every set includes it. An empty set is only valid when `round_id_from_variable` is `false`.

From hubAdmin 1.11.0, `validate_config()` reports an error for a set that leaves out the round ID variable, including an empty set. Omitting `compound_taskid_set` remains valid. Validating submissions against an empty set requires hubValidations 3.0.0 or later.

(sample-validation)=
### Validating coarser samples

The examples in this section use a configured `compound_taskid_set` of `["origin_date", "location", "horizon", "variant"]`, so each compound modeling task is one variant at one horizon. Each of the example submissions A to D passes validation against it.

#### Samples are validated in each compound modeling task they cover

A sample that is coarser than the configured set covers several compound modeling tasks. Validation splits the sample into one slice per compound modeling task, and checks each slice within its compound modeling task. In [Example B](#sample-example-b), sample `"s1"` is joint across the four variants at horizon 1, so it has four slices. It counts as one sample for each of the four compound modeling tasks. `"min_samples_per_task"` and `"max_samples_per_task"` therefore apply to the number of samples in each compound modeling task, and each compound modeling task in Example B holds two samples.

#### Samples in a modeling task can have different compound task ID sets

Each sample's compound task ID set is checked against the configured set on its own, and the samples in a modeling task do not have to share one set. In the submission below, the horizon 1 samples are joint across variants, as in [Example B](#sample-example-b), and the horizon 2 samples cover one variant each, as in [Example A](#sample-example-a). The submission passes validation.

The table shows variants `AA` and `BB` only, and leaves out the task ID columns that hold a single value. Here, `compound_idx` numbers the compound modeling tasks of the configured set, and each compound modeling task has its own colour. The rows of each sample are boxed together. Sample `"s1"` has two slices, one in compound idx 1 and one in compound idx 2. Each of the horizon 2 samples has a single slice. Every compound modeling task holds two samples.

<table class="table spl-slices">
  <thead>
    <tr>
      <th>compound_idx</th>
      <th>horizon</th>
      <th>variant</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr class="cidx-1 spl-first"><td>1</td><td>1</td><td>AA</td><td>sample</td><td><strong>s1</strong></td><td>-</td></tr>
    <tr class="cidx-2 spl-last"><td>2</td><td>1</td><td>BB</td><td>sample</td><td><strong>s1</strong></td><td>-</td></tr>
    <tr class="cidx-1 spl-first"><td>1</td><td>1</td><td>AA</td><td>sample</td><td>s2</td><td>-</td></tr>
    <tr class="cidx-2 spl-last"><td>2</td><td>1</td><td>BB</td><td>sample</td><td>s2</td><td>-</td></tr>
    <tr class="cidx-3 spl-first spl-last"><td>3</td><td>2</td><td>AA</td><td>sample</td><td><strong>s3</strong></td><td>-</td></tr>
    <tr class="cidx-3 spl-first spl-last"><td>3</td><td>2</td><td>AA</td><td>sample</td><td>s4</td><td>-</td></tr>
    <tr class="cidx-4 spl-first spl-last"><td>4</td><td>2</td><td>BB</td><td>sample</td><td><strong>s5</strong></td><td>-</td></tr>
    <tr class="cidx-4 spl-first spl-last"><td>4</td><td>2</td><td>BB</td><td>sample</td><td>s6</td><td>-</td></tr>
  </tbody>
</table>

<p class="spl-legend">
  <span class="spl-swatch cidx-1"></span>compound_idx 1 (horizon 1, AA): n = 2
  <span class="spl-swatch cidx-2"></span>compound_idx 2 (horizon 1, BB): n = 2
  <span class="spl-swatch cidx-3"></span>compound_idx 3 (horizon 2, AA): n = 2
  <span class="spl-swatch cidx-4"></span>compound_idx 4 (horizon 2, BB): n = 2
</p>

#### Partly overlapping samples fail validation

Two samples partly overlap when they share some compound modeling tasks but not others. In the submission below, sample `"s1"` is joint across variants `AA` and `BB`, and sample `"s2"` across `BB` and `CC`. Sample `"s3"` covers `BB` only. The three samples share `BB`, but each covers different variants[^6], so the submission fails validation.

The table shows horizon 1 for variants `AA` to `CC`, with the same layout as the table above.

<table class="table spl-slices">
  <thead>
    <tr>
      <th>compound_idx</th>
      <th>variant</th>
      <th>output_type</th>
      <th>output_type_id</th>
      <th>covers</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr class="cidx-1 spl-first"><td>1</td><td>AA</td><td>sample</td><td><strong>s1</strong></td><td>AA, BB</td><td>-</td></tr>
    <tr class="cidx-2 spl-last"><td>2</td><td>BB</td><td>sample</td><td><strong>s1</strong></td><td>AA, BB</td><td>-</td></tr>
    <tr class="cidx-2 spl-first"><td>2</td><td>BB</td><td>sample</td><td>s2</td><td>BB, CC</td><td>-</td></tr>
    <tr class="cidx-3 spl-last"><td>3</td><td>CC</td><td>sample</td><td>s2</td><td>BB, CC</td><td>-</td></tr>
    <tr class="cidx-2 spl-first spl-last"><td>2</td><td>BB</td><td>sample</td><td><strong>s3</strong></td><td>BB</td><td>-</td></tr>
  </tbody>
</table>

<p class="spl-legend">
  <span class="spl-swatch cidx-1"></span>compound_idx 1 (AA): n = 1
  <span class="spl-swatch cidx-2"></span>compound_idx 2 (BB): n = 3
  <span class="spl-swatch cidx-3"></span>compound_idx 3 (CC): n = 1
</p>

[^6]: The `covers` column lists the variants each sample spans. Like `compound_idx`, it is added for illustration and is not part of model output.

A hub that accepts partly overlapping samples, for example from ensembles, can skip this check with the `allow_overlapping_samples` argument of the hubValidations validation functions. Each sample then counts once in every compound modeling task it covers, so the number of samples per compound modeling task can become uneven. In the submission above, `BB` holds three samples, while `AA` and `CC` hold one each.

### Number of samples vs. `output_type_id`

The total number of samples per individual modeling task in the above examples can always be determined by the number of times that each unique combination of task ID variables (i.e., each individual modeling task) appears in the submission. For Submissions A, B, C, and D above, even though the number of unique values of `output_type_id` changes, all examples have two samples per individual modeling task since each task ID set appears exactly twice in the provided data (i.e., a unique combination of "origin_date", "location", "horizon", "variant").

### Relationship to `output_type`

Compound modeling tasks are a general conceptual property of the way targets for a hub are defined. As such, they could be configured for a specific target, for all output types, not just samples. However, at the present time, we choose to only implement the concept of compound modeling tasks for the sample `output_type`, to facilitate data format validation for samples. In mathematical terms, this means that all output types may collect predictions from marginal distributions, but only samples can collect predictions from joint distributions.

At a later time, the hubverse may revisit a way to more generally define compound modeling tasks, as they can be used for different things. For example, compound modeling tasks defined for a compositional data target could

 - validate that all of the proportions in a set of "mean" `output_types` sum to 1.
 - be used to evaluate the proportions in a set of "mean" `output_types`, since evaluating each modeling task independently would result in inappropriate duplication of scores for what should be viewed as a single multivariate outcome.

<br>

Documentation about tests for other output types can be found in [Validation Pull Requests on GitHub](https://hubverse-org.github.io/hubValidations/articles/validate-pr.html#validate_pr-check-details).
