# Developer Guide

This page is for developers and contributors to the hubverse infrastructure.

## Schema and Example Hubs

Modeling tasks for all hubs are defined validated via hub configuration files.
A valid hub configuration file is defined by our schemas, which are archived in
<https://github.com/hubverse-org/schemas#readme>.

There are four example hubs that can be used for testing:

 - <https://github.com/hubverse-org/example-simple-forecast-hub#readme>
 - <https://github.com/hubverse-org/example-complex-forecast-hub#readme>
 - <https://github.com/hubverse-org/example-simple-scenario-hub#readme>
 - <https://github.com/hubverse-org/example-complex-scenario-hub#readme>

## Projects


### User-facing Software

#### R Packages

All user-facing hubverse packages are released on [The Hubverse R Universe](https://hubverse-org.r-universe.dev/).

See [user-guide/software](../user-guide/software) for a list of these packages.

### Cloud integration

The AWS infrastructure provides opt-in cloud storage to AWS S3 buckets
maintained by the Reich lab so hubs can synchronize data with the cloud.

 - <https://github.com/hubverse-org/hubverse-infrastructure#readme>
   provides an **infrastructure-as-code (IaC)** solution
   - Read more about [onboarding a hub](https://github.com/hubverse-org/hubverse-infrastructure?tab=readme-ov-file#onboarding-a-hub)
 - <https://github.com/hubverse-org/hubverse-transform#readme>
   performs data transformation of model output files and is deployed as an AWS
   Lambda function
 - <https://github.com/hubverse-org/hubverse-cloud> provides a hub that can be used for integration tests

## Processes

### Decisions

As of 2025, decisions are recorded in <https://github.com/reichlab/decisions#readme>

### R Package Maintenance




## Maintainers
