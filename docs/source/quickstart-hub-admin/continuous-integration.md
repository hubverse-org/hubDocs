# Setting up continuous integration via GitHub Actions

Continuous integration (CI) is a practice that involves automating the way code and data are validated before being merged into a shared repository. CI allows code and data to be built and tested when any changes are made, which can help users and developers identify and debug errors sooner. CI tasks are carried out via a *workflow*, an automated process with steps (i.e., *jobs*) running sequentially or simultaneously. Workflows are triggered by an *event* or a specific activity within a repository, such as a request to merge new code or data into a repository branch. Hubs hosted on GitHub with a hubverse-compliant structure can use [GitHub Actions](https://github.com/features/actions), specifically the hubverse GitHub Action templates we've developed to perform a variety of CI workflows. 
This page provides information on:
* installing continuous integration workflows
* setting up hubverse GitHub Actions
* available hubverse GitHub Actions


## Installing continuous integration workflows with `hubCI`
You can use the [`hubCI` R package](https://github.com/hubverse-org/hubCI) to set up hubverse CI workflows. The development version can be installed with:

``` r
# install.packages("remotes")

remotes::install_github("hubverse-org/hubCI")
```
## Setting up hubverse GitHub Actions

The [`hubverse-actions`](https://github.com/hubverse-org/hubverse-actions) repository currently contains directories with templates related to the following workflows:

* [`cache-hubval-deps`](https://github.com/hubverse-org/hubverse-actions/tree/main/cache-hubval-deps)
* [`validate-config`](https://github.com/hubverse-org/hubverse-actions/tree/main/validate-config)
* [`validate-submission`](https://github.com/hubverse-org/hubverse-actions/tree/main/validate-submission)
* [`hubverse-aws-upload`](https://github.com/hubverse-org/hubverse-actions/tree/main/hubverse-aws-upload)

More information on each of these workflows is provided in the section below. 

GitHub Actions can be downloaded using the command `use_hub_github_action()` with the action's name in parentheses.

For example, to download the GitHub action `validate-submission`, you would use the code below:

``` r
library(hubCI)

use_hub_github_action(name = "validate-submission")
```

Please note that **your hub needs to be hosted on GitHub to use these actions**. In addition, your hub must be configured as an R project (i.e., contain a *.Rproj file), as this is a requirement of the `usethis` function we are currently using to download these workflows (this requirement might be relaxed in the future).  

## Available hubverse GitHub Actions

### [`cache-hubval-deps`](https://github.com/hubverse-org/hubverse-actions/tree/main/cache-hubval-deps)
This hubverse action downloads the software components required for others to work correctly (i.e., *dependencies*) in `hubValidations`. It stores them on a high-speed storage layer (i.e., *cache*) on the `main` branch. This dependency cache is available to all child branches, including on forks, which speeds up most submission validation workflows.

This action is run on a nightly schedule but can also be triggered by a push to the workflow from the `main` branch. 

More information can be found on the [README for `cache-hubval-deps`](https://github.com/hubverse-org/hubverse-actions/tree/main/cache-hubval-deps#readme).


### [`validate-submission`](https://github.com/hubverse-org/hubverse-actions/tree/main/validate-submission)
This hubverse action installs the `hubValidations` package and the required system dependencies using [pak](https://pak.r-lib.org/).
It then performs submission validation checks through the function `hubValidations::validate_pr()`.

The action is triggered by pull requests onto the `main` branch that add or modify files in the `model-output` and/or `model-metadata` directories. 

More information can be found on the [`validate-submission` README](https://github.com/hubverse-org/hubverse-actions/tree/main/validate-submission#readme) and in the hubValidations vignette on [Validating Pull Requests on GitHub](https://hubverse-org.github.io/hubValidations/articles/validate-pr.html).

### [`validate-config`](https://github.com/hubverse-org/hubverse-actions/tree/main/validate-config)

This hubverse action installs the `hubAdmin` package from GitHub using pak and the required system dependencies.

It then performs submission validation checks through the function `hubAdmin::validate_hub_config()` and assumes you have all three of the required configuration JSON files in your `hub-config/` directory:

 - `admin.json`
 - `model-metadata-schema.json`
 - `tasks.json`

When invalid config files are discovered, a GitHub comment is created (or updated) with a table containing information about the exact locations of the failures using the [`hubAdmin::view_config_val_errors()`](https://hubverse-org.github.io/hubAdmin/reference/view_config_val_errors.html) function. 

The action is triggered by pull requests onto the `main` branch, which adds or modifies files in the `hub-config/` directory. For hubs and repositories with differing configurations, workflow dispatch must be customized manually in the hubs workflow file.

### [`hubverse-aws-upload`](https://github.com/hubverse-org/hubverse-actions/tree/main/hubverse-aws-upload)
This action uploads your hub data to hubverse-hosted cloud storage. Currently, the workflow has a single job, `upload`, that pushes data to an Amazon Web Services (AWS) Simple Storage Service (S3) bucket.
The `upload` job inspects the hub's admin config (`admin.json`) for a `cloud` group. If cloud is enabled (i.e., if `cloud.enabled` is set to `true`), the job:
* authenticates to the hubverse AWS account,
* uses `cloud.host.storage` to determine the name of the hub's S3 bucket and
* syncs the hub's `hub-config`, `model-metadata`, and `model-output` directories to the S3 bucket
 
Before using this action, a member of the hubverse development team will need to "onboard" your hub to AWS. 

More information can be found on the [`hubverse-aws-upload` README](https://github.com/hubverse-org/hubverse-actions/tree/main/hubverse-aws-upload#readme).  
