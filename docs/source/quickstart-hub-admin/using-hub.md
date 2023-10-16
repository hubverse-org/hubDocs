# Using the modeling hub  

First, it is helpful to understand the target data we want to compile.  

## Target data  

Many hubs will focus on modeling tasks where the goal is to estimate or predict a quantity that is in principle observable, we refer to this as 'target data'. A detailed description of target data can be found [here](../user-guide/target-data.md).  

The requirements for 'target data' are:  
1. To define what the truth data source is and provide a pointer to the original source in your technical readme document that will be discussed below.  
2. To decide where to store a copy of the 'target data' on the hub, to describe the 'target data' and to provide a pointer to the copy in your technical readme document that will be discussed below.  

## Technical Readme  

You now have a repository to collect forecasts, and you need to populate it. You will probably do this by requesting forecasts from modelers. A standard way to do this is to create a technical readme that contains submission instructions. The technical readme should include the following concepts, with their corresponding explanations.  
- Definition of a forecast  
- Ground truth data  
- Data formatting  
- Forecast file format  
- Forecast data validation  
- Retractions  
- Weekly ensemble and visualization deployment  
- Policy on late submissions  

This technical readme should be stored on your hub. You will need to share this document with modelers when requesting submissions of forecasts.  

## Accepting forecasts  

Before you put out the word that you are accepting submissions of forecasts and give a date of when the submissions are due, you should be prepared to accept the data.  The [`hubValidations`](https://infectious-disease-modeling-hubs.github.io/hubValidations/) repository facilitates the implementation of general validation rules that are enforced on submissions in the form of [pull requests](https://docs.github.com/articles/about-pull-requests) to hub repositories.  

## Looking at the data  
Once you have collected some forecasts, you will want to explore the data. [`hubUtils`](https://infectious-disease-modeling-hubs.github.io/hubUtils/) provides a set of utility functions for downloading, plotting, and scoring forecasts and truth data from modeling hubs.  

## Building ensembles  
[`hubEnsembles`](https://infectious-disease-modeling-hubs.github.io/hubEnsembles/) is an `R` package with functionality to build simple ensembles of data from modeling hubs. Different ensembles can be built using for instance the mean, median, or mode.  

A [vignette](https://github.com/Infectious-Disease-Modeling-Hubs/example-complex-scenario-hub/blob/main/example_workflow.Rmd) is available that details the workflow needed for creating a sample hub.  

