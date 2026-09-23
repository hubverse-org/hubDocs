# The hubverse: open tools for collaborative modeling

```{admonition} Looking for a broad overview of the hubverse?
Visit <https://hubverse.io/> for a general introduction to the hubverse. This site provides detailed technical documentation on how to use it.
```

```{admonition} What is the hubverse for?
:class: seealso

**The goal of the hubverse** is to **ensure stakeholders have model summaries they can trust** by facilitating collaborative modeling efforts that are rapidly validated and summarized.
While this effort has been developed by scientists focusing on modeling outbreaks, **hubverse concepts and tooling are general enough to have a broader range of applications**.

Read more about **[who uses the hubverse](overview/who-uses-hubverse.md)**
```

The hubverse is a collection of open-source software and data tools that enable collaborative modeling exercises. It is developed by **the Consortium of Infectious Disease Modeling Hubs**, a collaboration of research teams and public health professionals that have built and maintained predictive modeling hubs for infectious disease applications. Working together, we have developed the hubverse for groups running collaborative modeling hub efforts. This website documents the requirements for using the hubverse.

The [overview section](overview/who-uses-hubverse.md) introduces the project, the [quickstart section](quickstart-hub-admin/intro.md) outlines how to set up and administer a working hub and the [user guide](user-guide/intro-data-formats.md) provides a deeper look at the different standards and resources developed by this project.

## Active hubs

Many public hubs are built on the hubverse. A few examples are shown below.

```{seealso}
**[Browse the full list of hubs on hubverse.io →](https://hubverse.io/community/hubs.html)**
```

<!-- The canonical list of hubs lives in the hubverse-site repo
     (hubverse-site/_data/active-hubs.qmd, rendered at
     https://hubverse.io/community/hubs.html). The cards below are a small,
     hand-picked set of examples. -->

:::::: {grid} 1 1 2 2

::: {grid-item-card} US CDC FluSight Forecast Hub

 - <https://github.com/cdcepi/FluSight-forecast-hub#readme>
 - [📈 Forecasts](https://reichlab.io/flusight-dashboard/forecast.html)
 - [📋 Evaluations](https://reichlab.io/flusight-dashboard/eval.html)

:::

::: {grid-item-card} European CDC RespiCast

 - [💻 RespiCast Website](https://respicast.ecdc.europa.eu/)
 - <https://github.com/european-modelling-hubs/RespiCast-SyndromicIndicators#readme>

:::

::: {grid-item-card} RSV Scenario Modeling Hub

 - [💻 Scenario Modeling Hub Website](https://rsvscenariomodelinghub.org)
 - <https://github.com/midas-network/rsv-scenario-modeling-hub#readme>

:::

::: {grid-item-card} Variant Nowcast Hub

 - <https://github.com/reichlab/variant-nowcast-hub#readme>
 - [🔎 Explore](https://reichlab.io/variant-nowcast-hub-dashboard/explore.html)
 - [📋 Evaluations](https://reichlab.io/variant-nowcast-hub-dashboard/eval.html)

:::

::: {grid-item-card} RVDSS Forecast Hub

 - <https://github.com/ai4castinghub/rvdss-forecast#readme>
 - [📈 Forecasts](https://4castinghub.uoguelph.ca/respiratory-virus-detections/)

:::

::: {grid-item-card} GZlab China COVID-19 Forecast Hub

 - <https://github.com/dailypartita/China-COVID-19-Forecast-Hub#readme>
 - [📈 Forecasts](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/forecast.html)
 - [📋 Evaluations](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/eval.html)

:::

::: {grid-item-card} CA DPH West Nile Virus Forecasting Hub

 - <https://github.com/cdphmodeling/wnvca-2024#readme>

:::

::: {grid-item-card} BVBD Modeling Hub

 - <https://github.com/InsightNet-US/BDBV-Modeling-Hub#readme>

:::

::: {grid-item-card} MetroCast Sandbox

 - <https://github.com/reichlab/metrocast-sandbox-2025-2026#readme>

:::

::: {grid-item-card} SISMID ILI Forecasting Sandbox

 - <https://github.com/reichlab/sismid-ili-forecasting-sandbox#readme>

:::

::: {grid-item-card} Archival COVID-19 Forecast Hub (2020-2024)

 - <https://github.com/hubverse-org/covid19-forecast-hub-archive#readme>

:::

::: {grid-item-card} DMA-PRIME Human-AI Teaming Sandbox

 - <https://github.com/bleicham/Human-AI-Forecasting-Challenge-Sandbox#readme>
 - [📈 Forecasts](https://bleicham.github.io/Human-AI-Teaming-Challenge-Sandbox-Dashboard/forecast.html)
 - [📋 Evaluations](https://bleicham.github.io/Human-AI-Teaming-Challenge-Sandbox-Dashboard/eval.html)

:::

::::::



```{toctree}
:maxdepth: 2
:caption: Overview
:hidden:
overview/who-uses-hubverse.md
overview/terminology.md
overview/abbreviations.md
overview/contact.md
overview/cite.md
```

```{toctree}
:maxdepth: 2
:caption: Quickstart - hub administration
:hidden:
quickstart-hub-admin/intro.md
quickstart-hub-admin/getting-started.md
quickstart-hub-admin/setting-up.md
quickstart-hub-admin/tasks-config.md
quickstart-hub-admin/scripting-task-config.md
quickstart-hub-admin/model-metadata-schema.md
quickstart-hub-admin/uploading-validating.md
quickstart-hub-admin/continuous-integration.md
quickstart-hub-admin/using-hub.md
```

```{toctree}
:maxdepth: 2
:caption: User Guide
:hidden:
user-guide/intro-data-formats.md
user-guide/data-storage.md
user-guide/hub-structure.md
user-guide/hub-config.md
user-guide/tasks.md
user-guide/model-metadata.md
user-guide/model-output.md
user-guide/sample-output-type.md
user-guide/target-data.md
user-guide/model-abstracts.md
user-guide/dashboards.md
user-guide/software.md
```

```{toctree}
:maxdepth: 2
:caption: Developer Guide
:hidden:
developer/index.md
developer/release-process.md
developer/hotfix.md
developer/r.md
developer/python.md
developer/security.md
developer/cloud-onboarding.md
developer/dashboard-tools.md
developer/dashboard-local.md
developer/dashboard-site.md
developer/dashboard-predtimechart.md
developer/dashboard-predevals.md
developer/dashboard-workflows.md
developer/dashboard-staging.md
```

```{toctree}
:maxdepth: 2
:caption: Code of Conduct
:hidden:
coc/covenant.md
coc/enforcement-manual.md
coc/committee.md
```

