# The hubverse: open tools for collaborative modeling

```{admonition} 📣 We have a new landing page!
:class: warning

We have a new landing page at <https://hubverse.io/> that provides a general overview of the hubverse. Over the next few weeks, we will be removing duplicated content from this site.
```

```{admonition} What is the hubverse for?
:class: seealso

**The goal of the hubverse** is to **ensure stakeholders have model summaries they can trust** by facilitating collaborative modeling efforts that are rapidly validated and summarized.
While this effort has been developed by scientists focusing on modeling outbreaks, **hubverse concepts and tooling are general enough to have a broader range of applications**.

Read more about **[who uses the hubverse](overview/who-uses-hubverse.md)**
```

The hubverse is a collection of open-source software and data tools that enable collaborative modeling exercises. It is developed by **the Consortium of Infectious Disease Modeling Hubs**, a collaboration of research teams and public health professionals that have built and maintained predictive modeling hubs for infectious disease applications. Working together, we have developed the hubverse for groups running collaborative modeling hub efforts. This website documents the requirements for using the hubverse.

The [overview section](overview/who-uses-hubverse.md) introduces the project, the [quickstart section](quickstart-hub-admin/intro.md) outlines how to set up and administer a working hub and the [user guide](user-guide/intro-data-formats.md) provides a deeper look at the different standards and resources developed by this project.

## Active Hubs

The following are some of the active and public hubs using the hubverse

:::::: {grid} 1 1 2 2

::: {grid-item-card} US CDC FluSight (2023-2025)

 - [💻 Flu Forecasting Website](https://www.cdc.gov/flu-forecasting/)
 - <https://github.com/cdcepi/FluSight-forecast-hub/#readme>
 - Resource: [📋 Evaluation reports](https://reichlab.io/flusight-eval/)
 - Resource: [📈 Interactive Visualization](https://zoltardata.com/project/360/viz)

:::

::: {grid-item-card} CA DPH West Nile Forecasts

 - <https://github.com/cdphmodeling/wnvca-2024#readme>

:::


::: {grid-item-card} European CDC RespiCast

 - [💻 RespiCast Website](https://respicast.ecdc.europa.eu/)
 - <https://github.com/european-modelling-hubs/flu-forecast-hub#readme>
 - <https://github.com/european-modelling-hubs/ari-forecast-hub#readme>

:::

::: {grid-item-card} European CDC RespiCompass

 - <https://github.com/european-modelling-hubs/RespiCompass#readme>

:::

::::::



```{toctree}
:maxdepth: 2
:caption: Overview
:hidden:
overview/who-uses-hubverse.md
overview/terminology.md
overview/abbreviations.md
overview/data-storage.md
overview/support-consulting.md
overview/cite.md
overview/contact.md
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
user-guide/presentations.md
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

