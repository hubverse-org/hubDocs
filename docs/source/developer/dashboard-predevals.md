# Evaluations Dashboard

The [evaluations dashboard](#dashboard-predevals) provides model evaluation scores
for predictions. The interactivity in the dashboard is provided by the [predevals](https://github.com/hubverse-org/predevals) JavaScript module, which reads in a series of static The docker image
[hubPredEvalsData-docker](https://github.com/hubverse-org/hubPredEvalsData-docker)
provides a thin wrapper around the R Package
[hubPredEvalsData](https://hubverse-org.github.io/hubPredEvalsData), which takes
a configuration file and produces a series of hierarchically structured folders
with CSV files that represent **scores disaggregated by target, time period,
and task ID.** The resulting folder structure looks like the one below

```{code-block}
:emphasize-lines: 6-10
:caption: Folder structure for the flu metrocast hub evaluations disaggregated by two targets with two time periods and four task IDs. Note that we are only showing the contents for the first folder. All collapsed folders have identical contents.
.
├── predevals-options.json
└── scores/
    ├── Flu ED visits pct/
    │   ├── Full season/
    │   │   ├── scores.csv
    │   │   ├── horizon/scores.csv
    │   │   ├── location/scores.csv
    │   │   ├── reference_date/scores.csv
    │   │   └── target_end_date/scores.csv
    │   └── Last 4 weeks/[...]
    └── ILI ED visits/
        ├── Full season/[...]
        └── Last 4 weeks/[...]
```

## Installation

You can install the latest version of this tool with docker:

```bash
docker pull ghcr.io/hubverse-org/hub-predevalsdata-docker:main
```

## How the evaluations are built

You need three things in order to build the evaluations

1. a predevals-config.yml file that contains the appropriate disaggregation filters
2. a hub that has forecast data with at least one model and one baseline model
3. oracle output data for that hub

The code below assumes you are starting with a dashboard repository that has
a `predevals-config.yml` file inside of it. We first clone the hub repository
locally and then run the docker container to create the predevals data.

```{code-block} bash
:emphasize-lines: 7-11
git clone <hub-git-url> hub
mkdir -p data/evals

docker run --rm -it --platform=linux/amd64 \
 -v "$(pwd)":"/project" \
 ghcr.io/hubverse-org/hubpredevalsdata-docker:main \
 create-predevals-data.R \
   -h "hub" \
   -c "predevals-config.yml" \
   -d "hub/target-data/oracle-output.csv" \
   -o "data/evals"
```

The more models that exist in the data, the more slowly this operation will run.
For the flusight hub, it currently takes over 20 minutes to run disaggregation
of four time periods over 70 models.

## How the image is built

The image is currently built by a single github workflow that will build and
push a new version to the github container registry every time a push happens on
main.

This will change to the same [build process for the hub-dash-site-builder](#dashboard-site-image-build).

### Updating the dependencies

We package this as a docker image because the process for installing R packages
on GitHub workflows involves several steps and we want this to just work. This
locks our container to a point in time with a specific R version.

This means that with every release of `hubPredEvalsData`, we need to update the
lockfile for the docker image.

To update this image, make sure you have {renv} installed on your machine and
then run `Rscript ./scripts/update.R`. This will update the lockfile and you can
create a pull request for these results.

## Testing

There are unit tests in `hubPredEvalsData`, but no formal tests for the image.

