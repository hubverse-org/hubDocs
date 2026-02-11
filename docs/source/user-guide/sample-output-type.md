# Sample output type

## Introduction

The sample `output_type` can represent a probabilistic distribution through a collection of possible future observed values ("samples") that originate from a predictive model. Depending on the model's setup and the hub's configuration settings, different information may be requested or required to identify each sample.

In the hubverse, a "modeling task" is the element that is being predicted and that can be represented by a univariate (e.g., scalar or single) value. This can be tied to a tabular representation of data more concretely as a combination of values from a set of task ID columns that uniquely define a single prediction. (Note that this concept is similar to that of a ["forecast unit" in the scoringutils R package](https://epiforecasts.io/scoringutils/reference/set_forecast_unit.html).)

We will use the following `model_output` data to help solidify the concept of a modeling task. (The mean `output_type` is used for demonstration purposes due to its simplicity.)

| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | -1 | MA | mean | NA| - |
| 2024-03-15 |  0 | MA | mean | NA| - |
| 2024-03-15 |  1 | MA | mean | NA| - |

In the above table, the three task-id columns `origin_date`, `horizon`, and `location` uniquely define a modeling task in every row. Here, there are three modeling tasks (one for each row), represented by the tuples <br>

```
{origin_date: "2024-03-15", horizon: "-1", location: "MA"}
{origin_date: "2024-03-15", horizon: "0", location: "MA"}
{origin_date: "2024-03-15", horizon: "1", location: "MA"}
```

In words, the first of these tuples (as well as the first row in the table above it) represents a forecast for one day (assume here the horizon is on the timescale of day) before the origin date of 2024-03-15 in Massachusetts.


## Individual modeling tasks

In many settings, forecasts will be made for individual modeling tasks, with no notion of modeling tasks being related to each other or collected into sets (for more on this, see the [compound modeling tasks section](#compound-modeling-tasks)). When forecasts are assumed to be made for individual modeling tasks, every modeling task is treated as distinct. In mathematical terms, these forecasts are summarizing marginal predictive distributions.

Now, suppose we wanted to collect samples for each of the modeling tasks defined in the previous section. Then, we might end up with following data set, in which each block of three rows (denoted by a shared `compound_idx`[^1]) represents the sample output type forecasts for a particular modeling task. In this example, every modeling task (group) is treated as distinct.

[^1]: The `compound_idx` column is only used to denote rows that make forecasts for the same modeling task. It is not a task id variable, nor typically present in actual model output data.

|compound_idx| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 1 | 2024-03-15 | -1 | MA | sample | 0| - |
| 1 | 2024-03-15 | -1 | MA | sample | 1| - |
| 1 | 2024-03-15 | -1 | MA | sample | 2| - |
| 2 | 2024-03-15 | 0 | MA | sample | 3| - |
| 2 | 2024-03-15 | 0 | MA | sample | 4| - |
| 2 | 2024-03-15 | 0 | MA | sample | 5| - |
| 3 | 2024-03-15 | 1 | MA | sample | 6| - |
| 3 | 2024-03-15 | 1 | MA | sample | 7| - |
| 3 | 2024-03-15 | 1 | MA | sample | 8| - |

In this setting, a hub will specify a minimum and maximum number of required samples in the metadata for the prediction task. The associated configuration might look like:

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

In words, the above configuration specifies that  `"output_type_id_params"` samples are required, they must be integers, and there must be exactly (i.e., no more or less than) 3 samples per modeling task. The "value" specifications correspond to the values contained in the "value" column (e.g., they must be storable as numeric "double" format and be no less than zero).

Note that the `output_type_id` parameters are specified in an `"output_type_id_params"` block because they are parameters defining the allowable values. For other output types, the `"output_type_id"` block is used to list required and optional values explicitly.

(compound-modeling-tasks)=
## Compound modeling tasks

In some settings, modeling hubs may wish to identify sets of modeling tasks that the hub will treat as related; for example, when multiple distinct values can be seen as representations of a single multivariate outcome of interest (i.e., forecasts originate from a joint predictive distribution). We use a subset of the task-id columns (the `"compound_taskid_set"`) to identify which variables do not display any dependence within or across their values. Any samples with the same output_type_id are assumed to to be a single sample from a joint distribution.

Consider the following model output[^2] from a hub reporting on **variant** proportions observed in **Massachusetts** (`**location**`) on **2024-03-15** (`**origin_date**`) for **7 and 14 day forecasts** (`**horizon**`). There are four variants (`AA`, `BB`, `CC`, and `DD`) represented over two horizons, with two sample predictions for each of the eight combinations; this results in a total of 16 rows of sample output type forecasts.

| origin_date | horizon | variant |location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | 7 | AA | MA | sample | - | - |
| 2024-03-15 | 7 | AA | MA | sample | - | - |
| 2024-03-15 | 7 | BB | MA | sample | - | - |
| 2024-03-15 | 7 | BB | MA | sample | - | - |
| 2024-03-15 | 7 | CC | MA | sample | - | - |
| 2024-03-15 | 7 | CC | MA | sample | - | - |
| 2024-03-15 | 7 | DD | MA | sample | - | - |
| 2024-03-15 | 7 | DD | MA | sample | - | - |
| 2024-03-15 | 14 | AA | MA | sample | - | - |
| 2024-03-15 | 14 | AA | MA | sample | - | - |
| 2024-03-15 | 14 | BB | MA | sample | - | - |
| 2024-03-15 | 14 | BB | MA | sample | - | - |
| 2024-03-15 | 14 | CC | MA | sample | - | - |
| 2024-03-15 | 14 | CC | MA | sample | - | - |
| 2024-03-15 | 14 | DD | MA | sample | - | - |
| 2024-03-15 | 14 | DD | MA | sample | - | - |

[^2]: In the tabular data, an entry of "-" stands in for specific values to be provided by the submitter. They are not assumed to be identical.

Notice that this example submission file could be displaying predictions with any number of dependence structures (or none at all) since we are not given the `output_type_id` values or compound task-id set. The following subsection provides four possible combinations of compound modeling tasks that this tabular data may be representing.

### Examples of distinct compound modeling tasks

#### Example A: No task ids display dependence

Sample `output_type` forecasts where **a single modeling task corresponds to a unique combination of `origin_date`, `location`, `horizon`, and `variant`**. There are no variables whose values display dependence.

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

The table below displays a subset of a possible submission for the prediction task specified in the above schema. There are eight unique modeling tasks in this example, with two samples for each.

```{attention}
Rows with the same `compound_idx` value indicate distinct sample forecasts made for the same compound forecast task. For example, in the table below, each pair of rows with the same `compound_idx` correspond to the same modeling task, but are each from one of sixteen distinct sample draws "s#".
```
<div class="heatMap1">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 7 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 7 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 7 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 7 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 7 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 7 | DD | sample | s7 | - |
| 4 | 2024-03-15 | MA | 14 | AA | sample | s8 | - |
| 4 | 2024-03-15 | MA | 14 | AA | sample | s9 | - |
| 5 | 2024-03-15 | MA | 14 | BB | sample | s10 | - |
| 5 | 2024-03-15 | MA | 14 | BB | sample | s11 | - |
| 6 | 2024-03-15 | MA | 14 | CC | sample | s12 | - |
| 6 | 2024-03-15 | MA | 14 | CC | sample | s13 | - |
| 7 | 2024-03-15 | MA | 14 | DD | sample | s14 | - |
| 7 | 2024-03-15 | MA | 14 | DD | sample | s15 | - |

</div>

#### Example B: Variant dependence

Sample `output_type` forecasts where a compound modeling task corresponds to a combination of values for `origin_date`, `horizon`, and `location`. In this example, **the proportions of all four variants at a given date, location, and horizon make up the compound modeling task**; that is, (viral) `variant` is the only task-id variable whose values display dependence.

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

The example data below is a subset of model output that shows two unique compound modeling tasks (shown with the `compound_idx` column) with two independent sample draws for each (making a total of four).

```{attention}
Once again, rows are grouped so each unique sample for each modeling task is together. Therefore, the first four rows correspond to the first sample ("s0") for the first modeling task, and the second four rows correspond to the second sample ("s1") for the first modeling task.
```

<div class="heatMap2">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | DD | sample | s1 | - |
| 1 | 2024-03-15 | MA | 14 | AA | sample | s2 | - |
| 1 | 2024-03-15 | MA | 14 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 14 | CC | sample | s2 | - |
| 1 | 2024-03-15 | MA | 14 | DD | sample | s2 | - |
| 1 | 2024-03-15 | MA | 14 | AA | sample | s3 | - |
| 1 | 2024-03-15 | MA | 14 | BB | sample | s3 | - |
| 1 | 2024-03-15 | MA | 14 | CC | sample | s3 | - |
| 1 | 2024-03-15 | MA | 14 | DD | sample | s3 | - |

</div>

#### Example C: Horizon and variant dependence

Sample `output_type` where each compound modeling task corresponds to a combination of `origin_date` and `location`. Here, there is a single compound modeling task, which we can describe as **"Massachusetts with the `origin_date` of `2024-03-15`"**. Both `horizon` and `variant` display dependence.

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

The table below has one unique compound modeling task (shown with the `compound_idx` column value) and two unique sample draws. Each sample represents a grouped collection of possible values for all four variants across both prediction horizons.

<div class="heatMap3">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 14 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 14 | BB | sample | s0 | - |
| 0 | 2024-03-15 | MA | 14 | CC | sample | s0 | - |
| 0 | 2024-03-15 | MA | 14 | DD | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 7 | DD | sample | s1 | - |
| 0 | 2024-03-15 | MA | 14 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 14 | BB | sample | s1 | - |
| 0 | 2024-03-15 | MA | 14 | CC | sample | s1 | - |
| 0 | 2024-03-15 | MA | 14 | DD | sample | s1 | - |

</div>

#### Example D: Horizon dependence

Sample `output_type` where a compound modeling task corresponds to a combination of values for `origin_date`, `location`, and `variant`. In other words, this could be described as **"trajectories of variant proportions over time in Massachusetts, with each variant treated independently from each other."** `Horizon` is the only variable that displays dependence.

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

The table below shows four unique compound modeling tasks (shown with the `compound_idx` column) and two independent sample draws for each.

<div class="heatMap4">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 14 | AA | sample | s0 | - |
| 0 | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| 0 | 2024-03-15 | MA | 14 | AA | sample | s1 | - |
| 1 | 2024-03-15 | MA | 7 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 14 | BB | sample | s2 | - |
| 1 | 2024-03-15 | MA | 7 | BB | sample | s3 | - |
| 1 | 2024-03-15 | MA | 14 | BB | sample | s3 | - |
| 2 | 2024-03-15 | MA | 7 | CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 14| CC | sample | s4 | - |
| 2 | 2024-03-15 | MA | 7 | CC | sample | s5 | - |
| 2 | 2024-03-15 | MA | 14 | CC | sample | s5 | - |
| 3 | 2024-03-15 | MA | 7 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 14 | DD | sample | s6 | - |
| 3 | 2024-03-15 | MA | 7 | DD | sample | s7 | - |
| 3 | 2024-03-15 | MA | 14 | DD | sample | s7 | - |

</div>

### Configuration of `compound_taskid_set`

Different models may generate samples for different compound modeling tasks. For example, some might simulate data from all horizons sequentially, making predictions that consider what has happened at past horizons. Such a model would create output data like that of Examples C and D in the previous subsection, which display dependence across horizons. Other models might only simulate draws from each horizon independently from other time points; these models would have output data similar to that of Examples A or B, which do not display dependence across horizons.

A hub should specify a `"compound_taskid_set"` field in the metadata for the sample `output_type` to indicate the task-id columns that define separate sample index values in the `output_type_id` column. **The `output_type_id` column allows a modeler to show which rows of model output belong to the same sample.**

Sometimes, multiple `"compound_taskid_set"` specifications may be valid for a single model output file; in this case, it is important to indicate which one applies to the given submission file so that the contents are correctly interpreted. The following table[^3] shows how different specifications of the `"compound_task_id_set"` field would impact the validity of each example submission A, B, C, and D in the previous subsection.

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
    <th scope="col"><strong>C (o_d,l)</strong></th>
    <th scope="col"><strong>D (o_d,l,v)</strong></th>
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
    <td>✅</td>
    <td>❌</td>
  </tr>
  <tr>
    <th scope="row"><code>["origin_date", "location"]</code></th>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
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
- Both Submissions B and C would pass validation since when the data are grouped by the `"compound_taskid_set"` variables you can always find a group of rows that have the same `output_type_id`.
- Submissions A and D would fail validation since when the data are grouped by the `"compound_taskid_set"` variables, there would be no rows that share an `output_type_id`.

To put it another way, samples can only describe "coarser" compound modeling tasks than those defined using the `compound_taskid_set` field. This is why all example submissions in the first row of the table pass validation, yet Example Submission A fails validation when the `compound_taskid_set` does not contain all four task id variables.

```{caution}
**Derived task-ids** are a type of task-ids whose values depend wholly on that of other task-id variables. A common example is the `target_end_date` task-id, which tends to be derived from the combination of the `reference_date` (or `origin_date`) and `horizon` task-ids.

These derived task-ids must be properly configured, or they can cause problems when validating compound modeling tasks by throwing erroneous errors. *If **all** the task-id variables a derived task-id is derived from are part of the `compound_task_id_set`, then that derived task-id must also be a part of the `compound_task_id_set`; otherwise, that derived task-id should be excluded.*
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

