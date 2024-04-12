# Continuous integration

Continuous integration (CI) involves frequent code commits to a shared repository, which helps developers identify and debug errors sooner. Hubverse hubs can use [GitHub Actions](https://github.com/features/actions) to perform a variety of CI tasks. 


# Github Actions

The [`hubverse-actions`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions) repository currently contains directories with templates related to the following Github Actions:

## `cache-hubval-deps`
This hubverse action builds a cache of dependencies for the `hubValidations` package on the `main` branch using `r-lib/actions/setup-r-dependencies@v2` Github Action. This makes the dependency cache available to all child branches, including on forks, speeding up most submission validation workflows.

[More information can be found here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps).

## `Hubverse-aws-upload`
This action uploads hub data to Hubverse-hosted cloud storage. Currently, the workflow has a single job, upload, that pushes data to an AWS S3 bucket.
The upload job perform the following steps:
1.	Inspect the hub's admin config (admin.json) for a cloud group.
2.	If cloud.enabled is set to true:
o	authenticate to the Hubverse AWS account
o	use cloud.host.storage to determine the name of the hub's S3 bucket
o	sync the hub's hub-config, model-metadata, and model-output directories to the S3 bucket

[More information can be found here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload).

## `Validate-submission`
This hubverse action installs the `hubValidations` package from GitHub using pak as well as required system dependencies.
It then performs submission validation checks through function `hubValidations::validate_pr()`.

[More information can be found here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission).

# Installation
`hubCI` is an R software package that provides functionality for setting up hubverse CI workflows. The development version can be installed with:

# install.packages("remotes")

remotes::install_github("Infectious-Disease-Modeling-Hubs/hubValidations")

#Setting up a Github Action

For hubs hosted on the GitHub, GitHub Actions can be downloaded with:

library(hubCI)

use_hub_github_action(name = "validate-submission")

Note: the hub most be configured as an R project (i.e. contain a *.Rproj file)
