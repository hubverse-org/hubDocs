# Target data

## Purpose
Many Hubs will focus on modeling tasks where the goal is to estimate or predict a quantity that is in principle observable. In those cases, the Hub should provide:
   * Ground truth data, i.e., "target data", for the variables that are used to define modeling targets, either within the hub itself or with a pointer to an external source providing the data. Critically, this truth data source should be openly accessible and should provide access to historical versions of the data that were available as of past dates.
   * A precise specification of how all modeling targets can be calculated from the ground truth data, ideally with functions implementing those calculations in multiple commonly used programming languages


## Auxiliary data
Optionally, a hub may want to store additional data relevant to the modeling efforts, but not specifically related to the modeling "targets". These data can be stored in the `auxiliary-data` directory of the hub. Examples of data that could be stored in such a directory are:

1. Other data sources that models might want to use as inputs
2. A list of outliers in the target data
3. A list of locations to be used in the hub

## Recommended standards
Any hub for which one or more model output targets are defined in terms of a ground truth data source should provide:
1. access to the truth data in an open and standardized time series format
2. specific instructions on how to calculate the targets from the truth data, including a mathematical specification and functions implementing these calculations in programming languages commonly used for modeling or data analysis in the community served by the Hub.

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
For any modeling Hubs with targets that can be calculated from the truth data, functions should be specified that map time series truth data in the tabular format discussed above to a value of the modeling target for each unique combination of values in the [“task id” columns](task-id-vars). This function should produce data in a tabular format with columns for all task id variables and a value column. These outputs can be consumed by later tools in our pipeline, such as evaluation tools.


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

