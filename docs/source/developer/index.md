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

### Dashboard

In late 2024, a project was developed that allows hub admins to easily create a
website that contains a
[predtimechart](https://github.com/reichlab/predtimechart)-like dashboard and an
evaluations dashboard.

A summary of the approach and tools can be found in [The Hub Dashboard project poster](https://github.com/reichlab/decisions/blob/main/project-posters/hub-dashboard/hub-dashboard.md).


## Processes


### Planning

Discussions of new features and prioritizing bug fixes happens every Wednesday
(except first Wednesday of the month) at the hubverse developer's meeting. Please
contact Zhian Kamvar (zkamvar@umass.edu) if you would like to be invited.

As of 2025, decisions are recorded in <https://github.com/reichlab/decisions>.

### Project Board

This GitHub project board contains an overview of Hubverse tickets and work in progress:
<https://github.com/orgs/hubverse-org/projects/3/views/2>.

### R Package Contributing and Maintenance

The [`hubDevs`](https://hubverse-org.github.io/hubDevs) package is a package
that provides tools for getting started with developing a new package in The
Hubverse.

If you want to contribute to an existing Hubverse package, please consult the
`CONTRIBUTING.md` document for details on how to contribute.

### R Package Release Process

R packages are published to The Hubverse R Universe upon minting a new GitHub
release. This process is detailed in the 
[Introduction to the release process article](https://hubverse-org.github.io/hubDevs/dev/articles/release-process.html) in hubDevs.


### Testing

In-development versions R packages are tested weekly on GitHub Actions runners.
Released versions are tested weekly in <https://github.com/hubverse-org/pkg-health-check>

