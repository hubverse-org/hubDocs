# Using the modeling hub  

First, it is helpful to understand the target data we want to compile.  

## Target data  

Many hubs will focus on modeling tasks where the goal is to estimate or predict a quantity that is in principle observable, we refer to this as 'target data'. A detailed description of target data can be found [here](../user-guide/target-data.md).  

The requirements for 'target data' are:  
1. To define what the truth data source is and provide a pointer to the original source in your technical readme document that will be discussed below.  
2. To decide where to store a copy of the 'target data' on the hub, to describe the 'target data' and to provide a pointer to the copy in your technical readme document that will be discussed below.  

## Technical ReadMe  

You now have a repository to collect models (in this example, forecasts), and you need to populate it. You will probably do this by requesting models (e.g., forecasts) from modelers. A standard way to do this is to create a technical ReadMe that contains submission instructions. The technical ReadMe should include the following concepts, with their corresponding explanations.  
- Definition of a model or forecast  
- Ground truth data  
- Data formatting  
- Model (e.g., forecast) file format  
- Model (e.g., forecast) data validation  
- Retractions  
- Weekly ensemble and visualization deployment  
- Policy on late submissions  

This technical ReadMe should be stored on your hub. You will need to share this document with modelers when requesting submissions of forecasts.  

[This is an example of a technical ReadMe](https://github.com/reichlab/covid19-forecast-hub/blob/master/data-processed/README.md) that is used by the US COVID-19 Forecast Hub.

## Accepting forecasts  

Before you put out the word that you are accepting submissions of models (such as forecasts) and before you give a date of when the submissions are due, you should be prepared to accept the data. The [`hubValidations`](https://hubverse-org.github.io/hubValidations/) repository facilitates the implementation of general validation rules that are enforced on submissions in the form of [pull requests](https://docs.github.com/articles/about-pull-requests) to hub repositories.  

## Looking at the data  
Once you have collected some models, you will want to explore the data. We have built a [software suite](../user-guide/software.md) to support common modeling hub tasks, like loading model output data, plotting the model output data, building ensembles using the data, and in some cases evaluating the predictions made by different models.

## Building ensembles  
[`hubEnsembles`](https://hubverse-org.github.io/hubEnsembles/) is an `R` package with functionality to build simple ensembles of data from modeling hubs. Different ensembles can be built using for instance the mean, median, or mode.  
