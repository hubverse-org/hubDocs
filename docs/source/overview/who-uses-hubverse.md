# Who is the hubverse for?

A **modeling hub** consists of one or more **hub administrators** who are responsible for coordinating model submissions from **modelers** who submit **model outputs** in a standardized format defined by the hub.
Model outputs are validated upon submission and at the end of every round. A summary of the individual and ensemble model outputs is presented to **stakeholders** who may be responsible for informing policy decisions.
All of these roles are directly supported by **hubverse developers** 
You may fit one, several, or none of these roles.
Below are details of what aspects of the hubverse each role will interact with.

```{image} ../images/hubverse_roles.png
:alt: Schematic of the hubverse showing different roles
:caption: A schematic illustration of the hubverse, showing different roles
```

## Hub administrators

You are responsible for setting up hubs in response to official challenges that define specific modeling targets and timeframes.
This involves:

 - setting up a central repository for the model submissions and target data
 - codifying the submission format for the modeling efforts in `tasks.json`
   - submission cadence (`rounds`)
      - modeling tasks (`model_tasks`) that correspond to specific modeling targets (e.g., incident hospitalizations)
        - combinations of categorical variables for model inputs (`task_ids`)
        - modeling output types and valid ranges (`output_type`)
 - transforming truth (target) data into standardized modeling targets for downstream validation
 - validate submissions as they arrive

The [quickstart chapter](/quickstart-hub-admin/intro.md) will get you up and running with a new hub. The [user guide](/user-guide/intro-data-formats.md) is a good resource for translating the modeling challenge language into a `tasks.json` configuration file.
You can use the [`{hubAdmin}` R package](https://hubverse-org.github.io/hubAdmin) to aid in the creation of this file.

## Modelers

You will ultimately submit your model outputs in the format specified by the hub administrators.
Do that freaky modeling magic you do with whatever resources you have on hand.
You use R? Great! Python? Go for it! Excel? Nobody's stopping you! Dark Magick? Uh, maybe try a TI-86.

You will be most interested in knowing how to format your output.
For that, you can use functions from the [`{hubValidations}` R package ](https://hubverse-org.github.io/hubValidations):

- Use [`submission_tmpl()`](https://hubverse-org.github.io/hubValidations/reference/submission_tmpl.html) to create a submission template and get an idea of what your model outputs should look like to be successfully incorporated into a hub. This includes accepted values for different columns as well the data types each column should adhere to. You can subset this template depending on the type of model output you're submitting and populate it with your model output values.
- Use  [`validate_submission()`](https://hubverse-org.github.io/hubValidations/reference/validate_submission.html) to validate your model output file prior to submitting. This can help pick up any issues with your submission prior to submitting. The sames checks will be also run as part of your submission but running them locally means you have access to additional check output that can hep you identify and fix any problems faster. See more about [validating your submission locally](https://hubverse-org.github.io/hubValidations/articles/validate-submission.html).


As a modeler, you will need to

 - understand the definitions of and differences between [model output types](#model-output-format)
 - understand the [structure of model output datasets](https://hubverse-org.github.io/hubData/articles/connect_hub.html#structure-of-hubverse-datasets)
 - build ensembles using the [`{hubEnsembles}` R package](https://hubverse-org.github.io/hubEnsembles).


## Data analysts

With the standardized data formats and schema in each hub, you can confidently write analysis scripts that will work for all model submissions to a hub.
No data cleaning is needed.
To get started, you can read the [accessing data from a hub vignette](https://hubverse-org.github.io/hubData/articles/connect_hub.html) from the [`{hubData}` R package](https://hubverse-org.github.io/hubData)

Once you have access to the data, you can summarise it in the following ways:

 - loading data
   - predictions data from a formal hub repo
   - predictions data sitting in a folder on your computer
 - plotting forecasts
 - evaluating forecasts
 - ensembling forecasts (via the [`{hubEnsembles}` R package](https://hubverse-org.github.io/hubEnsembles)
 - and more!

## Stakeholders 

You will be presented with visualizations describing the models' trajectory and uncertainty.
As the modeling effort continues, you will be presented with scores for each model that show how well it predicted trajectories.

Make good decisions.

## Hubverse developers

If you want to contribute to the hubverse, you should adhere to our [Code Of Conduct](https://hubverse-org.github.io/hubDevs/CODE_OF_CONDUCT.html).

We have a [contributing guide](contribute.md) that describes the process for contributing minor fixes.
If you want to know more about our packaging process and other valuable details, you can find more in the [`{hubDevs}` R package](https://hubverse-org.github.io/hubDevs/index.html).
