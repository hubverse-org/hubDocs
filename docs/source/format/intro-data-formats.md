# Overview

This working group is charged with specifying standards for:
* Structure of hub repositories: the organization of hub data and key functionality into a collection of standard packages
* Model outputs: standard formats for model outputs such as forecasts and projections that are saved in hubs
* Model metadata: Format of metadata describing models
* Hub specification: Format of metadata defining hub targets, validations, etc.
* Json encoding of model outputs
* Versioning of data formats for all of the above items


For now, this document is organized into sections for each of these topics, with a subsection for the recommended standard that we arrive at and a subsection for current practices in the hubs collaborating on this work.

## Context and concepts

In this section we introduce some running examples that will be used to illustrate and motivate the proposed infrastructure, as well as some core concepts that will be used repeatedly in the sections to follow.

## Running examples
To ground the ideas below, we present a few examples of hypothetical modeling hubs, adapted from some of the hubs participating in the Outbreak Hub Consortium.


* Example 1:  COVID-19 forecasts, adapted from the US COVID-19 Forecast Hub
   1. The US COVID-19 Forecast Hub solicits predictions corresponding to combinations of the following variables
      * outcome_variable: “cases”, “hospitalizations”, “deaths”
      * location: an identifier of a location, e.g., “US”
      * origin_date: date when a forecast was generated (defined more concretely below), e.g., 2021-07-11
      * horizon: 1
   2. Multiple prediction types can be submitted:
      * a set of predictive quantiles at specified probability levels
      * a predictive mean[c]
* Example 2: A hypothetical forecasting exercise for influenza hospitalization rates per 100,000 population by age group at the state level in the US, with short-term incidence and “seasonal” targets.
   1. Forecasts are requested for each combination of the following variables:
* location: “US”, “AL”, “AK”, …, “WY”
* age_group: “0-5 years”, “6-18 years”, …, “65+ years”
* origin_date: weekly on Mondays
* outcome_variable: “hospitalizations”
      * target[d]: “weekly rate”, “weekly rate”, “peak rate”, “peak week”
      * horizon (only applies if the target is “weekly rate”): 1, 2, NA, NA
* Example 3: scenario hub
   1. Projections are requested for each combination of the following variables:
      * scenario_id: “low vaccination”
      * location: “US”
      * origin_date: 2021-07-11
      * outcome_variable: “hospitalizations”, “cases”, “deaths”
      * target: “incident count”, “cumulative count”
      * horizon: 1


## Task ID variables
As illustrated here, Hubs typically specify that modeling outputs (e.g., forecasts or projections) should be generated for each combination of values across a set of “task id” variables. For modeling exercises where the model outputs correspond to estimates or predictions of a quantity that could in principle be calculated from observable data, these task id variables should be sufficient to uniquely identify an observed value for the modeling target that could be compared to model outputs to evaluate model accuracy. This is discussed more in the section on truth data below.


Because they are central to Hubs, these task id variables will appear in several of the following subsections:
* They are used in the Hub metadata to define modeling tasks of the hub
* They are used in model outputs to identify the modeling task to which forecasts correspond
* They are used in the specification of truth data and methods to calculate ground truth target values, to allow for alignment of model outputs with true target values
The relationships between these items is illustrated at a high level in the following diagram; sections to follow provide more detail.
