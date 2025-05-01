# Dashboard Tools

We use a wide range of tools to build the [dashboards](/user-guide/dashboards.md).
Ultimately, the only tools you will need to build a dashboard are git, python,
and docker. Everything else is encapsulated within docker images.

## General tools

[Python]{#dashboard-tool-python}
: Python is the backbone of hub-dashboard-predtimechart and is used in the
  control room to get a list of repositories that have the app installed.

[docker]{#dashboard-tool-docker}
: We use docker to containerize the tools needed to build the website and the
  data for the evaluations.

[BASH]{#dashboard-tool-bash}
: We use BASH to orchestrate building of the dashboard website and within the
  GitHub workflows

[R]{#dashboard-tool-r}
: R is the backbone of hubPredEvalsData, which generates the evaluations dashboard


## Website

The website is orchestrated with the docker image
[hub-dash-site-builder](https://github.com/hubverse-org/hub-dash-site-builder).
The image bundles BASH and [yq](#dashboard-tool-yq) to join the user data with
the template and [quarto](#dashboard-tool-quarto) to render the markdown to HTML.

[[quarto](https://quarto.org)]{#dashboard-tool-quarto}
: This is the website engine. It is responsible for converting markdown to HTML
   and applying styling.

[[yq](https://github.com/mikefarah/yq/#install)]{#dashboard-tool-yq}
: YAML Query. This tool is similar to the command line JSON processor,
  [jq](https://jqlang.org), except it works with YAML. It is responsible for
  joining the dashboard's `site-config.yml` to [`static/_quarto.yml`](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/static/_quarto.yml). The rationale
  behind this is that a user does not have to learn how to use quarto in order
  to generate a site.

## Forecast Visualization

The forecasts visualization is built with [PredTimeChart](https://github.com/reichlab/predtimechart), a JavaScript module that displays forecast visualizations.

The data for PredTimeChart is converted from hub format with
[hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart),
a command-line Python app, which uses the [polars](#dashboard-tool-polars) to
read and convert the data to JSON format.

[[polars](https://pola.rs)]{#dashboard-tool-polars}
: A data manipulation library that provides lazy data frame utilities in Python.
  It gives our tool the ability to read and slice hub data. Eventually, this
  will be subserseded by the hub-data package.

## Evaluations Visualisation

The evaluations visualization is built with [PredEvals](https://github.com/hubverse-org/predevals), a JavaScript module that displays the evaluation visualization. Its code is heavily based off of predtimechart.

The evaluations visualization data are built with the [hubPredEvalsData-docker](https://github.com/hubverse-org/hubPredEvalsData-docker) docker image. This bundles the R package [hubPredEvalsData](#dashboard-tool-hubPredEvalsData), which uses [hubEvals](#dashboard-tool-hubEvals) and [scoringutils](#dashboard-tool-scoringutils) to evaluate model performance if the hub has oracle output available.

[hubPredEvalsData]{#dashboard-tool-hubPredEvalsData}
: generates nested folders of scores disaggregated by task ID

[hubEvals]{#dashboard-tool-hubEvals}
: scores model output

[scoringutils]{#dashboard-tool-scoringutils}
: does some other scoring, IDK



