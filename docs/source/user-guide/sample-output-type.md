# Sample output type  

## Introduction  
The sample `output_type` can be used to represent a probabilistic distribution through a collection of possible future observed values (“samples”) that come out of a predictive model. Depending on the setup of the model and the configuration settings of the hub, different information may be requested or required to identify each sample.

In the hubverse, a “modeling task” is the element that is being predicted and that can be represented by a univariate (e.g., scalar, or single) value. We could also tie this to a tabular representation of data more concretely as a combination of values from a set of task id columns that uniquely define a single prediction. We note that this concept is similar to that of a [“forecast unit” in the scoringutils R package](https://epiforecasts.io/scoringutils/reference/set_forecast_unit.html).

Take the following model_output data for the mean output_type as an example:
| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | -1 | MA | mean | NA| - |
| 2024-03-15 |  0 | MA | mean | NA| - |
| 2024-03-15 |  1 | MA | mean | NA| - |


In the above table, the three task-id columns origin_date, horizon, and location uniquely define a modeling task. Here, there are three modeling tasks, represented by the tuples <br>
```
{origin_date: “2024-03-15”, horizon: “-1”, location: “MA”}
{origin_date: “2024-03-15”, horizon: “0”, location: “MA”}
{origin_date: “2024-03-15”, horizon: “1”, location: “MA”}
```

In words, the first of these tuples represents a forecast for one day (assume here the horizon is on the timescale of day) prior to the origin date of 2024-03-15 in Massachusetts. 

## Individual modeling tasks
In many settings, forecasts will be made for individual modeling tasks, with no notion of modeling tasks being related to each other or collected into sets (for more on this, see [Compound modeling tasks](#compound-modeling-tasks)). In the situations where forecasts are assumed to be made for individual modeling tasks, every modeling task is treated as distinct, as is implied by the compound_idx column in the table below (grayed out to indicate that such a column exists implicitly in the dataset and is not typically present in the actual tabular data). In this setting, the output_type_id column indexes the samples that exist for each modeling task.

|compound_idx| origin_date | horizon | location | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| ${\color{lightgrey}1}$ | 2024-03-15 | -1 | MA | sample | 0| - |
| ${\color{lightgrey}1}$ | 2024-03-15 | -1 | MA | sample | 1| - |
| ${\color{lightgrey}1}$ | 2024-03-15 | -1 | MA | sample | 2| - |
| ${\color{lightgrey}2}$ | 2024-03-15 | 0 | MA | sample | 3| - |
| ${\color{lightgrey}2}$ | 2024-03-15 | 0 | MA | sample | 4| - |
| ${\color{lightgrey}2}$ | 2024-03-15 | 0 | MA | sample | 5| - |
| ${\color{lightgrey}3}$ | 2024-03-15 | 1 | MA | sample | 6| - |
| ${\color{lightgrey}3}$ | 2024-03-15 | 1 | MA | sample | 7| - |
| ${\color{lightgrey}3}$ | 2024-03-15 | 1 | MA | sample | 8| - |

In this setting, a hub will specify a minimum and maximum number of required samples in the metadata for the prediction task. The associated configuration might look like:

```
"output_type":{
	"sample":{
		"output_type_id_params":{
			“is_required”: true,
			“type”: “integer”,
                        "min_samples_per_task": 100,
			"max_samples_per_task": 100
		},
		"value":{
			"type":"double",
			"minimum":0
		}
	}
}
```

In words, the above configuration specifies that  "output_type_id_params" samples are required, they must be integers, and there must be exactly (i.e., no more or less than) 100 samples per modeling task. The "value" specifications correspond to the values contained in the "value" column (e..g they must be storable as numeric "double" format and be no less than zero).

Note that the output_type_id parameters are specified in an “output_type_id_params” block because they are parameters defining the allowable values. For other output types, the “output_type_id” block is used to explicitly list required and optional values.

(compound-modeling-tasks)=
## Compound modeling tasks

There are settings where modeling hubs may wish to identify sets of modeling tasks that the hub will treat as being related to each other. This occurs when multiple distinct values that can be seen as being representations of a single multivariate outcome of interest. In these settings, a subset of the task-id columns (a “compound_taskid_set”) will be used to identify what values are shared for the modeling tasks that are related to each other.

As a running example of how compound modeling tasks could be specified in different ways, we will look at a hub reporting on variant proportions observed at a given location and at a given time. In the table below, a single modeling task is a unique combination of values from the task-id variables origin_date, horizon, variant, and location.  In the table below, one set of four rows with the same values in the origin_date, horizon, and location columns but different variant values below represent four predicted variant proportions. 

Base data: mean output_type. In the table below, an entry of “-” stands in for specific values to be provided by the submitter.

| origin_date | horizon | variant |location | output_type| output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | 7 | AA | MA | sample | - | - |
| 2024-03-15 | 7 | BB | MA | sample | - | - |
| 2024-03-15 | 7 | CC | MA | sample | - | - |
| 2024-03-15 | 7 | DD | MA | sample | - | - |
| 2024-03-15 | 14 | AA | MA | sample | - | - |
| 2024-03-15 | 14 | BB | MA | sample | - | - |
| 2024-03-15 | 14 | CC | MA | sample | - | - |
| 2024-03-15 | 14 | DD | MA | sample | - | - |

### Four submissions, differing by compound modeling task
**Submission A**: sample output_type where **a single modeling task corresponds to a unique combination of origin_date, location, horizon, and variant**. There are eight unique modeling tasks in this example.

```
"output_type_id_params":{
			“is_required”: true,
			“type”: “character”,
			“max_length”: 6,
                        "min_samples_per_task": 90,
			"max_samples_per_task": 100,
			"compound_taskid_set": ["origin_date", "location", "horizon", "variant"]
		}
```

```{attention}
Rows are shaded to indicate different samples for the same compound forecast task. For example in the table below, the first two rows correspond to the same modeling task but they are highlighted to show that the first row is from sample "s0" while the second row is from sample "s1".
```
<div class="heatMap1">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 7 | BB | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 7 | BB | sample | s3 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 7 | CC | sample | s4 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 7 | CC | sample | s5 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 7 | DD | sample | s6 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 7 | DD | sample | s7 | - |
| ${\color{lightgrey}4}$ | 2024-03-15 | MA | 14 | AA | sample | s8 | - |
| ${\color{lightgrey}4}$ | 2024-03-15 | MA | 14 | AA | sample | s9 | - |
| ${\color{lightgrey}5}$ | 2024-03-15 | MA | 14 | BB | sample | s10 | - |
| ${\color{lightgrey}5}$ | 2024-03-15 | MA | 14 | BB | sample | s11 | - |
| ${\color{lightgrey}6}$ | 2024-03-15 | MA | 14 | CC | sample | s12 | - |
| ${\color{lightgrey}6}$ | 2024-03-15 | MA | 14 | CC | sample | s13 | - |
| ${\color{lightgrey}7}$ | 2024-03-15 | MA | 14 | DD | sample | s14 | - |
| ${\color{lightgrey}7}$ | 2024-03-15 | MA | 14 | DD | sample | s15 | - |

</div>

**Submission B**: sample output_type where a compound modeling task corresponds to a combination of values for origin_date, horizon, and location. In this example, **the proportions of all four variants at a given date, location, and horizon make up the compound modeling task**. In the example data shown below there are two unique compound modeling tasks (shown with the grayed out column) and four samples. 

```
"output_type_id_params":{
			“is_required”: true,
			“type”: “character”,
			“max_length”: 6,
                        "min_samples_per_task": 90,
			"max_samples_per_task": 100,
			"compound_taskid_set": ["origin_date", "location", "horizon"]
		}
```

```{attention}
Once again, rows are grouped so that each unique sample for each modeling task is together. Therefore, the first four rows correspond to the first sample ("s0") for the first modeling task and the second four rows correspond to the second sample ("s1") for the first modeling task..
```

<div class="heatMap2">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | BB | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | CC | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | DD | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | BB | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | CC | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | DD | sample | s1 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | AA | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | BB | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | CC | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | DD | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | AA | sample | s3 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | BB | sample | s3 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | CC | sample | s3 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | DD | sample | s3 | - |

</div>

**Submission C**: sample output_type where each compound modeling task corresponds to a combination of origin_date and location. In this example, there is a single compound modeling task which we can describe as **“Massachusetts with the origin_date of 2024-03-15”**. In the example data shown below there is one unique compound modeling task (shown with the latent grayed out column) and two unique samples. Each sample represents a grouped collection of possible values for all four variants across both prediction horizons.

```
"output_type_id_params":{
			“is_required”: true,
			“type”: “character”,
			“max_length”: 6,
                        "min_samples_per_task": 90,
			"max_samples_per_task": 100,
			"compound_taskid_set": ["origin_date", "location"]
               }
```

<div class="heatMap3">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | BB | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | CC | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | DD | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | BB | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | CC | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | DD | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | BB | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | CC | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | DD | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | AA | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | BB | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | CC | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | DD | sample | s1 | - |

</div>

**Submission D**: sample output_type where a compound modeling task corresponds to a combination of values for origin_date, location and variant. In plain language, this could be described as **“trajectories of proportions over time for a given variant in a given location, with each variant treated independently from each other.”**  In the example data shown below there are four unique compound modeling tasks (shown with the grayed out column) and two samples for each. 

```
"output_type_id_params":{
			“is_required”: true,
			“type”: “character”,
			“max_length”: 6,
                        "min_samples_per_task": 90,
			"max_samples_per_task": 100,
			"compound_taskid_set": ["origin_date", "location", "variant"]
		}
```

<div class="heatMap4">

|compound_idx| origin_date |location | horizon | variant | output_type| output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | AA | sample | s0 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| ${\color{lightgrey}0}$ | 2024-03-15 | MA | 14 | AA | sample | s1 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 7 | BB | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | BB | sample | s2 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 7 | BB | sample | s3 | - |
| ${\color{lightgrey}1}$ | 2024-03-15 | MA | 14 | BB | sample | s3 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 7 | CC | sample | s4 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 14| CC | sample | s4 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 7 | CC | sample | s5 | - |
| ${\color{lightgrey}2}$ | 2024-03-15 | MA | 14 | CC | sample | s5 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 7 | DD | sample | s6 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 14 | DD | sample | s6 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 7 | DD | sample | s7 | - |
| ${\color{lightgrey}3}$ | 2024-03-15 | MA | 14 | DD | sample | s7 | - |

</div>

## Configuration of output_type_id
**The output_type_id column allows a modeler to show which rows of model output belong to the same sample.**

Models may have different internal structures that allow them to naturally generate samples for different compound modeling tasks. 
For example, some models might be able to simulate data from all horizons sequentially, taking into account what has happened at the prior horizons. Such a model would accurately represent their output data as in Submissions C and D. 
Some models might not have this capability, and just be able to simulate draws from each horizon entirely independently of other timepoints. This model would accurately represent their output data as in Submission A or B.

A hub can specify a "compound_taskid_set" field in the metadata for the sample output_type to specify the task-id columns that must be used to define separate sample index values (as present in the output_type_id column). The following table shows how different specifications of this field would impact the validity of each of the example submissions A, B, C, and D. 

<table>
  <tr>
    <td>  </td>
    <td colspan="4"><strong>Submission passing validation</strong></td>
  </tr>
  <tr>
    <td><strong>“compound_taskid_set” in schema"</strong></td>
    <td><strong>A  (o_d,l,h,v)</strong></td>
    <td><strong>B (o_d,l,h)</strong></td>
    <td><strong>C (o_d,l)</strong></td>
    <td><strong>D (o_d,l,v)</strong></td>
  </tr>
  <tr>
    <td>[“origin_date”, “location”, “horizon”, “variant”]</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td>[“origin_date”, “location”, “horizon”]</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
  </tr>
  <tr>
    <td>[“origin_date”, “location”]</td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
  </tr>
  <tr>
    <td>[“origin_date”, “location”, “variant”]</td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
</table>

In general, a submission will pass validation if the task-id variables that define a compound modeling task (as implied by the sample ID values present in the output_type_id column) are also present in the “compound_taskid_set”. To talk through the example of [“origin_date”, “horizon”, “location”]:
- Both Submissions B and C would pass validation since when the data are grouped by the “compound_taskid_set” variables you can always find a group of rows that have the same output_type_id.
- Submissions A and D would fail validation since when the data are grouped by the “compound_taskid_set” variables, there would be no rows that share an output_type_id.
- A hub wants to ensure that samples describe compound modeling tasks corresponding to unique combinations of “origin_date”, “horizon” and “location”. It is acceptable if samples describe “coarser” compound modeling tasks such as units identified by a combination of “origin_date” and “location”. However, it is not acceptable if samples describe “finer” compound modeling tasks corresponding to combinations of “origin_date”, “horizon”, “location”, and “variant”. To achieve this, the hub specifies: <br>
“compound_taskid_set” : [“origin_date”, “horizon”, “location”]

## Number of samples vs. output_type_id
The number of samples per individual modeling task in the above examples can always be determined by the number of times that each unique combination of task-id variables (i.e., each individual modeling task) appears in the submission. For Submissions A, B, C and D above, even though the number of unique values of output_type_id changes, all examples have two samples per individual modeling task since each task-id-set appears exactly twice in the provided data.

## Relationship to output_types
Compound modeling tasks are a general conceptual property of the way targets for a hub are defined. As such, they could be configured for a specific target, for all output types, not just samples. However, at the present time we choose to only implement the concept of compound modeling tasks for sample output_types, to facilitate data format validation for samples. 

At a later time, the hubverse may revisit a way to more generally define compound modeling tasks, as they can be used for different things. For example, compound modeling tasks defined for a compositional data target could

 - validation that all of the proportions in a set of “mean” output_types sum to 1.
 - be used to evaluate the proportions in a set of “mean” output_types, since evaluating each modeling task independently would result in inappropriate duplication of scores for what should be viewed as a single multivariate outcome.

<br>

Documentation about tests for other output types can be found in  [Validation Pull Requests on GitHub](https://hubverse-org.github.io/hubValidations/articles/validate-pr.html#validate_pr-check-details).
