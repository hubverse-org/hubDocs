# Setting up continuous integration via Github Actions

Continuous integration (CI) is a recommended practice that involves automating frequent code commits to a shared repository. This allows code to be continually built and tested, which can help you identify and debug errors sooner. Hubverse hubs can use [GitHub Actions](https://github.com/features/actions) to perform a variety of CI tasks. These tasks are carried out via a *workflow*, an automated process with steps (i.e., *jobs*) that are run either sequentially or in parallel. Workflows are triggered by an *event*, or a specific activity within a repository.   

The [`hubverse-actions`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions) repository currently contains directories with templates related to the following workflows:

## Continuous integration workflow with cloud storage

### [`Hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)
This action uploads your hub data to Hubverse-hosted cloud storage. Currently, the workflow has a single job, `upload`, that pushes data to an Amazon Web Services (AWS) Simple Storage Service (S3) bucket.
* The `upload` job inspects the hub's admin config (`admin.json`) for a `cloud` group. If cloud is enabled (i.e., if `cloud.enabled` is set to `true`), the job:
    + authenticates to the Hubverse AWS account
    + uses `cloud.host.storage` to determine the name of the hub's S3 bucket, and
    + syncs the hub's `hub-config`, `model-metadata`, and `model-output` directories to the S3 bucket
 
Before using this action, a member of the Hubverse development team will need to "onboard" your hub to AWS. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload).

## Continuous integration workflows with `hubValidations`

### [`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
This hubverse action makes it so the first time your job is run with the `hubValidations` package, the software components that are required for others to work properly (i.e., *dependencies*) are downloaded and stored on a high-speed storage layer (i.e., *cached*) on the `main` branch. This dependency cache is available to all child branches, including on forks, which speeds up most submission validation workflows.

This action is run on a nightly schedule but can also be triggered by a push to the workflow from the `main` branch. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps).


### [`Validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
This hubverse action installs the `hubValidations` package from GitHub using pak as well as required system dependencies.
It then performs submission validation checks through the function `hubValidations::validate_pr()`.

The action is triggered by pull requests onto the `main` branch that add or modify files in the `model-output` and/or `model-metadata` directories. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission).



## Installing continuous integration workflows with `hubValidations`
You can use the [`hubCI`](https://github.com/Infectious-Disease-Modeling-Hubs/hubCI) software package (R) to set up hubverse CI workflows. The development version can be installed with:

``` r
# install.packages("remotes")

remotes::install_github("Infectious-Disease-Modeling-Hubs/hubValidations")
```


## Setting up a Github Action with `hubValidations`

If your hub is hosted on GitHub, you can download GitHub Actions with:

```{r example, eval = FALSE}
library(hubCI)

use_hub_github_action(name = "validate-submission")
```

Note: the hub must be configured as an R project (i.e. contain a *.Rproj file)
