# AWS Onboarding (and Offboarding)

The Hubverse team currently provides cloud hosting for hubs. A "cloud-enabled" hub is one that
mirrors its data and configuration to an Amazon Web Services (AWS) S3 bucket. By default, the current
hub directories are synced in near-real-time to AWS:

- auxiliary-data
- hub-config
- model-abstracts
- model-metadata
- model-output
- target-data

## Cloud Onboarding Setup

Because each hub has its own S3 bucket and other dedicated AWS resources, a member of the Hubverse team needs to be
involved in cloud onboarding.

If a hub admin wants to enable cloud hosting, these are the steps to follow:

1. Decide on a name for the hub's S3 bucket. S3 bucket names must follow
   Amazon's
   [bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html) and be globally unique.
2. Create the hub's AWS resources by following instructions in the
   [`hubverse-infrastructure` README](https://github.com/hubverse-org/hubverse-infrastructure/blob/main/README.md#onboarding-a-hub-to-aws).\
    **Note:** Don't be intimidated by "creating AWS resources." The process is automated and requires a three line
    config change.
3. Once the AWS resources are in place, submit a PR to the hub:
    - Add a `cloud` section to the `admin.json` file. See the
      [Hubverse schema documentation](#hub-admin-config)
      for more details.
    - Add the [`hubverse-aws-upload.yaml` GitHub workflow file](https://github.com/hubverse-org/hubverse-actions/blob/main/hubverse-aws-upload/hubverse-aws-upload.yaml).
      This is a Hubverse-maintained workflow that runs after a PR is merged to the hub's `main` branch. You do not need
      to make changes to this file.
    - Update the hub's README to include information about accessing data from S3. The `hubTemplate` repo has some
      [boilerplate to use as a starting point](https://github.com/hubverse-org/hubTemplate/blob/main/README.md#accessing-hub-data-on-the-cloud).

:::{tip}
As an example of this process, here are the pull requests used to onboard the `variant-nowcast-hub` to AWS:

- [Creating the AWS infrastructure](https://github.com/hubverse-org/hubverse-infrastructure/pull/63)
- [Updating `admin.json` and adding the new GitHub workflow](https://github.com/reichlab/variant-nowcast-hub/pull/159)
- [Adding information about cloud data access to the README](https://github.com/reichlab/variant-nowcast-hub/pull/331)
:::

Other notes:

- A hub can be onboarded at any time.
- The S3 data sync occurs after pull requests are merged to the hub. The sync process does not interfere
  with hub operations (for example, if AWS is down, hub validations and other tasks will still work).
- Mirroring a hub's data to the Hubverse-hosted AWS account does not require AWS tokens or other secrets to be stored
  in its repository.

## How it works

At a high level, this diagram describes the interactions between hub users, the hub hosted on GitHub, and the
hub's data mirrored to AWS:

```{mermaid}
:name: onboarding-aws
:alt: An architecture diagram that depicts the components of an AWS-hosted hub
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
sequenceDiagram
    create actor A as hub admins and modelers
    create participant h as hub
    A->>h: PR: update hub config
    A->>h: PR: submit model-output
    h-->h: run validations
    h-->h: generate target data
    create participant hc as Hubverse cloud
    h->>hc: sync config, target, and model output data
    actor B as hub data user
    B->>hc: query hub data
    hc->>B: return data
```

## Cloud Offboarding

Removing a hub from Hubverse AWS hosting is essentially a reverse of the onboarding
process, with a few caveats.

1. Update the hub's `admin.json` file, setting the `cloud.enabled` value to false. \
   **Note:** You can also remove the entire `cloud` section if you prefer.
2. **Optional:** Remove the `hubverse-aws-upload.yaml` workflow file from the hub.
   Leaving this workflow intact won't harm anything because it checks `admin.json`
   for `cloud.enabled` = true before syncing data to AWS.
3. To completely remove the hub's AWS resources:

  - Manually delete the contents of the hub's S3 bucket (AWS does not
    permit deleting S3 buckets that contain objects).
  - Submit a PR to [`hubverse-infrastructure`](https://github.com/hubverse-org/hubverse-infrastructure)
    that removes the hub from the `hubs.yaml` file.
  - Once the PR is merged, the hub's AWS resources will be deleted.
