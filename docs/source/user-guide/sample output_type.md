# Sample output_type

## Introduction
The sample output_type can be used to represent a probabilistic distribution through a collection of possible future observed values (“samples”) that come out of a predictive model. Depending on the setup of the model and the configuration settings of the hub, different information may be requested or required to identify each sample.

In the hubverse, a “modeling task” is the element that is being predicted and that can be represented by a univariate (e.g., scalar, or single) value. We could also tie this to a tabular representation of data more concretely as a combination of values from a set of task id columns that uniquely define a single prediction. We note that this concept is similar to that of a [“forecast unit” in the scoringutils R package](https://epiforecasts.io/scoringutils/reference/set_forecast_unit.html).

Take the following model_output data for the mean output_type as an example:
| Origin_date | horizon | location | output_type| Output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | -1 | MA | mean | NA| - |
| 2024-03-15 |  0 | MA | mean | NA| - |
| 2024-03-15 |  1 | MA | mean | NA| - |

In the above table, the three task-id columns origin_date, horizon, and location uniquely define a modeling task. Here, there are three modeling tasks, represented by the tuples
{origin_date: “2024-03-15”, horizon: “-1”, location: “MA”}
{origin_date: “2024-03-15”, horizon: “0”, location: “MA”}
{origin_date: “2024-03-15”, horizon: “1”, location: “MA”}

In words, the first of these tuples represents a forecast for one day (assume here the horizon is on the timescale of day) prior to the origin date of 2024-03-15 in Massachusetts. 

## Individual modeling tasks
In many settings, forecasts will be made for individual modeling tasks, with no notion of modeling tasks being related to each other or collected into sets (for more on this, see Compound modeling tasks). In the situations where forecasts are assumed to be made for individual modeling tasks, every modeling task is treated as distinct, as is implied by the compound_idx column in the table below (grayed out to indicate that such a column exists implicitly in the dataset and is not typically present in the actual tabular data). In this setting, the output_type_id column indexes the samples that exist for each modeling task.

|compound_idx| Origin_date | horizon | location | output_type| Output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| $${\color{lightgrey}1}$$ | 2024-03-15 | -1 | MA | sample | 0| - |
| $${\color{lightgrey}1}$$ | 2024-03-15 | -1 | MA | sample | 1| - |
| $${\color{lightgrey}1}$$ | 2024-03-15 | -1 | MA | sample | 2| - |
| $${\color{lightgrey}2}$$ | 2024-03-15 | 0 | MA | sample | 3| - |
| $${\color{lightgrey}2}$$ | 2024-03-15 | 0 | MA | sample | 4| - |
| $${\color{lightgrey}2}$$ | 2024-03-15 | 0 | MA | sample | 5| - |
| $${\color{lightgrey}3}$$ | 2024-03-15 | 1 | MA | sample | 6| - |
| $${\color{lightgrey}3}$$ | 2024-03-15 | 1 | MA | sample | 7| - |
| $${\color{lightgrey}3}$$ | 2024-03-15 | 1 | MA | sample | 8| - |

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

In words, the above configuration specifies that samples are required, they must be integers, and there must be exactly (i.e., no more or less than) 100 samples per modeling task.

Note that the output_type_id parameters are specified in an “output_type_id_params” block because they are parameters defining the allowable values. For other output types, the “output_type_id” block is used to explicitly list required and optional values.

## Compound modeling tasks

There are settings where modeling hubs may wish to identify sets of modeling tasks that the hub will treat as being related to each other. This occurs when multiple distinct values that can be seen as being representations of a single multivariate outcome of interest. In these settings, a subset of the task-id columns (a “compound_taskid_set”) will be used to identify what values are shared for the modeling tasks that are related to each other.

As a running example of how compound modeling tasks could be specified in different ways, we will look at a hub reporting on variant proportions observed at a given location and at a given time. In the table below, a single modeling task is a unique combination of values from the task-id variables origin_date, horizon, variant, and location.  In the table below, one set of four rows with the same values in the origin_date, horizon, and location columns but different variant values below represent four predicted variant proportions. 

Base data: mean output_type. In the table below, an entry of “-” stands in for specific values to be provided by the submitter.

| Origin_date | horizon | variant |location | output_type| Output_type_id | value |
|:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| 2024-03-15 | 7 | AA | MA | sample | - | - |
| 2024-03-15 | 7 | BB | MA | sample | - | - |
| 2024-03-15 | 7 | CC | MA | sample | - | - |
| 2024-03-15 | 7 | DD | MA | sample | - | - |
| 2024-03-15 | 14 | AA | MA | sample | - | - |
| 2024-03-15 | 14 | BB | MA | sample | - | - |
| 2024-03-15 | 14 | CC | MA | sample | - | - |
| 2024-03-15 | 14 | DD | MA | sample | - | - |

### Three submissions, differing by compound modeling task
Submission A: sample output_type where **a single modeling task corresponds to a unique combination of origin_date, location, horizon, and variant**. There are eight unique modeling tasks in this example.

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

|compound_idx| Origin_date |location | horizon | variant | output_type| Output_type_id | value |
|:----------: |:----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| $${\color{lightgrey}0}$$ | 2024-03-15 | MA | 7 | AA | sample | s0 | - |
| $${\color{lightgrey}0}$$ | 2024-03-15 | MA | 7 | AA | sample | s1 | - |
| $${\color{lightgrey}1}$$ | 2024-03-15 | MA | 7 | BB | sample | s2 | - |
| $${\color{lightgrey}1}$$ | 2024-03-15 | MA | 7 | BB | sample | s3 | - |
| $${\color{lightgrey}2}$$ | 2024-03-15 | MA | 7 | CC | sample | s4 | - |
| $${\color{lightgrey}2}$$ | 2024-03-15 | MA | 7 | CC | sample | s5 | - |
| $${\color{lightgrey}3}$$ | 2024-03-15 | MA | 7 | DD | sample | s6 | - |
| $${\color{lightgrey}3}$$ | 2024-03-15 | MA | 7 | DD | sample | s7 | - |
| $${\color{lightgrey}4}$$ | 2024-03-15 | MA | 14 | AA | sample | s8 | - |
| $${\color{lightgrey}4}$$ | 2024-03-15 | MA | 14 | AA | sample | s9 | - |
| $${\color{lightgrey}5}$$ | 2024-03-15 | MA | 14 | BB | sample | s10 | - |
| $${\color{lightgrey}5}$$ | 2024-03-15 | MA | 14 | BB | sample | s11 | - |
| $${\color{lightgrey}6}$$ | 2024-03-15 | MA | 14 | CC | sample | s12 | - |
| $${\color{lightgrey}6}$$ | 2024-03-15 | MA | 14 | CC | sample | s13 | - |
| $${\color{lightgrey}7}$$ | 2024-03-15 | MA | 14 | DD | sample | s14 | - |
| $${\color{lightgrey}7}$$ | 2024-03-15 | MA | 14 | DD | sample | s15 | - |


