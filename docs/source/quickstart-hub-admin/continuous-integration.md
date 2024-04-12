# Using continuous integration via Github Actions

Continuous integration (CI) is a practice that involves automating frequent code commits to a shared repository. This allows code to be continually built and tested, which can help you identify and debug errors sooner. Hubverse hubs can use [GitHub Actions](https://github.com/features/actions) to perform a variety of CI tasks. 

The [`hubverse-actions`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions) repository currently contains directories with templates related to the following Github Actions:

### [`cache-hubval-deps`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps)
This hubverse action builds a cache of dependencies for the `hubValidations` package on the `main` branch using `r-lib/actions/setup-r-dependencies@v2` Github Action. This makes the dependency cache available to all child branches, including on forks, speeding up most submission validation workflows.

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/cache-hubval-deps).

### [`Hubverse-aws-upload`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload)
This action uploads hub data to Hubverse-hosted cloud storage. Currently, the workflow has a single job, `upload`, that pushes data to an AWS S3 bucket.
The `upload` job performs the following steps:
1.	Inspects the hub's admin config (`admin.json`) for a `cloud` group.
2.	If `cloud.enabled` is set to `true`:
    -	authenticate to the Hubverse AWS account
    -	use `cloud.host.storage` to determine the name of the hub's S3 bucket
    -	sync the hub's `hub-config`, `model-metadata`, and `model-output` directories to the S3 bucket

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/hubverse-aws-upload).

### [`Validate-submission`](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission)
This hubverse action installs the `hubValidations` package from GitHub using pak as well as required system dependencies.
It then performs submission validation checks through function `hubValidations::validate_pr()`.

More information can be found [here](https://github.com/Infectious-Disease-Modeling-Hubs/hubverse-actions/tree/main/validate-submission).



# Installing continuous integration workflows
[`hubCI`](https://github.com/Infectious-Disease-Modeling-Hubs/hubCI) is an R software package that provides functionality for setting up hubverse CI workflows. The development version can be installed with:

``` r
# install.packages("remotes")

remotes::install_github("Infectious-Disease-Modeling-Hubs/hubValidations")
```



# Setting up a Github Action

For hubs hosted on the GitHub, GitHub Actions can be downloaded with:

```{r example, eval = FALSE}
library(hubCI)

use_hub_github_action(name = "validate-submission")
```

Note: the hub must be configured as an R project (i.e. contain a *.Rproj file)
