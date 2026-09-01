# Software

The hubverse is built as a suite of interoperable, open-source packages that support the common tasks of running a modeling hub: administering hubs, validating and evaluating model outputs, accessing hub data, and building ensembles and visualizations. The packages are written in R, Python, and JavaScript, and because they all rely on the same [data standards](https://hubverse.io/tools/data.html), they work on any hub.

This page groups the packages by language, followed by community tools that work well alongside the hubverse ("friends of the hubverse") and archival data resources. For a comprehensive list of every package, review our [repositories on GitHub](https://github.com/orgs/hubverse-org/repositories).

(software-r)=
## R packages

Most users start here. The [`hubverse`](https://hubverse-org.r-universe.dev/hubverse) meta-package installs and loads the full suite in one step, or you can install any package individually from the [hubverse R-Universe](https://hubverse-org.r-universe.dev/packages).

Install the `hubverse` meta-package from R-Universe:

```r
install.packages("hubverse", repos = c("https://hubverse-org.r-universe.dev", "https://cloud.r-project.org"))
```

Then `library(hubverse)` loads the core packages listed below. Instructions for installing any individual package can be found by following its link in the table.

| Package | Purpose |
| --- | --- |
| [`hubData`](https://hubverse-org.github.io/hubData) | Connect to, access, and manipulate hub model-output and target data. |
| [`hubAdmin`](https://hubverse-org.github.io/hubAdmin) | Create and validate hub configuration files such as `admin.json` and `tasks.json`. |
| [`hubValidations`](https://hubverse-org.github.io/hubValidations) | Validate model-output submissions, typically as pull-request CI checks on a hub. |
| [`hubEnsembles`](https://hubverse-org.github.io/hubEnsembles) | Build ensembles from model outputs, including weighted and quantile averages and linear pools. |
| [`hubEvals`](https://hubverse-org.github.io/hubEvals) | Evaluate and score infectious-disease model outputs. |
| [`hubVis`](https://hubverse-org.github.io/hubVis) | Plot and visualize hub model outputs to synthesize model submissions. |
| [`hubExamples`](https://hubverse-org.github.io/hubExamples) | Example forecasting and scenario-modeling data in the hubverse format. |
| [`hubUtils`](https://hubverse-org.github.io/hubUtils) | Lightweight utility functions shared across hubverse packages. |
| [`hubCI`](https://hubverse-org.github.io/hubCI) | Set up and manage hubverse continuous-integration workflows. |
| [`hubDevs`](https://hubverse-org.github.io/hubDevs) | Utilities for creating and standardizing new hubverse packages. |

(software-python)=
## Python packages

The Python packages support data access and the data pipelines behind hubverse dashboards.

| Package | Purpose |
| --- | --- |
| [`hubdata`](https://pypi.org/project/hubdata/) | Python tools for accessing and working with hubverse hub data ([source](https://github.com/hubverse-org/hub-data)). |
| [`hubverse-transform`](https://github.com/hubverse-org/hubverse-transform) | Transform hubverse model-output files; used in the cloud data pipeline. |

(software-js)=
## JavaScript and dashboard components

These JavaScript components power the interactive [hubverse dashboards](https://hubverse.io/tools/dashboards.html).

| Package | Purpose |
| --- | --- |
| [`predtimechart`](https://github.com/hubverse-org/hub-dashboard-predtimechart) | A predtimechart-based forecast-visualization component for hub dashboards. |
| [`predevals`](https://github.com/hubverse-org/predevals) | A JavaScript module for interactive exploration of forecast evaluations. |

(friends-of-the-hubverse)=
## Friends of the hubverse

Compatible tools from the wider community that work well alongside hubverse packages.

| Tool | Purpose |
| --- | --- |
| [`modelimportance`](https://mkim425.r-universe.dev/modelimportance) | Measures the contribution and importance of individual models within an ensemble. |
| [`alloscore`](https://github.com/aaronger/alloscore) | Scoring methods for allocation and decision problems built on forecasts. |
| [`scoringutils`](https://epiforecasts.io/scoringutils/) | Evaluate and score probabilistic forecasts with a range of proper scoring rules. |
| [`fable`](https://fable.tidyverts.org/) | Tidy time-series forecasting models that integrate with the tidyverts ecosystem. |
| [`EpiBenchmark`](https://accidda.github.io/EpiBenchmark/) | Benchmark and compare epidemic-forecasting models. |

(archival-data-resources)=
## Archival data resources

Several hubs have been reformatted to the hubverse standard and archived so their data remain available for analysis. Browse them, alongside all active hubs, on the [hubverse list of hubs](https://hubverse.io/community/hubs.html).

