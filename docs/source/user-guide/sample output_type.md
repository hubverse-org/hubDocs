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


### Time series truth data
Access to truth data could take any of the following forms; appropriate mechanisms may differ for different hubs depending on the modeling goals and available systems for data access:
* storing the data within the hub
* setting up a separate github repository that contains truth data
* linking to another resource like covidcast that provides an API for access to truth data


In any of these cases, the data should be provided in a time series format with the following columns:
* **Time index**: a column identifying the time of occurrence of an event
   * Example: For a modeling exercise focusing on daily hospitalizations, the time index may specify the date of admission to the hospital.
   * Example: For an influenza forecasting challenge focusing on weekly confirmed influenza cases, the time index may specify the value of the epidemic week during which a patient tested positive for influenza.
* **Keys**: zero or more columns that, taken together, identify strata for analysis.
   * Example: For a scenario modeling Hub where models are asked to provide projections stratified by task id variables location and age_group, the truth data should contain columns named “location” and “age_group”
* **Outcome variables**: One or more columns specifying values of outcome variables.
   * Example: For a Hub in which modelers forecast cases, deaths, and hospitalizations, the truth data should contain columns named “cases”, “deaths”, and “hospitalizations”


To allow for reproducible analyses in the event of revisions to previously reported data, any system for accessing ground truth data should provide functionality for accessing the data as they were at past points in time.


## Calculating modeling targets
For any modeling Hubs with targets that can be calculated from the truth data, functions should be specified that map time series truth data in the tabular format discussed above to a value of the modeling target for each unique combination of values in the [“task id” columns](task_id_vars). This function should produce data in a tabular format with columns for all task id variables and a value column. These outputs can be consumed by later tools in our pipeline, such as evaluation tools.


We illustrate with our second running example: a hypothetical forecasting exercise for influenza hospitalization rates per 100,000 population by age group at the state level in the US, with short-term incidence and “seasonal” targets. Forecasts are requested for each combination of the following variables:
* location: “US”, “AL”, “AK”, ..., “WY”
* age_group: “0-5 years”, “6-18 years”, ..., “65+ years”
* origin_date: weekly on Mondays
* outcome_variable: “hospitalizations”
* target: “weekly rate”, “weekly rate”, “peak rate”, “peak week”
* horizon (only applies if the target is “weekly rate”): 1, 2, NA, NA

Suppose that $y_{l,a,d}$ represents the hospitalization rate for location $l$ and age group $a$ on the week corresponding to date $d$. Additionally, let $season(d)$ denote the influenza season to which the date $d$ belongs. For a forecast submitted on `origin_date` $d$, the following table specifies how the observed target values can be calculated from known ground truth data:

| Target/horizon combination | Target value |
| ----------- | ----------- |
| Target: “weekly rate”, Horizon: 1 | $y_{l,a,d+1}$ |
| Target: “weekly rate”, Horizon: 2 | $y_{l,a,d+2}$ |
| Target: “peak rate”, Horizon: NA | $max_{\{d':season(d') = season(d) \}} y_{l,a,d'}$ |
| Target: “peak week”, Horizon: NA | $argmax_{\{d':season(d') = season(d) \}} y_{l,a,d'}$ | 
	

A Hub should additionally provide a function that calculates the value of these targets from input ground truth data, ideally in multiple programming languages that are commonly used by modelers.

