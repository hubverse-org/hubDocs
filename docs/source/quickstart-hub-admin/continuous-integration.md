# Setting up continuous integration via GitHub Actions

Continuous integration (CI) is a practice that involves automating the way code and data are validated prior to being merged into a shared repository. This allows code and data to be built and tested when any changes are made, which can help users and developers identify and debug errors sooner. CI tasks are carried out via a *workflow*, an automated process with steps (i.e., *jobs*) that are run either sequentially or simultaneously. Workflows are triggered by an *event*, or a specific activity within a repository, such as a request to merge new code or data into a branch of a repository. Hubs that exist as GitHub repositories with hubverse-compliant data can use [GitHub Actions](https://github.com/features/actions) to perform a variety of CI workflows. 
This page provides information on:
* installing continuous integration workflows
* setting up hubverse GitHub Actions
* available hubverse GitHub Actions


## Installing continuous integration workflows with `hubCI`
You can use the [`hubCI`](https://github.com/Infectious-Disease-Modeling-Hubs/hubCI) software package (R) to set up hubverse CI workflows. The development version can be installed with:

``` r
# install.packages("remotes")

remotes::install_github("Infectious-Disease-Modeling-Hubs/hubCI")
```
## Setting up hubverse GitHub Actions

The [`hubverse-actions`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions) repository currently contains directories with templates related to the following workflows:

* [`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
* [`validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
* [`hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)

More information on each of these workflows is provided in the section below. 

Please note that while anyone with an RStudio project can download GitHub Actions, your hub needs to be hosted on GitHub in order to use these Actions. GitHub Actions can be downloaded using the command `use_hub_github_action()` with the name of the action in parentheses.

For example, to download the github action `validate-submission`, you would use the code below:

```{r example, eval = FALSE}
library(hubCI)

use_hub_github_action(name = "validate-submission")
```

Note: the hub must be configured as an R project (i.e. contain a *.Rproj file), as this is a requirement of the `usethis` function we are using to create these workflows.  

## Available hubverse GitHub Actions

### [`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
This hubverse action downloads the software components that are required for others to work properly (i.e., *dependencies*) in `hubValidations` and stores them on a high-speed storage layer (i.e., *cache*) on the `main` branch. This dependency cache is available to all child branches, including on forks, which speeds up most submission validation workflows.

This action is run on a nightly schedule but can also be triggered by a push to the workflow from the `main` branch. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps).


### [`validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
This hubverse action installs the `hubValidations` package from GitHub using [pak](https://pak.r-lib.org/) as well as required system dependencies.
It then performs submission validation checks through the function `hubValidations::validate_pr()`.

The action is triggered by pull requests onto the `main` branch that add or modify files in the `model-output` and/or `model-metadata` directories. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission) as well as in the hubValidations vignette on [Validating Pull Requests on GitHub](https://infectious-disease-modeling-hubs.github.io/hubValidations/articles/validate-pr.html).

### [`hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)
This action uploads your hub data to hubverse-hosted cloud storage. Currently, the workflow has a single job, `upload`, that pushes data to an Amazon Web Services (AWS) Simple Storage Service (S3) bucket.
The `upload` job inspects the hub's admin config (`admin.json`) for a `cloud` group. If cloud is enabled (i.e., if `cloud.enabled` is set to `true`), the job:
* authenticates to the hubverse AWS account
* uses `cloud.host.storage` to determine the name of the hub's S3 bucket, and
* syncs the hub's `hub-config`, `model-metadata`, and `model-output` directories to the S3 bucket
 
Before using this action, a member of the hubverse development team will need to "onboard" your hub to AWS. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload).



