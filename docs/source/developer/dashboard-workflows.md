# Dashboard operational workflows

:::{admonition} Required reading

You are expected to know _how_ the build process of the
dashboard works with respect to being able to identify the tools involved, the
inputs, and the outputs are. If you cannot yet identify these elements, please
go and read the [local dashboard workflow chapter](./dashboard-local.md).

We strongly recommend to look over the [Dashboard tools, operations
section](#dashboard-tools-operations) as that section contains valuable
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

## Overall workflow

While the local workflow saves the data in individual folders that all live in
the site folder, the workflows that orchestrate the dashboard build the three
components (forecast data, evaluations data, and website) separately to
individual [orphan
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
this. In this diagram, thick arrows represent `git push` events, thin arrows
represent direct data sources and dashbed arrows represent remote data sources.

Notice how similar it is to the [local-workflow](#local-workflow).

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

This is not the exact structure of the workflows, but it's a good starting
point.

### Operations from the dashboard

In practice, however, we realize that both the forecast and evals data are going
to be built a the same time, so they actually exist in the same workflow, so we
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

### Reusable workflows

The reason we can provide two workflow files with a combined total of fewer
than 100 lines of code is because we are using [Reusable
workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows).
The reusable workflow is one that is able to chain several workflows and jobs
into one single job that can be called from any repository as long as it's
public.

There are three reusable workflows in the [control room](https://github.com/hubverse-org/hub-dashboard-control-room):

1. `generate-site.yaml` builds the website and pushes it to the `gh-pages` branch
1. `generate-data.yaml` builds both the forecast and eval data and pushes them to their respective branches in parallel.
1. `push-things.yaml` pushes an to a specific branch. This is reusable workflow is only ever called by the previous two workflows.

Peering into the jobs defined in each workflow, we can see what they are doing:

#### `generate-site.yaml`

Generating the site is fairly straightforward:


```{mermaid}
:name: branch-diagram-2
:alt: A flowchart that demonstrates flow of data from the hub and dashboard to the final site with the tools that build each component labelling arrows.
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart LR
  dashboard["org/dashboard"]
  push["push-site"]
  subgraph build-site
    checkout
    bs["build-site"]
    upload["upload-artifact"]
  end
  dashboard --> checkout --> bs --> upload --> push
```

#### `generate-data.yaml`

Gen

#### `push-things.yaml`
