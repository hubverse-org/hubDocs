# Software

The hubverse is built as a suite of interoperable, open-source packages that support the common tasks of running a modeling hub: administering hubs, validating and evaluating model outputs, accessing hub data, and building ensembles and visualizations. The packages are written in R, Python, and JavaScript, and because they all rely on the same [data standards](https://hubverse.io/tools/data.html), they work on any hub.

This page groups the packages by language, followed by community tools that work well alongside the hubverse ("friends of the hubverse") and archival data resources. For a comprehensive list of every package, review our [repositories on GitHub](https://github.com/orgs/hubverse-org/repositories).

In the tables below, {octicon}`book;1em` links to a package's documentation and {octicon}`mark-github;1em` to its source code.

(software-r)=
## R packages

Since the majority of hubverse users are R users, our suite of R packages is the most well-developed. The [`hubverse`](https://hubverse-org.r-universe.dev/hubverse) meta-package installs and loads the full suite in one step, or you can install any package individually from the [hubverse R-Universe](https://hubverse-org.r-universe.dev/packages).

Install the `hubverse` meta-package from R-Universe:

```r
install.packages("hubverse", repos = c("https://hubverse-org.r-universe.dev", "https://cloud.r-project.org"))
```

Then `library(hubverse)` loads the core packages listed below. Installation instructions for each package are on its documentation site.

| Package | Purpose | Links |
| :--- | :--- | :--- |
| `hubData` | Connect to, access, and manipulate hub model-output and target data. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubData) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubData) |
| `hubAdmin` | Create and validate hub configuration files such as `admin.json` and `tasks.json`. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubAdmin) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubAdmin) |
| `hubValidations` | Validate model-output submissions, typically as pull-request CI checks on a hub. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubValidations) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubValidations) |
| `hubEnsembles` | Build ensembles from model outputs, including weighted ensembles and linear pools. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubEnsembles) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubEnsembles) |
| `hubEvals` | Evaluate and score model outputs. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubEvals) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubEvals) |
| `hubVis` | Plot and visualize hub model outputs to synthesize model submissions. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubVis) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubVis) |
| `hubExamples` | Example forecasting and scenario-modeling data in the hubverse format. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubExamples) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubExamples) |
| `hubUtils` | Lightweight utility functions shared across hubverse packages. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubUtils) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubUtils) |
| `hubCI` | Set up and manage hubverse continuous-integration workflows. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubCI) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubCI) |
| `hubDevs` | Utilities for creating and standardizing new hubverse packages. | [{octicon}`book;1em`](https://hubverse-org.github.io/hubDevs) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubDevs) |

(software-python)=
## Python packages

The Python packages support data access and the data pipelines behind hubverse dashboards.

| Package | Purpose | Links |
| :--- | :--- | :--- |
| `hubdata` | Python tools for accessing and working with hubverse hub data. | [{octicon}`book;1em`](https://hubverse-org.github.io/hub-data/) [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hub-data) |
| `hubverse-transform` | Transform hubverse model-output files; used in the cloud data pipeline. | [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hubverse-transform) |

(software-js)=
## JavaScript and dashboard components

These JavaScript components power the interactive [hubverse dashboards](https://hubverse.io/tools/dashboards.html).

| Package | Purpose | Links |
| :--- | :--- | :--- |
| `predtimechart` | A predtimechart-based forecast-visualization component for hub dashboards. | [{octicon}`mark-github;1em`](https://github.com/hubverse-org/hub-dashboard-predtimechart) |
| `predevals` | A JavaScript module for interactive exploration of forecast evaluations. | [{octicon}`mark-github;1em`](https://github.com/hubverse-org/predevals) |

(friends-of-the-hubverse)=
## Friends of the hubverse

Tools from the wider community that work well alongside hubverse packages.

| Tool | Purpose | Links |
| :--- | :--- | :--- |
| `scoringutils` | Evaluate and score probabilistic forecasts with a range of proper scoring rules. | [{octicon}`book;1em`](https://epiforecasts.io/scoringutils/) [{octicon}`mark-github;1em`](https://github.com/epiforecasts/scoringutils) |
| `alloscore2` | Scoring methods for allocation and decision problems built on forecasts. | [{octicon}`book;1em`](https://reichlab.io/alloscore2/) [{octicon}`mark-github;1em`](https://github.com/reichlab/alloscore2) |
| `modelimportance` | Measures the contribution and importance of individual models within an ensemble. | [{octicon}`book;1em`](https://mkim425.r-universe.dev/modelimportance) [{octicon}`mark-github;1em`](https://github.com/mkim425/modelimportance) |
| `MicroHub` | An R Shiny app to work with hub data locally. | [{octicon}`book;1em`](https://sjfox.github.io/microhub-workshop/) [{octicon}`mark-github;1em`](https://github.com/sjfox/microhub-workshop) |
| `EpiBenchmark` | Benchmark and compare epidemic forecasting models. | [{octicon}`book;1em`](https://accidda.github.io/EpiBenchmark/) [{octicon}`mark-github;1em`](https://github.com/ACCIDDA/EpiBenchmark) |
| `RespiLens` | A responsive web app to explore respiratory disease forecasts in the US. | [{octicon}`book;1em`](https://www.respilens.com/) [{octicon}`mark-github;1em`](https://github.com/ACCIDDA/RespiLens) |

(archival-data-resources)=
## Archival data resources

Several hubs have been reformatted to the hubverse standard and archived so their data remain available for analysis. Browse them, alongside all active hubs, on the [hubverse list of hubs](https://hubverse.io/community/hubs.html#archival-hubs).
