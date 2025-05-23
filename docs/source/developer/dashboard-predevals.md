# Evaluations dashboard

The evaluations dashboard provides model evaluation scores
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

The base image is the
[rocker/r-ver:4](https://rocker-project.org/images/versioned/r-ver.html) docker
image because it allows us to use binaries from the Posit Package Manager
(P3M), which increases the build time from 30 minutes down to 2 minutes. If a
new major version of R is released, we will switch to use R version 5 after
careful testing.

#### Reproducibility vs production code

Note that we are using the latest major version of R[^versioning]. The version
of R is determined by the version of rocker/r-ver, which follows R releases and
_emphasizes reproducibility_. This is an important point because **the decision
of what tag to use for the base image has downstream impacts on what R packages
are available** (see note below).

The best strategy for choosing the version for the base image is to use
`rocker/r-ver:4`, which specifies that you use the latest non-breaking version
of R, which will always use the latest version of CRAN. If you use a specific
version (e.g. `rocker/r-ver:4.5`), you will be locked in to a snapshot of CRAN
when the next version hits, which can lead to unexpected consequences. For a
table of snapshot dates, you can visit [the Versions
wiki](https://github.com/rocker-org/rocker-versioned2/wiki/Versions).

The R package ecosystem is a bit different than others. Unlike Python where
packages are free to declare any subset of package versions (leading to a
minefield of incompatibilities for any project with more than a few
dependencies), packages in R declare minimum package versions and are expected
to be _forwards compatible_ with its dependencies and the language itself.
However, this is a bit at odds with the concept of reproducibility because you
want to be able to produce the same result with the same data with the same
software.

The problem is that we are not looking for reproducibility because _production
software does not operate in a strict reproducibility context._ Data are
changing all the time and while we expect the software to be internally
correct, we do not expect the exact same result with the same software and
different data. Moreover, we want to be sure to fix any bugs that are latent in
the system, which requires updating the software or even the dependencies. By
using the latest major version release, then we can ensure that we can safely
include updates when needed.

[^versioning]: R itself does not undergo a lot of churn. New minor versions are
    expected to be backwards-compatible and are released every year in April.
    The last time the major version changed was in April 2020 and before that
    was April 2013. Because the gap between changes is longer than an average
    Ph.D. dissertation, it's safe to assume that we can pin a specific major
    version.

:::{admonition} A case study for only pinning the major version of R
:class: info

If you choose a specific minor or patch version of R (e.g. 4.4.2), then once
the next version (4.4.3) is released, you are locked into a snapshot of CRAN
when that 4.4.2 was the latest version (2025-02-27). This can lead to a
situation where a newer version of a package is required, but that version was
released _after_ CRAN released a new version, which would cause a "package not
found" error.

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

#### Updating dependencies after a minor R version update

After a minor R version update, it is important to run `renv::update()` so that
all of the packages and version of R are updated to the latest major version.


## Testing

There are unit tests in `hubPredEvalsData`. There is an integration test in the
github workflow that is built into the build workflow with the following steps:

1. fetch the [flu metrocast hub](https://github.com/reichlab/flu-metrocast)
2. fetch the [predevals-config from the dashboard repo](https://github.com/reichlab/metrocast-dashboard/blob/main/predevals-config.yml)
3. load the latest version of this image and generate data, output into a
   folder called `latest/`
4. load the PR version of this image and generate data, output into a folder
   called `new/`
5. use [`scripts/test.R`](https://github.com/hubverse-org/hubPredEvalsData-docker/blob/main/scripts/test.R) from the container to compare the two outputs. It will
   error if they are not equal.

This is done twice during a pull request and once from the main branch and on
releases. The idea behind the two tests comes from [the dashboard site builder
test strategy](#dashboard-site-image-build). It is a way to balance the need
for security and the need to update tests.

- The first test uses the tests embedded in the current PR
  - allows for updated expectations and more tests to be added
- the second uses the tests from the current release
  - prevents malicious intent by confirming the test suite from the source
    container works as expected.
  - this is allowed to fail if the tests are updated for a valid reason (as in
    this case where there are no tests in the release).

Once the PR is merged, then the tests are considered valid and we no longer need
to run the second iteration.


