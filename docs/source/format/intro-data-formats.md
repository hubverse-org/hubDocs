# Overview

This section of the documentation provides standards for:

* Structure of hub repositories: the organization of hub data and key functionality into a collection of standard packages
* Model outputs: standard formats for model outputs such as forecasts and projections that are saved in hubs
* Model metadata: Format of metadata describing models
* Hub specification: Format of metadata defining hub targets, validations, etc.
* Json encoding of model outputs
* Versioning of data formats for all of the above items


## Context and concepts

In this section we introduce some running examples that will be used to illustrate and motivate the proposed infrastructure, as well as some core concepts that will be used repeatedly in the sections to follow.

## Running examples
To ground the ideas below, we present a few examples of hypothetical modeling hubs, adapted from some of the hubs participating in the Outbreak Hub Consortium.


```{margin}
Note on Example 1 item 2: The US Forecast Hub actually did not specify what type of point forecast should be submitted, but here we are being more specific to illustrate what we think would be a best practice.
```

```{admonition} Example 1: COVID-19 forecasts, adapted from the [US COVID-19 Forecast Hub](https://covid19forecasthub.org/)
1. The US COVID-19 Forecast Hub solicits predictions corresponding to combinations of the following variables
    * outcome_variable: “cases”, “hospitalizations”, “deaths”
    * location: an identifier of a location, e.g., “US”
    * origin_date: date when a forecast was generated (defined more concretely below), e.g., 2021-07-11
    * horizon: 1
2. Multiple prediction types can be submitted:
    * a set of predictive quantiles at specified probability levels
    * a predictive mean
```



```{admonition} Example 2: A hypothetical forecasting exercise for influenza hospitalization rates per 100,000 population by age group at the state level in the US, with short-term incidence and “seasonal” targets.
1. Forecasts are requested for each combination of the following variables:
    * location: “US”, “AL”, “AK”, …, “WY”
    * age_group: “0-5 years”, “6-18 years”, …, “65+ years”
    * origin_date: weekly on Mondays
    * outcome_variable: “hospitalizations”
        * target[d]: “weekly rate”, “weekly rate”, “peak rate”, “peak week”
        * horizon (only applies if the target is “weekly rate”): 1, 2, NA, NA
```

```{admonition} Example 3: [US COVID-19 Scenario Modeling Hub](https://covid19scenariomodelinghub.org/)
1. Projections are requested for each combination of the following variables:
    * scenario_id: “low vaccination”
    * location: “US”
    * origin_date: 2021-07-11
    * outcome_variable: “hospitalizations”, “cases”, “deaths”
    * target: “incident count”, “cumulative count”
    * horizon: 1
```

## Task ID variables
As illustrated here, Hubs typically specify that modeling outputs (e.g., forecasts or projections) should be generated for each combination of values across a set of “task id” variables. For modeling exercises where the model outputs correspond to estimates or predictions of a quantity that could in principle be calculated from observable data, these task id variables should be sufficient to uniquely identify an observed value for the modeling target that could be compared to model outputs to evaluate model accuracy. This is discussed more in the section on truth data below.


Because they are central to Hubs, these task id variables will appear in several of the following subsections:
* They are used in the Hub metadata to define modeling tasks of the hub
* They are used in model outputs to identify the modeling task to which forecasts correspond
* They are used in the specification of truth data and methods to calculate ground truth target values, to allow for alignment of model outputs with true target values
The relationships between these items is illustrated at a high level in the following diagram; sections to follow provide more detail.

```{figure} img/hub-data-relations.jpeg
---
figclass: margin-caption
alt: A figure showing where data from hubs is created.
name: hub-data-relations
---
The figure shows that Hub metadata and truth data are specified by the hub itself, along with any necessary functions to calculate scores or "observed values" of targets from truth data. Teams provide model output data that must conform with standards identified in the Hub metadata. 
```

When appropriate, we suggest that Hubs adopt the following standard column names and definitions:

* `outcome_variable`: the name of the variable that is used to calculate the value of the forecast target. Hubs are encouraged to be specific about the unit of measurement for the outcome variable.
   1. Example: for the target “1 week ahead cumulative deaths”, the outcome variable is “deaths”
   2. Example: For the target “season peak incident cases”, the outcome variable is “cases”
* `outcome_modifier`: a description of a preliminary adjustment that’s made to the outcome variable
   1. Example: for the target “1 week ahead cumulative deaths”, the modifier is “cumulative”
   2. Example: for the target “1 week ahead incident deaths”, the modifier is “incident”
   3. Example: for the target “1 week ahead hospitalization rate”, the modifier is “rate” (per 100,000 population)
* `target_date`: for short-term forecasts, the target_date specifies the date of occurrence of the outcome of interest. For instance, if models are requested to forecast the number of hospitalizations that will occur on 2022-07-15, the target_date is 2022-07-15.
* `origin_date`: the starting point that can be used for calculating a target_date via the formula target_date = origin_date + horizon * time_units_per_horizon (e.g., with weekly data, target_date is calculated as origin_date + horizon * 7 days).
* `horizon`: The difference between the target_date and the origin_date in time units specified by the hub (e.g., may be days, weeks, or months)
* `location`: a unique identifier for a location
* `age_group`: a unique identifier for an age group
* `scenario`: a unique identifier for a scenario


```{note}
We encourage hubs to avoid redundancy in the model task columns. For example, Hubs should not include all three of `target_date`, `origin_date`, and `horizon` as task id columns because if any two are specified, the third can be calculated directly. Similarly, if a variable is constant, it should not be included. For example, if a Hub doesn’t include multiple outcome variables, an outcome variable should not be included among the task id columns.
```

As Hubs define new modeling tasks, they may need to introduce new task id variables that have not been used before. In those cases, the new variables should be added to this list to ensure that the concepts are documented in a central place and can be reused in future efforts.


## Submission rounds
Many Hubs will accept model output submissions over multiple rounds. In the case of the forecast hubs there has typically been one submission round per week, while the scenario hubs have had submission rounds less frequently, typically about once per month. As part of the Hub metadata described below, Hubs should specify a set of ‘round id’ values that uniquely identify the submission round. For instance, for weekly submissions the round id might be the date that submissions are due to the Hub or a specification of an epidemic week. In instances where the rounds do not follow a predetermined schedule, more generic identifiers such as “round1” may be preferred. The round id will be used as the file names of model output submissions and round-specific model abstract submissions, as well as in the Hub metadata to specify model tasks that may vary across rounds.
