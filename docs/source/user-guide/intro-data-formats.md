# Overview

On this page we provide an [outline on the contents of this data formats section](#data-formats-outline), define a few [running examples of Hubs](#running-examples), and describe in some detail the key concepts of [task ID variables](#task-id-vars) and [submission rounds](#submission-rounds).

(data-formats-outline)=
## Data Formats section outline
This section of the documentation provides standards for:

* [Structure of hub repositories](#hub-structure): standards for file and directory structures for Hubs
* [Hub configuration files](#hub-config): the files needed to set up and run a modeling Hub
* [Model metadata](#model-metadata): metadata describing models
* [Model output](#model-output): standard formats for model output such as forecasts and projections that are saved in Hubs
* [Target data](#target-data): standard formats for target data, the eventually observable quantities of interest to a hub
* [Model abstracts](#model-abstracts): structure for round-specific detailed narrative descriptions of modeling methods and results

(running-examples)=
## Running examples
In this section we introduce some running examples that will be used to illustrate and motivate the proposed infrastructure, as well as some core concepts that will be used repeatedly in the sections to follow. For each Hub, we identify the task ID variables and output types, both of which are discussed in more detail in [the description of tasks metadata](#tasks-metadata).


(running-example-1)=
```{admonition} Example 1: A simple forecast hub

This example is adapted from [COVID-19 hospitalization forecasts submitted to the US COVID-19 Forecast Hub](https://github.com/reichlab/covid19-forecast-hub) to provide examples of nowcasts.  Additionally, we note that the description below was written to mirror the technical set-up of the [simple forecast hub example repository](https://github.com/hubverse-org/example-simple-forecast-hub). The following specifications can be determined from [the tasks.json configuration file for this Hub](https://github.com/hubverse-org/example-simple-forecast-hub/blob/main/hub-config/tasks.json). 

This Hub allows for submissions on a pre-specified set of dates specified by the `origin_date` task ID variable. **Each `origin_date` corresponds to a separate modeling round.** In each round, the submissions follow the same format. **There is a single target, called `inc covid hosp`** which, in English, translates to **"weekly incident COVID-19 hospitalizations"** for that day. Mean point forecasts are provided at the state and territory level in the US.  

#### Task ID variables

* `target`{.codeitem} (the sole **target key** variable[^target-key]): can only take the value "inc covid hosp" 
* `location`{.codeitem}: “US”, “01”, “02”, …, “78” ([FIPS codes for US states and territories](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standards))
* `origin_date`{.codeitem} (this variable is specified as the one from which rounds are given IDs): nowcast date
```

[^target-key]: Since the target in the simple forecast hub is defined by a
    single task_id variable (`target`) which only takes one value (`inc covid
    hosp`), the hub maintainers could have opted to not include any
    `target_key` variable to save space in the file. For example, in CSV
    submission files, row will have the same value in the `target` column, so
    this information is redundant.


(running-example-2)=
```{admonition} Example 2: COVID-19 forecasts, adapted from the [US COVID-19 Forecast Hub](https://covid19forecasthub.org/)

This Hub collects forecasts at 1 through 4 weeks ahead of cases, hospitalizations and deaths, at a set of locations. Each forecast is assumed to originate from a specific date.

#### Task ID variables

* `target`{.codeitem} (**target key** variable): "cases", "hospitalizations", "deaths"
* `location`{.codeitem}: an identifier of a location, e.g., "US"
* `origin_date`{.codeitem}: date when a forecast was generated, e.g., "2021-07-11"
* `horizon`{.codeitem}: 1, 2, 3, 4 (in units of weeks, which is specified in the target-metadata)

#### Output Types

* a set of predictive quantiles at specified probability levels
* a predictive mean[^predictive-dist]

```

[^predictive-dist]: The US COVID-19 Forecast Hub actually did not specify what type of point forecast should be submitted, but here we are being more specific to illustrate what we think would be a best practice.


(running-example-3)=
```{admonition} Example 3: Multiple target keys
Projections are requested for each combination of the following variables.

#### Task ID variables

* `outcome_variable`{.codeitem} (**target key** variable): “hospitalizations”, “cases”, “deaths”
* `outcome_measure`{.codeitem} (**target key** variable): “incident count”, “cumulative count”
* `scenario_id`{.codeitem}: “low vaccination”
* `location`{.codeitem}: “US”
* `origin_date`{.codeitem}: 2021-07-11
* `horizon`{.codeitem}: 1
```

(submission-rounds)=
## Submission rounds
Many Hubs will accept model output submissions over multiple rounds. In the case of the forecast hubs there has typically been one submission round per week, while the scenario hubs have had submission rounds less frequently, typically about once per month. As part of the [Hub configuration files](#hub-config), Hubs should specify a set of `round_id` values that uniquely identify the submission round. For instance, for weekly submissions the round id might be the date that submissions are due to the Hub or a specification of an epidemic week. In instances where the rounds do not follow a predetermined schedule, more generic identifiers such as “round1” may be preferred. The round id will be used as the file names of model output submissions and round-specific model abstract submissions, as well as in the Hub metadata to specify model tasks that may vary across rounds.
