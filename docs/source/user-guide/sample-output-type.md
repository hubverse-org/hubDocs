# Sample output type

## Introduction

The sample `output_type` can represent a probabilistic distribution through a collection of possible future observed values ("samples") that originate from a predictive model. Depending on the model's setup and the hub's configuration settings, different information may be requested or required to identify each sample.

In the hubverse, a "modeling task" is defined by a unique combination of task ID column values. You can think of each modeling task as a specific point (or "slice") in the space defined by the task ID variables that we are interested in predicting. Each modeling task results in a single prediction. (Note that this concept is similar to that of a ["forecast unit" in the scoringutils R package](https://epiforecasts.io/scoringutils/reference/set_forecast_unit.html).)

We will use the following `model_output` data to help solidify the concept of a modeling task. (The mean `output_type` is used for demonstration purposes due to its simplicity.)

| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 |  1 | MA | mean | NA| - |
| 2024-03-15 |  2 | MA | mean | NA| - |
| 2024-03-15 |  3 | MA | mean | NA| - |

In this table, the task ID columns are `origin_date`, `horizon`, and `location`. There are three modeling tasks (one per row): horizon 1, horizon 2, and horizon 3—all for Massachusetts and origin date 2024-03-15. The first row, for example, represents a single slice of task ID space, a prediction for one week ahead in Massachusetts, resulting in one predicted value.


## Sampling modeling tasks

While the mean output type produces a single predicted value per modeling task, the sample output type captures uncertainty by providing multiple possible values at each slice of task ID space. Each sample represents one possible outcome, and together, the collection of samples describes a distribution of predicted values.

How modeling tasks relate to each other determines the structure of this distribution. When modeling tasks are treated independently, samples at each slice form a univariate (single-variable) distribution. When modeling tasks are grouped together, samples capture a multivariate (joint) distribution across the group.

## Marginal distributions

In many settings, predictions will be made for individual modeling tasks, with no notion of modeling tasks being related to each other or collected into sets (for more on this, see the [compound modeling tasks section](#compound-modeling-tasks)). When predictions are assumed to be made for individual modeling tasks, every modeling task is treated as distinct. In mathematical terms, these samples represent draws from marginal predictive distributions.

Now, suppose we wanted to collect samples for each of the modeling tasks defined in the previous section. The table below shows a dataset with three groups (indicated by `compound_idx`[^1] values 1, 2, and 3) and three samples per group. The `output_type_id` column contains sample indexes that are unique across an entire model output file, not just within each group, so each group has distinct sample indexes (0-2, 3-5, and 6-8 respectively). When sampling from marginal distributions, each group corresponds to a single modeling task, so all task ID values are identical within each group. Notice how each group represents samples for a single slice of task ID space.

[^1]: The `compound_idx` column is a visual aid to indicate which rows belong to the same group. In the marginal case shown here, each group contains samples for one modeling task. This column is not a task ID variable and is not typically present in actual model output data.

|compound_idx| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | 1 | MA | sample | 0| - |
| 1 | 2024-03-15 | 1 | MA | sample | 1| - |
| 1 | 2024-03-15 | 1 | MA | sample | 2| - |
| 2 | 2024-03-15 | 2 | MA | sample | 3| - |
| 2 | 2024-03-15 | 2 | MA | sample | 4| - |
| 2 | 2024-03-15 | 2 | MA | sample | 5| - |
| 3 | 2024-03-15 | 3 | MA | sample | 6| - |
| 3 | 2024-03-15 | 3 | MA | sample | 7| - |
| 3 | 2024-03-15 | 3 | MA | sample | 8| - |

In this setting, a hub will specify a minimum and maximum number of required samples per group in the configuration for the prediction task. In the marginal case, each group corresponds to a single modeling task, but as we will see in the [compound modeling tasks section](#compound-modeling-tasks), a group can span multiple modeling tasks. The associated configuration might look like:

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

More specifically, the `"output_type_id_params"` property specifies that sample `output_type_id`s must be integers, and there must be exactly (i.e., no more or less than) 3 samples per modeling task (group). The `"value"` specification refers to the predicted values contained in the "value" column (e.g., they must be storable as numeric "double" format and be no less than zero) and the `"is_required"` property specifies that samples are a required output type.

Note that samples use an `"output_type_id_params"` block to define allowable values through parameters (like min/max). Other output types use an `"output_type_id"` block that lists required and optional values explicitly.

(compound-modeling-tasks)=
## Compound modeling tasks

In the previous section, we saw that when sampling from marginal distributions, each sample is drawn from a single modeling task (a single slice of task ID space). In some settings, however, modeling hubs may wish to capture relationships between modeling tasks by sampling from a joint distribution. This means drawing values for multiple modeling tasks at once as a coherent set.

Consider two common scenarios:
- **Trajectories over time**: A model might predict values across multiple time horizons as a coherent path. Rather than drawing each horizon's prediction independently, the model draws an entire trajectory, a sample from a joint distribution over horizons.
- **Variant proportions**: A model predicting proportions of multiple disease variants might draw all variant proportions together, a sample from a joint distribution across variants.

In both cases, joint sampling introduces additional dimensions to the predictive distribution. Instead of a univariate distribution at each modeling task, we have a multivariate distribution spanning multiple modeling tasks. We refer to this as **response dependence** across the task IDs that vary within a group, because the predicted values (responses) for different modeling tasks are statistically dependent.

Within a group of jointly sampled modeling tasks, some task ID values remain constant (defining which group we're in), while others vary (defining the multiple modeling tasks covered by the joint distribution). The `"compound_taskid_set"` specifies which task IDs remain constant within a group. Task IDs not in this set vary within the group and are sampled jointly, introducing response dependence across those task IDs. A **compound modeling task** is thus a group of related predictions defined by the compound task ID set.

Consider the following model output[^2] submission file from a hub reporting on **variant** proportions observed in **Massachusetts** (`location`) on **2024-03-15** (`origin_date`) for **1 and 2 week predictions** (`horizon`). There are four variants (`AA`, `BB`, `CC`, and `DD`) represented over two horizons, with two sample predictions for each of the eight combinations; this results in a total of 16 rows of sample output type predictions.

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

[^2]: In model output files, an entry of "-" stands in for specific values to be provided by the submitter. They are not assumed to be identical.

Notice that this example submission file could be displaying predictions with any number of response dependence structures (or none at all) since we are not given the `output_type_id` values or compound task-id set. The following subsection provides four possible combinations of compound modeling tasks that this model output data may be representing.

### Examples of different `compound_taskid_set` configurations

#### Example A: No response dependence across task IDs
***Each group = one modeling task***

This is essentially the marginal case described earlier, included here for comparison. Each group contains a single modeling task, with no response dependence across any task IDs.

<div class="heatMap1">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 1 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 1 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 1 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 1 | DD | sample | s7 | - |
| 4 | 2024-03-15 | MA | 2 | AA | sample | s8 | - |
| 4 | 2024-03-15 | MA | 2 | AA | sample | s9 | - |
| 5 | 2024-03-15 | MA | 2 | BB | sample | s10 | - |
| 5 | 2024-03-15 | MA | 2 | BB | sample | s11 | - |
| 6 | 2024-03-15 | MA | 2 | CC | sample | s12 | - |
| 6 | 2024-03-15 | MA | 2 | CC | sample | s13 | - |
| 7 | 2024-03-15 | MA | 2 | DD | sample | s14 | - |
| 7 | 2024-03-15 | MA | 2 | DD | sample | s15 | - |

</div>

```{attention}
Rows with the same `compound_idx` value indicate distinct sample predictions made for the same group. In this marginal case, each group contains a single modeling task. For example, each pair of rows with the same `compound_idx` correspond to the same modeling task, but are each from one of sixteen distinct sample draws "s#".
```

The table above shows eight unique modeling tasks, with two samples for each. A unique combination of `origin_date`, `location`, `horizon`, and `variant` defines each modeling task.

To configure this response dependence structure, all task IDs are included in the `compound_taskid_set`:

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
| 0 | 2024-03-15 | MA | 1 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | DD | sample | s1 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | CC | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | DD | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | AA | sample | s3 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s3 | - |
| 1 | 2024-03-15 | MA | 2 | CC | sample | s3 | - |
| 1 | 2024-03-15 | MA | 2 | DD | sample | s3 | - |

</div>

```{attention}
Rows are grouped so each unique sample for each compound modeling task is together. The first four rows correspond to the first sample ("s0") for the first compound modeling task (compound_idx=0), covering all four variants. The second four rows correspond to the second sample ("s1") for the same compound modeling task.
```

The table above shows two unique compound modeling tasks (shown with the `compound_idx` column), with two independent sample draws for each, identified by `output_type_id` (s0, s1, s2, s3, making a total of four samples). Each compound modeling task is defined by a fixed combination of `origin_date`, `horizon`, and `location` values, while the values of `variant` vary.

To configure this response dependence structure, `variant` is excluded from the `compound_taskid_set`:

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
| 0 | 2024-03-15 | MA | 1 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 2 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 2 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 1 | BB | sample | s3 | - |
| 1 | 2024-03-15 | MA | 2 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 1 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 2 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 1 | CC | sample | s5 | - |
| 2 | 2024-03-15 | MA | 2 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 1 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 2 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 1 | DD | sample | s7 | - |
| 3 | 2024-03-15 | MA | 2 | DD | sample | s7 | - |

</div>

The table above shows four unique compound modeling tasks (shown with the `compound_idx` column) and two independent sample draws for each, identified by `output_type_id` (s0-s7, making a total of eight samples). Each compound modeling task is defined by a fixed combination of `origin_date`, `location`, and `variant` values, while `horizon` varies.

To configure this response dependence structure, `horizon` is excluded from the `compound_taskid_set`:

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

#### Example D: Response dependence across horizons and variants
***Joint distribution across both horizons and variants***

Here, there is response dependence across both `horizon` and `variant`. Each sample represents a grouped collection of possible values for all four variants across both prediction horizons.

<div class="heatMap3">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 2 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 2 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 2 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 2 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 1 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 1 | DD | sample | s1 | - |
| 0 | 2024-03-15 | MA | 2 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 2 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 2 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 2 | DD | sample | s1 | - |

</div>

The table above shows one unique compound modeling task (shown with the `compound_idx` column value) and two unique sample draws, identified by `output_type_id` (s0 and s1). This single compound modeling task can be described as predictions for **"Massachusetts with the `origin_date` of `2024-03-15`"**, with a fixed combination of `origin_date` and `location` values, while both `horizon` and `variant` vary.

To configure this response dependence structure, both `horizon` and `variant` are excluded from the `compound_taskid_set`:

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

### Configuration of `compound_taskid_set`

Different models may generate samples for different compound modeling tasks. For example, some might simulate data from all horizons sequentially, making predictions that consider what has happened at past horizons. Such a model would create output data like that of Examples C and D in the previous subsection, which have response dependence across horizons. Other models might only simulate draws from each horizon independently from other time points; these models would have output data similar to that of Examples A or B, which have no response dependence across horizons.

A hub should specify a `"compound_taskid_set"` field in the configuration for the sample `output_type` to indicate the task-id columns that define separate sample index values in the `output_type_id` column. **The `output_type_id` column allows a modeler to show which rows of model output belong to the same sample.**

Sometimes, multiple `"compound_taskid_set"` specifications may be valid for a single model output file; in this case, it is important to indicate which one applies to the given submission file so that the contents are correctly interpreted. The following table[^3] shows how different specifications of the `"compound_taskid_set"` field would impact the validity of each example submission A, B, C, and D in the previous subsection.

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
    <th scope="row"><code>["origin_date", "location"]</code></th>
    <td>❌</td>
    <td>❌</td>
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
</table>

[^3]: The letters shown in parentheses shown in the column names indicate the actual composition of the compound task id set in the examples from the previous subsection, where 1) o_d is origin_date, 2) l is location, 3) h is horizon, and 4) v is variant.

<br>

In general, a submission will pass validation if the task-id variables that define a compound modeling task (as implied by the sample ID values present in the `output_type_id` column) are also present in the `"compound_taskid_set"`. For the example of [`"origin_date"`, `"horizon"`, `"location"`] in the table above:
- Both Submissions B and D would pass validation since when the data are grouped by the `"compound_taskid_set"` variables you can always find a group of rows that have the same `output_type_id`.
- Submissions A and C would fail validation since when the data are grouped by the `"compound_taskid_set"` variables, there would be no rows that share an `output_type_id`.

To put it another way, samples can only describe "coarser" compound modeling tasks than those defined using the `compound_taskid_set` field. This is why all example submissions in the first row of the table pass validation, yet Example Submission A fails validation when the `compound_taskid_set` does not contain all four task-id variables.

```{caution}
**Derived task-ids** are a type of task-ids whose values depend wholly on that of other task-id variables. A common example is the `target_end_date` task-id, which tends to be derived from the combination of the `reference_date` (or `origin_date`) and `horizon` task-ids.

These derived task-ids must be properly configured, or they can cause problems when validating compound modeling tasks by throwing erroneous errors. *If **all** the task-id variables a derived task-id is derived from are part of the `compound_taskid_set`, then that derived task-id must also be a part of the `compound_taskid_set`; otherwise, that derived task-id should be excluded.*
```

### Number of samples vs. `output_type_id`

The number of samples per individual modeling task in the above examples can always be determined by the number of times that each unique combination of task-id variables (i.e., each individual modeling task) appears in the submission. For Submissions A, B, C, and D above, even though the number of unique values of `output_type_id` changes, all examples have two samples per individual modeling task since each task-id-set appears exactly twice in the provided data.

### Relationship to `output_types`

Compound modeling tasks are a general conceptual property of the way targets for a hub are defined. As such, they could be configured for a specific target, for all output types, not just samples. However, at the present time, we choose to only implement the concept of compound modeling tasks for sample `output_types`, to facilitate data format validation for samples. In mathematical terms, this means that all output types may collect predictions from marginal distributions, but only samples can collect predictions from joint distributions.

At a later time, the hubverse may revisit a way to more generally define compound modeling tasks, as they can be used for different things. For example, compound modeling tasks defined for a compositional data target could

 - validate that all of the proportions in a set of "mean" `output_types` sum to 1.
 - be used to evaluate the proportions in a set of "mean" `output_types`, since evaluating each modeling task independently would result in inappropriate duplication of scores for what should be viewed as a single multivariate outcome.

<br>

Documentation about tests for other output types can be found in [Validation Pull Requests on GitHub](https://hubverse-org.github.io/hubValidations/articles/validate-pr.html#validate_pr-check-details).

