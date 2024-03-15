# Software  

To assist users in building a hub, we have developed a software suite with specific functions and uses outlined below. These tools are designed to support common modeling hub tasks, like loading model output data, plotting the model output data, building ensembles using the data, and in some cases evaluating the predictions made by different models.  

## [`hubData`](https://github.com/Infectious-Disease-Modeling-Hubs/hubData)  

The goal of `hubData` is to provide tools for connecting to, interacting with, and manipulating Hub data. [Here are instructions](https://github.com/Infectious-Disease-Modeling-Hubs/hubData) to download and use the package.  

## [`hubAdmin`](https://github.com/Infectious-Disease-Modeling-Hubs/hubAdmin)  

The `hubAdmin` package contains utility functions for administering Hubs, in particular creating and validating hub configuration files. [Here are instructions](https://github.com/Infectious-Disease-Modeling-Hubs/hubAdmin) to download and use the package.  

## [`hubUtils`](https://infectious-disease-modeling-hubs.github.io/hubUtils/)  

`hubUtils` is a lightweight package that primarily contains general utilities imported by other hubverse packages. Previously, `hubUtils` was a larger package with more functions, but most of these were moved and split across `hubData` and `hubAdmin`.   

## [`hubEnsembles`](https://github.com/Infectious-Disease-Modeling-Hubs/hubEnsembles)  

`hubEnsembles` is an R package with functionality to build simple ensembles of data from modeling hubs. Different ensembles can be built using for instance the mean, median, and mode. You can find the complete package and instructions for use [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubEnsembles).  

## [`hubValidations`](https://github.com/Infectious-Disease-Modeling-Hubs/hubValidations)  

The `hubValidations` repository facilitates the implementation of general validation rules that are enforced on submissions in the form of pull requests to hub repositories. You can find the complete package and instructions for use [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubValidations).  

## [`hubVis`](https://github.com/Infectious-Disease-Modeling-Hubs/hubVis)  

The goal of `hubVis` is to provide plotting methods for hub model outputs in order to synthesize and visualize model submissions. You can find the complete package and instructions for use [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubVis).  

