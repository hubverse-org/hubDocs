# Modeling Hub documentation

```{caution}
This project is under active development.
```

**The Consortium of Infectious Disease Modeling Hubs** is a collaboration of research teams that have built and maintained predictive modeling hubs for infectious disease applications. Working together, we have developed software for groups that are running collaborative modeling hub efforts. This website documents the requirements for using the infrastructure that the Consortium has set up.  

The following sections of this page provide an outline of the different resources created by this project.

## Tools for building and hosting modeling hubs

The following subsections provide pointers to resources developed by the Consortium to make designing, launching, and maintaining hubs easier.

### Template hubs

The [template hub repositories](https://github.com/Infectious-Disease-Modeling-Hubs?q=&type=template&language=&sort=) provided by the consortium may be cloned directly to start a new hub. Unlike the example hubs below, these repositories do not have any data in them, they just provide a skeletal structure of a hub. Currently, we only host a single [template hub](https://github.com/Infectious-Disease-Modeling-Hubs/hubTemplate).

### Example hubs

We have created some [example Hub repositories](https://github.com/Infectious-Disease-Modeling-Hubs?q=example&type=all&language=&sort=) that provide minimal working examples of hubs. These repositories could be used for ideas of how to set up configuration files for new projects. They are also used as use-cases for testing the software described below.

- The [Simple Forecast Hub Example](https://github.com/Infectious-Disease-Modeling-Hubs/example-simple-forecast-hub) is designed to be similar to the [US CDC FluSight Hospitalization Forecasting exercise](https://github.com/cdcepi/Flusight-forecast-data) from 2022-2023.
- The [Complex Forecast Hub Example](https://github.com/Infectious-Disease-Modeling-Hubs/example-complex-forecast-hub) is designed to be similar to the [US COVID-19 Forecast Hub](https://github.com/reichlab/covid19-forecast-hub) and the [European COVID-19 Forecast Hub](https://github.com/covid19-forecast-hub-europe/covid19-forecast-hub-europe).
- The [Complex Scenario Hub Example](https://github.com/Infectious-Disease-Modeling-Hubs/example-complex-scenario-hub) is designed to be similar to the [US COVID-19 Scenario Modeling Hub](https://github.com/midas-network/covid19-scenario-modeling-hub)

### Schema files for hub configuration

To take advantage of the infrastructure designed by the Consortium, a hub must contain JSON configuration files in a [specific location and format](hub-config). The schemas that define the structure and formats of the configuration files live in their own [schemas repository](https://github.com/Infectious-Disease-Modeling-Hubs/schemas). The schemas are versioned, and every hub must point to a specific version of the schemas that they are using.

## Software for modeling hubs

The main benefit of setting up a hub using the structure outlined in this documentation is that it enables you to use a wide array of tools designed to support common modeling hub tasks, like loading model output data, plotting the model output data, building ensembles using the data, and in some cases evaluating the predictions made by different models. 

- [`hubUtils`](https://infectious-disease-modeling-hubs.github.io/hubUtils/) is an R package with utility functions for working with data from modelings hubs.  
- [`hubEnsembles`](https://github.com/Infectious-Disease-Modeling-Hubs/hubEnsembles) is an R package with functionality to build simple ensembles of data from modeling hubs.  
- [`hubValidations`](https://github.com/Infectious-Disease-Modeling-Hubs/hubValidations) is an R package that facilitates the implementation of general validation rules to enforce on submissions to modeling hubs.   







```{toctree}
:maxdepth: 2
:caption: Overview
:hidden:
overview/who-we-are.md
overview/scope.md
overview/definitions.md
overview/getting-started.md
overview/software.md
```

```{toctree}
:maxdepth: 2
:caption: Data formats
:hidden:
format/intro-data-formats.md
format/hub-structure.md
format/task-id-vars.md
format/hub-config.md
format/model-metadata.md
format/model-output.md
format/target-data.md
format/model-abstracts.md
```

```{toctree}
:maxdepth: 2
:caption: Data validation
:hidden:
validation/validation.md
```
