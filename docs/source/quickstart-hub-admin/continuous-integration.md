# Setting up continuous integration via Github Actions

Continuous integration (CI) is a recommended practice that involves automating frequent code commits to a shared repository. This allows code to be continually built and tested, which can help you identify and debug errors sooner. CI tasks are carried out via a *workflow*, an automated process with steps (i.e., *jobs*) that are run either sequentially or simultaneously. Workflows are triggered by an *event*, or a specific activity within a repository. Hubverse hubs can use [GitHub Actions](https://github.com/features/actions) to perform a variety of CI tasks. 
This document provides information on:
* installing continuous integration workflows
* setting up a hubverse Github Actions
* available hubverse Github Actions


## Installing continuous integration workflows with `hubCI`
You can use the [`hubCI`](https://github.com/Infectious-Disease-Modeling-Hubs/hubCI) software package (R) to set up hubverse CI workflows. The development version can be installed with:

``` r
# install.packages("remotes")

remotes::install_github("Infectious-Disease-Modeling-Hubs/hubValidations")
```
## Setting up hubverse Github Actions

The [`hubverse-actions`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions) repository currently contains directories with templates related to the following workflows:

[`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
[`Validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
[`Hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)

More information on each of these workflows is provided in the section below. 

If your hub is hosted on GitHub, you can download GitHub Actions with this command followed by the name of the action in ():

```
use_hub_github_action():
```
For example, to download the github action `validate-submission`, you would use the code below:

```{r example, eval = FALSE}
library(hubCI)

use_hub_github_action(name = "validate-submission")
```

Note: the hub must be configured as an R project (i.e. contain a *.Rproj file)

## Available hubverse Github Actions

### [`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
This hubverse action downloads the software components that are required for others to work properly (i.e., *dependencies*) in `hubValidations` and stores them on a high-speed storage layer (i.e., *cache*) on the `main` branch. This dependency cache is available to all child branches, including on forks, which speeds up most submission validation workflows.

This action is run on a nightly schedule but can also be triggered by a push to the workflow from the `main` branch. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps).


### [`Validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
This hubverse action installs the `hubValidations` package from GitHub using pak as well as required system dependencies.
It then performs submission validation checks through the function `hubValidations::validate_pr()`.

The action is triggered by pull requests onto the `main` branch that add or modify files in the `model-output` and/or `model-metadata` directories. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission).

### [`Hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)
This action uploads your hub data to Hubverse-hosted cloud storage. Currently, the workflow has a single job, `upload`, that pushes data to an Amazon Web Services (AWS) Simple Storage Service (S3) bucket.
* The `upload` job inspects the hub's admin config (`admin.json`) for a `cloud` group. If cloud is enabled (i.e., if `cloud.enabled` is set to `true`), the job:
    + authenticates to the Hubverse AWS account
    + uses `cloud.host.storage` to determine the name of the hub's S3 bucket, and
    + syncs the hub's `hub-config`, `model-metadata`, and `model-output` directories to the S3 bucket
 
Before using this action, a member of the Hubverse development team will need to "onboard" your hub to AWS. 

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload).



