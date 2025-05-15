# Evaluations Dashboard

The [evaluations dashboard](#dashboard-predevals) provides model evaluation scores
for predictions. The interactivity in the dashboard is provided by the [predevals](https://github.com/hubverse-org/predevals) JavaScript module, which reads in CSV files and produces a
dashboard interface to view charts and tables summarizing these files.

The docker image
[hubPredEvalsData-docker](https://github.com/hubverse-org/hubPredEvalsData-docker)
provides a thin wrapper around the R Package
[hubPredEvalsData](https://hubverse-org.github.io/hubPredEvalsData), which
takes a configuration file and produces a series of hierarchically structured
folders with CSV files that represent **scores disaggregated by target, time
period, and task ID.** The resulting folder structure looks like the one below

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
docker pull ghcr.io/hubverse-org/hub-predevalsdata-docker:latest
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
 ghcr.io/hubverse-org/hubpredevalsdata-docker:latest \
 create-predevals-data.R \
   -h "hub" \
   -c "predevals-config.yml" \
   -d "hub/target-data/oracle-output.csv" \
   -o "data/evals"
```

**This tool scales poorly with the respect to the number of models.** The more
models that exist in the data, the more slowly this operation will run. For the
flusight hub, it currently takes over 20 minutes to run disaggregation of four
time periods over 70 models.

## How the image is built

This image is built every time a tagged release is created. It process that is
nearly identical to the [build process for the
hub-dash-site-builder](#dashboard-site-image-build).

### Base image

The base image is <https://github.com/hubverse-org/test-docker-hubUtils-dev/>,
which in turn is based on the
[rocker/r-ver](https://rocker-project.org/images/versioned/r-ver.html) docker
images (see
[hubverse-org/hubPredEvalsData-docker#9](https://github.com/hubverse-org/hubPredEvalsData-docker/issues/9)
for future plans).

The version of R is determined by the version of rocker/r-ver, which follows R
releases and _emphasizes reproducibility_. This is an important point because
**the decision of what tag to use for the base image has downstream impacts on
what R packages are available.** The R versions follow semantic versioning rules
and new minor or major versions of R are released every year in April. The best
strategy for choosing the version for the base image is to use `rocker/r-ver:4`,
which specifies that you use the latest non-breaking version of R, which will
always use the latest version of CRAN. If you use a specific version (e.g.
`rocker/r-ver:4.5`), you will be locked in to a snapshot of CRAN when the next
version hits, which can lead to unexpected consequences (see below). For a
table of snapshot dates, you can visit [the Versions
wiki](https://github.com/rocker-org/rocker-versioned2/wiki/Versions).



:::{admonition} A case study for not pinning a specific version of R
:class: info

If you choose a specific minor or patch version of R, then once the next
version is released, you are locked into a snapshot of CRAN when that R was the
latest version. This can lead to a situation where a newer version of a package
is required, but that version was released _after_ CRAN released a new version,
which would cause a "package not found" error.

This was the situation we found ourselves in when implementing this fix
[reichlab/operational-models#29](https://github.com/reichlab/operational-models/pull/29).

:::


### R Packages

The R packages used are dicated by the `renv.lock` file in the repository. This
file was manually generated with a modified [renv workflow](https://docs.posit.co/ide/user/ide/guide/environments/r/renv.html#workflow): `renv::init()` followed by
`renv::install("hubverse-org/hubPredEvalsData")` and `renv::snapshot()`. The
reason for the `renv::install()` step is because renv cannot infer what GitHub
repository `hubPredEvalsData` belongs to.

Because hubPredEvalsData is in a development version, it also brings in the
development versions of these packages:

```
# GitHub ---------------------------------------------------------------------
- hubData            [* -> hubverse-org/hubData]
- hubEvals           [* -> hubverse-org/hubEvals]
- hubPredEvalsData   [* -> hubverse-org/hubPredEvalsData]
- hubUtils           [* -> hubverse-org/hubUtils]
- scoringutils       [* -> epiforecasts/scoringutils]
```


### Updating the R package dependencies

We package this as a docker image because the process for installing R packages
on GitHub workflows involves several steps and we want this to just work. This
locks our container to a point in time with a specific R version.

This means that with every release of `hubPredEvalsData`, we need to update the
lockfile for the docker image.

To update this image, make sure you have {renv} installed on your machine and
then run `Rscript ./scripts/update.R`. This will update the lockfile and you can
create a pull request for these results. An example of a pull request with
these changes can be found in [hubverse-org/hubPredEvalsData-docker#3](https://github.com/hubverse-org/hubPredEvalsData-docker/pull/3).

## Testing

There are unit tests in `hubPredEvalsData`, but no formal tests for the image.
