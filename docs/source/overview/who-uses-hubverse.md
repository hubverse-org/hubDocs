# Who is the hubverse for?

A **modelling hub** consists of one or more **hub administrators** who are responsible for coordinating model submissions from **modellers** who submit **model outputs** in a standardized format defined by the hub.
Model outputs are validated on submission and at the end of every round, a summary of the individual and ensemble model outputs is presented to **stakeholders** who may be responsible for informing policy decisions.
All of these roles are directly supported by **hubverse developers** 
You may fit one, several, or none of these roles.
Below are details of what aspects of the hubverse each role are going to interact with.

## Hub administrators

You are responsible for setting up hubs in response to official challenges that define specific modelling targets and timeframes.
This involves:

 - setting up central repository for the model submissions and target data
 - codifying the submission format for the modelling efforts in `tasks.json`
   - submission cadance (`rounds`)
      - modelling tasks (`model_tasks`) that correspond to specific modelling targets (e.g. incident hospitalizations)
        - combinations of categorical variables for model inputs (`task_ids`)
        - modelling output types and valid ranges (`output_type`)
 - transforming truth (target) data into standardized modelling targets for downstream validation
 - validate submissions as they arrive

The [quickstart chapter](/quickstart-hub-admin/intro.md) will get you up and running with a new hub and the [user guide](/user-guide/intro-data-formats.md) are good resources to get started with translating the challenge language into a `tasks.json` configuration file.
You can use the [`{hubAdmin}` R package](https://hubverse-org.github.io/hubAdmin) to aid in the creation of this file.

## Modellers

You will ultimately submit your model outputs in the format specified by the Hub Administrators.
Do that freaky modelling magic you do with whatever resources you have on hand.
You use R? Great! Python? Go for it! Excel? Nobody's stopping you! Dark Magick? Uh, maybe try a TI-86.

You will be most interested in knowing how to format your output.
For that, you can use a function from the [`{hubAdmin}` R package ](https://hubverse-org.github.io/hubAdmin) to create an expanded model output grid.
You can then fit your outputs to that format and submit it to the hub.
They will be validated on submission.

As a modeller, you will need to

 - understand the definitions of and differences between [model output types](/user-guide/model-output.md#formats-of-model-output)
 - understand the [structure of model output datasets](https://hubverse-org.github.io/hubData/articles/connect_hub.html#structure-of-hubverse-datasets)
 - build ensembles using the [`{hubEnsembles}` R package](https://hubverse-org.github.io/hubEnsembles).


## Data analysts

With the standardized data formats and schema in each hub, you can confidently write analysis scripts that will work for all model submissions to a hub.
No data cleaning needed.
To get started, you can read the [Accessing data from a hub](https://hubverse-org.github.io/hubData/articles/connect_hub.html) vignette from the [`{hubData}` R package](https://hubverse-org.github.io/hubData)

Once you have access to the data, you can summarise it in the following ways:

 - loading data
   - predictions data from a formal hub repo
   - predictions data sitting in a folder on your computer
 - plotting forecasts
 - evaluating forecasts
 - ensembling forecasts (via the [`{hubEnsembles}` R package](https://hubverse-org.github.io/hubEnsembles)
 - and more!

## Stakeholders 

You will be presented with visualisations that describe the trajectory and uncertainty of the models.
As the modelling effort continues, you will be presented with scores for each model that shows you how well it was able to predict trajectories.

Make good decisions.

## Hubverse developers

If you want to contribute to the hubverse, you should adhere to [our Code Of Conduct](https://hubverse-org.github.io/hubDevs/CODE_OF_CONDUCT.html).

We have a [contributing guide](contribute.md) that describes the process for
contributing small fixes.
If you want to know more about our packaging process
and other useful details, you can find more in the [`{hubDevs}` R package](https://hubverse-org.github.io/hubDevs/index.html).