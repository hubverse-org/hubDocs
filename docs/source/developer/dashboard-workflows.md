# Dashboard operational workflows

:::{admonition} Required reading

You are expected to know _how_ the build process of the
dashboard works with respect to being able to identify the tools involved, the
inputs, and the outputs are. If you cannot yet identify these elements, please
go and read the [local dashboard workflow chapter](./dashboard-local.md).

We strongly recommend to look over the [Dashboard tools, operations
section](#dashboard-tools-operations) as that it contains valuable
resources for understanding GitHub workflows.

:::

## An analogy for operations

The purpose of this chapter is concerned with **operational aspects** of
building a dashboard. If you are reading this chapter, you know how to build
the dashboard and you can build a dashboard locally.

To given an imperfect analogy, building a dashboard locally is a lot like
knowing how to cook a meal for five people. You know the ingredients you need,
the tools you can use, and the steps necessary to complete the recipe. You
already have the ingredients and the tools and you can spend a little time in
your kitchen to produce something that is satisfying and delicious.

Providing an operational workflow where anyone can build a dashboard as long as
they have the right inputs is more challenging. Continuing with the kitchen
analogy, imagine now that you still have this knowledge about the ingredients
and tools, but instead of working in your own kitchen, you are now working in
an industrial kitchen and are cooking for 50 people. You _may_ be able to do
everything on your own, but it's better to have help. So now, you have other
people helping with the prep, such as dicing the vegetables, sharpening the
knives, preparing the sauces, and cleaning up. You have to think about _when_
specific parts of the recipe need to be executed, _where_ in the kitchen you
have space to hold the final components, and how to handle variations in the
recipe.

Moving a local workflow to run on GitHub actions is a lot like scaling up a
recipe for a commercial kitchen. You are no longer familiar with your
environment and you cannot assume that you will have all the inputs and
tools at your disposal. Now, you have to think about the following aspects:

1. How do we fetch the source data?
1. How to we make sure our tools are installed?
1. Where do we store the output?
1. When should the components be built?
1. When should the components be deployed?
1. How do we do with variations in hub configuration?
1. How do we distribute this code?
1. How can we inspect the output without deployment?

This chapter will address these questions.

## Rationale

Unlike the local workflow, **the dashboard website and data are built and
deployed separately**. The reason behind this is because the concerns of the
website (displaying information for people interested in the hub) and of the
data (a record of the predictions or evaluations) are separate. If someone
wants to update their home page, they should not have to wait for data to be
rebuilt in order to make that change. Similarly, if the data are updated, it
should not depend on a website build in order to be available.

Another situation one will often encounter are pull requests to update the
configuration files for a hub. In this case, it is important to explicitly test
that the contents can be built, but not to deploy to prevent unexpected things
from happening.


### Timing

Given the rationale above, we would want to define timings for building the site
and the data:

 - build the site
   - when someone adds content to the site (deploy)
   - when someone manually triggers a build (deploy)
   - on a pull request
 - build the data
   - after a submission round closes (deploy)
   - when someone updates the data configuration files (deploy)
   - when someone manually triggers a build (deploy)
   - on a pull request

All of these timings are defined in GitHub Actions.

## About GitHub Actions

GitHub Actions is a framework for [CI/CD (continuous integration and continuous
deployment)](https://en.wikipedia.org/wiki/CI/CD) that emerged in 2019. This
framework supports us being able to test our R packages and allow hub
administrators to validate model submissions as they come through.

All GitHub actions are run via [a YAML workflow
file](https://docs.github.com/en/actions/writing-workflows/about-workflows)
that provides instructions about when, where (e.g. one or more virtual
machines), and how to run a process like testing a package or validating a hub
submission. These workflow files live in the `.github/workflows/` directory in
a GitHub repository and they have two top-level keys that are important to know
about:

| key  | what it does | documentation |
| :--- | :----------- | :------------ |
| `on`| specifies _when_ a workflow should run | [Understanding GitHub Actions: Events](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions?learn=getting_started&learnProduct=actions#events) |
| `jobs` | separates your workflow across a series of runners (virtual machines or docker containers). These can run in parallel or one after another. Many workflows you will see have a single job (e.g. check an R package or validate a submission), but the dashboard workflows use multiple jobs. This is useful for separating build and deploy steps for quality control over permissions. | [Understanding GitHub Actions: Jobs](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions?learn=getting_started&learnProduct=actions#jobs) and [Understanding GitHub Actions: Runners](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions?learn=getting_started&learnProduct=actions#runners) |

Each **job** is made up of a series of **steps** that runs inside of the
**runner** (virtual machine or docker container) that, together, perform the tasks of
fetching resources, installing/caching tools, performing checks, or building
artifacts. Each step can be a snippet of a language like BASH or Python or,
more often, it can be an individual [**action**---a pre-written building block](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions?learn=getting_started&learnProduct=actions#actions) such
as [actions/checkout](https://github.com/actions/checkout) or
[actions/upload-artifact](https://github.com/actions/upload-artifact) that
performs a complex task. Of course, now that GitHub Actions has the concept of
an _action_ as a component of GitHub Actions, the terminology is a bit confusing.
This table may help:

| term | called by | acts like | what it means | think of it as |
| :--- | :------------ | :----------- | :---- | :--------- |
| workflow | N/A | workflow | a YAML file that describes how one or more tasks should be performed | instructions for CI/CD |
| job | workflow | job | Performs a complex task that includes provisioning tools and data. It can take inputs and outputs | an individual docker container |
| step | job | step | a single purpose operation | an single program |
| action | step | step | a pre-written building block | a reusable step that someone else wrote |


## Dashboard workflows

Each dashboard has two workflows, one to build the website and one to build the
data. These workflows are designed so to minimize the required knowledge for
hub administrators to have to deploy the site. This section will discuss the
**broad overview** of these workflows and segue into what's going on behind the
scenes.

While the [local dashboard workflow chapter](./dashboard-local.md) demonstrates
saving the data in individual folders that all live in the site folder, the
operations in practice are slightly different. The workflows that orchestrate
the dashboard build the three components (forecast data, evaluations data, and
website) separately to individual [orphan
branches](https://git-scm.com/docs/git-checkout#Documentation/git-checkout.txt---orphanltnew-branchgt)[^orphan]:

 - `gh-pages` contains the website source
 - `ptc/data` contains the forecast data that is used for the `forecast.html` visualization
 - `predevals/data` contains the evaluations data that is used for the `eval.html` visualization

[^orphan]: An orphan branch is a special kind of branch in git that does not
    contain any history related to the `main` branch. Orphan branches are
    commonly used to store website contents that do not need the source code to
    come along for the ride. In our case, we also use orphan branches to store
    data for the website.

If you were to diagram this process from source to site, it would look like
the diagram below. Here, thick arrows represent `git push` events, thin arrows
represent direct data sources and dashboard arrows represent remote data sources.

Notice that this is nearly identical to the [local workflow](#local-workflow)
with the exception that now the data live in separate branches of the
repository instead of in separate folders.

```{mermaid}
:name: branch-diagram
:alt: A flowchart that demonstrates flow of data from the hub and dashboard to the final site with the tools that build each component labelling arrows.
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart BT
    hub-repo["hub-repo@main"]
    subgraph dashboard-repo
        subgraph workflows
            forecast-workflow
            eval-workflow
            site-workflow
        end
        main>main]
        gh-pages>gh-pages]
        ptc/data>ptc/data]
        predevals/data>predevals/data]
    end
    site
    hub-repo --> forecast-workflow
    main --> forecast-workflow
    hub-repo --> eval-workflow
    main --> eval-workflow
    main --> site-workflow
    forecast-workflow ==> ptc/data
    eval-workflow ==> predevals/data
    site-workflow ==> gh-pages
    gh-pages --> site
    ptc/data -.- site
    predevals/data -.- site
```

Note that this is not the exact structure of the workflows, but it's a good
starting point.

### Operations from the dashboard

In practice, we realize that both the forecast and evals data are going
to be built at the same time, so they actually exist in the same workflow and we
can simplify the diagram a little bit more and introduce some workflow names:

```{mermaid}
:name: branch-diagram-2
:alt: A flowchart that demonstrates flow of data from the hub and dashboard to the final site with the tools that build each component labelling arrows.
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart BT
    hub-repo["hub-repo@main"]
    subgraph dashboard-repo
        subgraph workflows
            build-site.yaml
            build-data.yaml
        end
        main>main]
        gh-pages>gh-pages]
        ptc/data>ptc/data]
        predevals/data>predevals/data]
    end
    site
    hub-repo --> build-data.yaml
    main --> build-data.yaml
    main --> build-site.yaml
    build-data.yaml ==> ptc/data
    build-data.yaml ==> predevals/data
    build-site.yaml ==> gh-pages
    gh-pages --> site
    ptc/data -.- site
    predevals/data -.- site
```

The above diagram shows how the two workflows in the hub dashboard template
operate:

 - [build-site.yaml](https://github.com/hubverse-org/hub-dashboard-template/blob/main/.github/workflows/build-site.yaml) builds the website
 - [build-data.yaml](https://github.com/hubverse-org/hub-dashboard-template/blob/main/.github/workflows/build-data.yaml) builds the data

Both of these workflow files have the same basic structure with the following
top-level keys:

 - `on:` defines the events that cause the workflow to run
 - `permissions:` defines the permissions the workflow has (`contents: write`)
 - `jobs:` defines a single job that will build and push either the site or the data

You might notice, however that both of these files are 50 lines and under.
If you consider the fact that this is fewer lines than
[validate-config.yaml](https://github.com/hubverse-org/hubverse-actions/blob/main/validate-config/validate-config.yaml),
a github workflow whose only job is to validate incoming pull requests and is
not responsible for pushing data, it seems... strange that we can encapsulate a
process that provisions a tool we built, fetches data, builds data, and pushes
it to the appropriate branch in a 50 line configuration file.

The key to this is in these lines:

```yaml
uses: hubverse-org/hub-dashboard-control-room/.github/workflows/generate-site.yaml@main
```

```yaml
uses: hubverse-org/hub-dashboard-control-room/.github/workflows/generate-data.yaml@main
```

These are known as reusable workflows.


## Reusable workflows

The reason we can provide two workflow files with a combined total of fewer
than 100 lines of code is because we are using [Reusable
workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows).
The reusable workflow is one that is able to chain several workflows and jobs
into one single job that can be called from any repository as long as it's
public. Just like an **action** can be a stand in for a **step** in a workflow,
a **reusable workflow** can be a stand in for a **job** in a workflow.

There are three reusable workflows in the [control room](https://github.com/hubverse-org/hub-dashboard-control-room):

1. `generate-site.yaml` builds the website and pushes it to the `gh-pages` branch
1. `generate-data.yaml` builds both the forecast and eval data and pushes them to their respective branches in parallel.
1. `push-things.yaml` pushes an to a specific branch. This reusable workflow is only ever called by the previous two workflows.

Peering into the jobs defined in each workflow, we can see what they are doing.

:::{tip}

The [dashboard tools chapter, operations section](#dashboard-tools-operations)
contains links to resources that are valuable reading for understanding concepts
that are specific to GitHub workflows.

:::


:::{admonition} GitHub App-related inputs, outputs, and steps
:class: dropdown important

**All GitHub App related inputs, outputs, and steps will can be ignored for this
chapter.**

There are a few parts in each of these workflows that are related to handling
the credentials for a GitHub App (see [2024-12-13 RFC hub dashboard
orchestration](https://github.com/reichlab/decisions/blob/main/decisions/2024-12-13-rfc-hub-dashboard-orchestration.md)
for details). I'll list them below with notes about what they do or why they
were deprecated, but remember that this is not required reading.

### Inputs

There is one input that is **deprecated** and no longer used or relevant:
**`repos`**. See
[hub-dashboard-control-room#14](https://github.com/hubverse-org/hub-dashboard-control-room/issues/14)
for details of the workflow that previously used this field.

### Outputs

The `is-bot` output is a flag that indicates if the workflow is being run by the
GitHub App. In a workflow that's run from a dashboard repository, this will
be `false`.

In the context of running a reusable workflow via an app, it is important for
separating the concerns of the temporary app token between the build and push
steps. Otherwise, it is not necessary because the workflow would then be run in
the same context as the calling repository and would automatically have a
temporary token with the correct permissions.

### Steps

A summary of these steps is:

1. **`is-bot`** checks the `secrets.id` input. If it is `'none'`, then the output
   of this step (`steps.is-bot.outputs.bot`) is `false` indicating that the
   `secrets.key` is a valid GitHub token. If the output is `true`, then the
   `key` represents a PEM key that can be used to generate a token.
2. **`token`** only runs if `steps.is-bot.outputs.bot` is `true`. It uses the
   values from `secrets.id` and `secrets.key` to generate a temporary access
   token for the particular repository.

When discussing the workflows below **we will skip these steps.**

:::

:::{admonition} A legend for diagrams
:class: note

From here on out, we are going to rely heavily on diagrams to illustrate the
workflows and we will use a few conventions:

1. ribbon nodes (asymmetric nodes) are **branches**
1. parallelograms pointing to the right are **inputs**
1. parallelograms pionting to the left are **outputs or artifacts**
   1. artifacts and outputs are often surrounded by their own boxes to indicate
      that they persist beyond the job/workflow execution
   1. output values will have a `key: ` label with the name of the output
1. **surrounding boxes determine the context** and are labelled as such. A box that
   is labelled with `workflow.yaml` is a workflow and nodes will be jobs and
   their outputs
1. rectangles inide of the boxes represents individual **jobs or steps** (depending on context)
1. hexagons are special steps represent **decision points or setup**

```{mermaid}
:name: dashboard-diagram-legend
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph branches
        main>"main"]
        gh-pages>"gh-pages"]
    end
    input[/input/]
    subgraph workflow.yaml
        job/step
        decision{{decision/setup}}
    end
    subgraph artifacts/outputs
        artifact[\"artifact-name"\]
        output[\"output-name: output-value"\]
    end
    external-repository ~~~ branches
    input --> job/step --> artifact
    job/step --> output
```

:::


### `generate-site.yaml`

This workflow has one sequence of two jobs, build-site and push-site. The
workflow only needs information about the hub dashboard and the contents within
it:

```{mermaid}
:name: generate-site-overview
:alt: A flowchart contains two nodes: build site going to push site with inputs from org, dashboard, and publish
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart LR
    org[/reichlab/]
    dashboard[/flusight-dashboard/]
    publish[/publish/]
    subgraph generate-site.yaml
        build-site --> artifact[\artifact\] --> push-site
    end
    org --> build-site
    dashboard --> build-site
    publish --> push-site
```

 - `build-site` runs inside of [hub-dash-site-builder](https://github.com/hubverse-org/hub-dash-site-builder/pkgs/container/hub-dash-site-builder) to build the website and upload it as an artifact
 - `push-site` runs after `build-site` and pushes the artifact to the `gh-pages` (see [`push-things.yml`](#dashboard-workflows-push-things))

If we were to expand this, showing all the inputs and outputs for build-site, we
can see the process:

```{mermaid}
:name: generate-site-workflow
:alt: A flowchart that demonstrates flow of data from the hub and dashboard to the final site with the tools that build each component labelling arrows.
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
  org[/reichlab/]
  dashboard[/flusight-dashboard/]
  publish[/publish/]
  subgraph push-site
  end
  subgraph build-site
    id{{"setup run variables"}}
    checkout
    check{{"check if we need to build"}}
    bs["build-site"]
    upload["upload-artifact"]
  end
  subgraph artifacts
    org-dashboard-site[\"reichlab-flusight-dashboard-site"\]
  end
  publish --> push-site
  id --> checkout --> check --> bs --> upload --> org-dashboard-site --> push-site

  org --> id
  dashboard --> id

```


### `generate-data.yaml`

Generating the data is a little bit more involved because now

1. we are building two different data sets (one for the forecast page and one for the evals page)
2. we need to be able to access the hub's `model-outputs/`, `model-metadata/`,
   `hub-config/`, and `target-data/` folders.
3. we need to fetch any data that was previously recorded in the output branch
4. we only need the configuration files from the dashboard

To handle this, we have one job called `check` that will fetch the dashboard
repository once, compile information from the dashboard repository as outputs[^check-outputs],
and save the configuration files together in an artifact. These are used as
inputs for both the `build-evals` and `build-forecasts` jobs.

[^check-outputs]: There are [quite a few outputs for the `check`
    job](https://github.com/hubverse-org/hub-dashboard-control-room/blob/01750c9411484b51d92b884e29b8e46584208934/.github/workflows/generate-data.yaml#L52-L62)
    and we are not showing all of them here because that would overwhelm the
    diagram. Instead, we are showing a representative set of inputs that
    defines the hub and dashboard repositories and the configuration file
    artifacts. all

From there, the process is similar to the `generate-site.yaml` workflow, except
that we have a setup phase to gather information about the hub and then the
`build-evals` and `build-forecasts` jobs run in parallel.


```{mermaid}
:name: generate-data-overview
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    org[/reichlab/]
    dashboard[/flusight-dashboard/]
    publish[/publish/]
    subgraph build-data.yaml
        check["check (Setup)"]
        subgraph outputs/artifacts
            hub[/hub: cdcepi/FluSight-forecast-hub/]
            repo[/repo: reichlab/flusight-dashboard/]
            artifact[/reichlab-flusight-dashboard-cfg/]
        end
        subgraph artifacts
            eval-data[\"reichlab-flusight-dashboard-eval-data"\]
            forecast-data[\"reichlab-flusight-dashboard-forecast-data"\]
        end
        check --> outputs/artifacts
        outputs/artifacts -->|eval-ok: true| build-evals --> eval-data --> push-evals-data
        outputs/artifacts -->|forecast-ok: true| build-forecasts --> forecast-data --> push-forecasts-data
    end
    org --> check
    dashboard --> check
    publish --> push-evals-data
    publish --> push-forecasts-data
```

Both the `build-evals` and `build-forecasts` jobs have similar steps, with a few
key differences:

1. `build-forecasts` needs to provision python and install
   `hub-dashboard-predtimechart` while `build-evals` runs in a docker container
2. `build-forecasts` has two data generation steps (for forecast+config and for
   target data) while `build-evals` only has one

Taking those differences in mind, if we zoom into `build-evals`, we would find
the following process[^build-evals-process]:

[^build-evals-process]: similar to above, we are not showing all of the inputs
  because they are often redundant. Here we are highlighting the `key` variable
  that allows us to fetch and create artifacts that are specific to the build.

```{mermaid}
:name: generate-data-evals
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    repo[/repo: reichlab/flusight-dashboard/]
    hub[/hub: cdcepi/FluSight-forecast-hub/]
    key[/key: reichlab-flusight-dashboard/]
    subgraph artifacts
        eval-data[\"reichlab-flusight-dashboard-eval-data"\]
    end
    subgraph build-evals
        checkout-config["Fetch config file reichlab-flusight-dashboard-cfg"]
        check-branch{{"check for predevals/data branch"}}
        checkout-data["checkout predevals/data branch to out/"]
        clone-repo["clone hub repository to hub/"]
        build-targets["Generate scores data"]
        upload-artifact["save scores data artifact"]
    end
    key --> checkout-config --> check-branch -->|fetch == true| checkout-data --> clone-repo
    check-branch -->|fetch == false| clone-repo --> build-targets --> upload-artifact --> eval-data
    repo --> check-branch
    hub --> clone-repo
```

(dashboard-workflows-push-things)=
### `push-things.yaml`


This workflow is used by the previous two workflows and is not directly called
by the user. Its job is a three step process:

1. enforce the existence of an orphan branch to store the payload
2. checkout existing data branch
3. download the artifact containing the payload
4. push the artifact to that branch

```{mermaid}
:name: push-things
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    branch[/"branch: predevals/data"/]
    predevals/data>predevals/data]
    artifact[/artifact: reichlab-flusight-dashboard-predevals/]
    subgraph push-data
        checkout-repo-scripts["provision scripts from the dashboard control room"]
        provision["enforce the existence of predevals/data"]
        checkout-data["checkout predevals/data"]
        fetch-artifact
        publish["publish to predevals/data"]
    end
    checkout-repo-scripts --> provision --> checkout-data --> fetch-artifact --> publish --> predevals/data
    branch --> provision
    provision --> predevals/data
    predevals/data --> checkout-data
    artifact --> fetch-artifact
```
