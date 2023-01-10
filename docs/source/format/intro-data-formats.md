# Overview

On this page we provide an [outline on the contents of this data formats section](data-formats-outline), define a few [running examples of Hubs](running-examples), and describe in some detail the key concepts of [task ID variables](task_id_vars) and [submission rounds](submission-rounds).

(data-formats-outline)=
## Data Formats section outline
This section of the documentation provides standards for:

* [Structure of hub repositories](hub-structure): standards for file and directory structures for Hubs
* [Hub configuration files](hub-metadata): the files needed to set up and run a modeling Hub
* [Model metadata](model-metadata): metadata describing models
* [Model output](model-output): standard formats for model output such as forecasts and projections that are saved in Hubs
* [Target data](target-data): standard formats for target data, the eventually observable quantities of interest to a hub
* [Model abstracts](model-abstracts): structure for round-specific detailed narrative descriptions of modeling methods and results

(running-examples)=
## Running examples
In this section we introduce some running examples that will be used to illustrate and motivate the proposed infrastructure, as well as some core concepts that will be used repeatedly in the sections to follow. For each Hub, we identify the task ID variables and output types, both of which are discussed in more detail in [the description of tasks metadata](tasks-metadata).

```{margin}
Note on Example 1 item 2: The US Forecast Hub actually did not specify what type of point forecast should be submitted, but here we are being more specific to illustrate what we think would be a best practice.
```

```{admonition} Example 1: COVID-19 forecasts, adapted from the [US COVID-19 Forecast Hub](https://covid19forecasthub.org/)

This Hub collects forecasts at 1 through 4 weeks ahead of cases, hospitalizations and deaths, at a set of locations. Each forecast is assumed to originate from a specific date.

**Task ID variables**

* `target` (**target key** variable): "cases", "hospitalizations", "deaths"
* `location`: an identifier of a location, e.g., "US"
* `origin_date`: date when a forecast was generated, e.g., "2021-07-11"
* `horizon`: 1, 2, 3, 4 (in units of weeks, which is specified in the target-metadata)

**Output types**

* a set of predictive quantiles at specified probability levels
* a predictive mean

```


```{admonition} Example 2: Influenza hospitalization forecasts in the US 

A hypothetical forecasting exercise for influenza hospitalization rates per 100,000 population by age group at the state level in the US, with short-term incidence and “seasonal” targets.

**Task ID variables**

* `target` (**target key** variable): “weekly rate”, “peak rate”, “peak week”
* `location`: “US”, “AL”, “AK”, …, “WY”
* `age_group`: “0-5 years”, “6-18 years”, …, “65+ years”
* `origin_date`: weekly on Mondays
* `horizon` (only applies if the target is “weekly rate”): 1, 2, NA, NA
```

```{admonition} Example 3: [US COVID-19 Scenario Modeling Hub](https://covid19scenariomodelinghub.org/)
Projections are requested for each combination of the following variables.

**Task ID variables**

* `outcome_variable` (**target key** variable): “hospitalizations”, “cases”, “deaths”
* `outcome_measure` (**target key** variable): “incident count”, “cumulative count”
* `scenario_id`: “low vaccination”
* `location`: “US”
* `origin_date`: 2021-07-11
* `horizon`: 1
```

(task_id_vars)=
## Task ID variables

### Overview of task ID variables
Hubs typically specify that modeling outputs (e.g., forecasts or projections) should be generated for each combination of values across a set of task ID variables. For modeling exercises where the model outputs correspond to estimates or predictions of a quantity that could in principle be calculated from observable data, these task ID variables should be sufficient to uniquely identify an observed value for the modeling target that could be compared to model outputs to evaluate model accuracy. This is discussed more in the section on [target (a.k.a. truth) data](target-data).

Because they are central to Hubs, these task ID variables serve several purposes:
* They are used in the Hub metadata to define modeling tasks of the hub
* They are used in model outputs to identify the modeling task to which forecasts correspond
* They are used in the specification of [target data](target-data) and methods to calculate "ground truth" target data values, to allow for alignment of model outputs with true target values
The relationships between these items are illustrated at a high level in the following diagram; sections to follow provide more detail.

```{figure} img/hub-data-relations.jpeg
---
figclass: margin-caption
alt: A figure showing where data from hubs is created.
name: hub-data-relations
---
The figure shows that Hub metadata and target data are specified by the hub itself, along with any necessary functions to calculate scores or "observed values" from target data. Teams provide model output data that must conform with standards identified in the Hub metadata. 
```

### Usage of task ID variables

Task ID variables can be thought of as columns of a tabular representation in a model output file, where a combination of values of task ID variables would uniquely define a row of data. 

In our running Example 1 above, the task ID variables are `target`, `location`, `origin_date`, and `horizon`. We note that some task ID variables are special in that they conceptually define a modeling "target" (these are referred to in the [tasks metadata](tasks-metadata) as a `target_key`). In this example, `target` is the target key. In other examples, (such as Running Example 3) more than one variable can serve as target keys together.

In general, there are no restrictions on what task ID variables may be named, however when appropriate, we suggest that Hubs adopt the following standard column names and definitions:

* `origin_date`: the starting point that can be used for calculating a target_date via the formula target_date = origin_date + horizon * time_units_per_horizon (e.g., with weekly data, target_date is calculated as origin_date + horizon * 7 days).
* `scenario_id`: a unique identifier for a scenario
* `location`: a unique identifier for a location
* `target`: a unique identifier for the target. It is recommended, although not required, that hubs set up a single variable to define the target (i.e., as a target key), with additional detail specified in the `target_metadata` section of the [tasks metadata](tasks-metadata).
* `target_date`: for short-term forecasts, the target_date specifies the date of occurrence of the outcome of interest. For instance, if models are requested to forecast the number of hospitalizations that will occur on 2022-07-15, the target_date is 2022-07-15.
* `horizon`: The difference between the target_date and the origin_date in time units specified by the hub (e.g., may be days, weeks, or months)
* `age_group`: a unique identifier for an age group

```{note}
We encourage Hubs to avoid redundancy in the model task columns. For example, Hubs should not include all three of `target_date`, `origin_date`, and `horizon` as task ID columns because if any two are specified, the third can be calculated directly. Similarly, if a variable is constant, it should not be included. For example, if a Hub does not include multiple targets, the `target` column could be omitted from the task ID columns.
```

As Hubs define new modeling tasks, they may need to introduce new task ID variables that have not been used before. In those cases, the new variables should be added to this list to ensure that the concepts are documented in a central place and can be reused in future efforts.

(submission-rounds)=
## Submission rounds
Many Hubs will accept model output submissions over multiple rounds. In the case of the forecast hubs there has typically been one submission round per week, while the scenario hubs have had submission rounds less frequently, typically about once per month. As part of the [Hub metadata](hub-metadata), Hubs should specify a set of `round_id` values that uniquely identify the submission round. For instance, for weekly submissions the round id might be the date that submissions are due to the Hub or a specification of an epidemic week. In instances where the rounds do not follow a predetermined schedule, more generic identifiers such as “round1” may be preferred. The round id will be used as the file names of model output submissions and round-specific model abstract submissions, as well as in the Hub metadata to specify model tasks that may vary across rounds.
