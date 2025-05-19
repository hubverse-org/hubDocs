# Staging dashboard changes

## Introduction

This chapter deals with what to do when you are staging changes to the
dashboard. This incorporates elements from the [local dashboard
workflow](./dashboard-local.md) and the [operational
workflows](./dashboard-workflows.md), so it is _very important_ to be familiar
with these resources before reading on.

When staging dashboard changes, it is helpful to think about how the data flow
from the source to the branches, which is illustrated by the diagram
below[^hub-source].

[^hub-source]: This graph is simplified in the following ways: 1. The local
    dashboard workflows, which call the control-room workflows are excluded from
    this diagram because they act as a messenger, passing data downstream. 2. The
    artifacts and branches generated from the workflows are performed in
    parallel; generate-site.yaml generates the `site` and `gh-pages` artifact
    and branch while generate-data.yaml generates the rest.

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph dashboard
        contents[/"[site contents]"/]
        site-config.yaml[/site-config.yml/]
        predtimechart-config.yaml[/predtimechart-config.yml/]
        predevals-config.yaml[/predevals-config.yml/]
    end
    generate-site.yaml
    generate-data.yaml
    subgraph artifacts
        site[\site\]
        eval-data[\eval-data\]
        forecast-data[\forecast-data\]
    end
    subgraph dashboard-branches
        gh-pages>gh-pages]
        predevals/data>predevals/data]
        ptc/data>ptc/data]
    end
    subgraph tools
        hub-dash-site-builder
        hub-dashboard-predtimechart
        hubPredEvalsData-docker
    end

    dashboard ~~~ tools
    site-config.yaml ~~~ tools
    predevals-config.yaml ==> generate-data.yaml
    predtimechart-config.yaml ==> generate-data.yaml

    contents -.-> generate-site.yaml
    site-config.yaml ==> generate-site.yaml
    site-config.yaml -.-> hub -.-> generate-data.yaml
    hub-dash-site-builder --> generate-site.yaml

    hub-dashboard-predtimechart --> generate-data.yaml
    hubPredEvalsData-docker --> generate-data.yaml

    generate-site.yaml --> artifacts
    generate-data.yaml --> artifacts

    generate-site.yaml ==> push-things.yaml
    generate-data.yaml ==> push-things.yaml

    artifacts -.-> push-things.yaml ==> dashboard-branches
```

I've arrange the diagram starting with the configuration files because **in order
to know what pieces are affected by modification of a given tool, you should
start with the config file** and follow the arrows.

| configuration file  | tool | workflow | artifact | branch |
| :-----------------  | :--- | :------- | :------- | :----- |
| `site-config.yml`  | hub-dash-site-builder | `generate-site.yaml` | site | gh-pages |
| `predevals-config.yml`  | hubPredEvalsData-docker | `generate-data.yaml` | eval-data | predevals/data |
| `predtimechart-config.yml`  | hub-dashboard-predtimechart | `generate-data.yaml` | forecast-data | ptc/data |

## Broad steps for staging changes

The process for staging changes looks a bit different depending on where you are
in the workflow. There are broad steps that should be followed, depending on
what you are changing.

### In the control room

Unless you are staging a patch update to a frontend tool that runs in the browser,
part of the staging will take place in [the control room](https://github.com/hubverse-org/hub-dashboard-control-room). There are three situations that you will find yourself staging,

1. updates affecting [the control room generate workflows](#staging-control-room-generate)
2. updates affecting [the control room `push-things.yaml` workflow](#staging-control-room-push)
3. updates affecting [the control room scripts](#staging-control-room-scripts)


(staging-control-room-generate)=
#### Control room `generate-` workflows

If you are modifying one of the `generate-data.yaml` or `generate-site.yaml`
workflows in the control room, then:
1. create a branch in the control room
2. make the changes you need to change
3. (**in a fork of a dashboard repository**), change the
   `@main` tag for the reusable workflow to `@<branch-name>`
   ```diff
   -uses: hubverse-org/[...]/workflows/generate-site.yaml@main
   +uses: hubverse-org/[...]/workflows/generate-site.yaml@<branch-name>
   ```
4. inspect the resulting page and artifacts

(staging-control-room-push)=
#### Control room `push-things.yaml` workflow

This builds off of the [the control room generate workflows](#staging-control-room-generate).
1. create a branch in the control room
2. make the changes you need to change
4. (**in the control room**) In the `generate-*` workflows, change the `push-things.yaml` workflows to use `@<branch-name>`:
   ```diff
   -uses: hubverse-org/[...]/workflows/push-things.yaml@main
   +uses: hubverse-org/[...]/workflows/push-things.yaml@<branch-name>
   ```
4. (**in a fork of a dashboard repository**), change the
   `@main` tag for the reusable workflow to `@<branch-name>`
   ```diff
   -uses: hubverse-org/[...]/workflows/generate-site.yaml@main
   +uses: hubverse-org/[...]/workflows/generate-site.yaml@<branch-name>
   ```
5. inspect the resulting page and artifacts

(staging-control-room-scripts)=
#### Control room scripts

If a script changes, it builds off of the [the control room `push-things.yaml` workflow](#staging-control-room-push):
1. create a branch in the control room
2. make the changes you need to change
4. (**in the control room**) In the `generate-*` workflows, change the `push-things.yaml` workflows to use `@<branch-name>`:
   ```diff
   -uses: hubverse-org/[...]/workflows/push-things.yaml@main
   +uses: hubverse-org/[...]/workflows/push-things.yaml@<branch-name>
   ```
4. (**in the control room**) In the `push-things.yaml` workflow, modify the `ref` key of the `checkout-this-here-repo-scripts` step:
   ```{code-block} yaml
   :lineno-start: 60
   :emphasize-lines: 6
   :caption: the `ref` key should point to the new branch
        steps:
          - id: checkout-this-here-repo-scripts
            uses: actions/checkout@v4
            with:
              repository: hubverse-org/hub-dashboard-control-room
              ref: <branch-name>
              persist-credentials: false
              sparse-checkout: |
                scripts
   ```
4. (**in a fork of a dashboard repository**), change the
   `@main` tag for the reusable workflow to `@<branch-name>`
   ```diff
   -uses: hubverse-org/[...]/workflows/generate-site.yaml@main
   +uses: hubverse-org/[...]/workflows/generate-site.yaml@<branch-name>
   ```
5. inspect the resulting page and artifacts

### In the toolchain


## What does it mean to stage changes?

The concept of staging changes is the same as a dress rehearsal for a play. You
get all the players together and execute the performance exactly as you would if
an audience were there. You are confirming everything is operating as expected
and providing room for improvements if things go awry.

Similarly, since the dashboard is automatically deployed to any repository that
uses it, it is important to confirm that changes to any components produce
expected results and do not break the dashboards in production. To confirm
this, it is important to create a branch in the control room that implements
the changes and temporary dashboard website to preview. This website should
adhere to these three descriptors:

1. its workflows should point to an in-development branch of the control room
2. it should implement any configuration file changes if necessary
3. it should be relatively quick to test

Once that is set up, you can let the website build and confirm that you are
seeing the output you expect and confirm that you are not seeing any unexpected
artifacts or behavior.

## When to stage changes

You will need to stage changes when any of the tools produces results whose
structures diverge significantly from the output of the latest versions of the
dashboard tools. The judgement of what a significant divergence is can be
subjective, but a pretty clear checklist to consult is:

 1. Is there a new option that is available from the configuration file?
 1. Does the tool generate new files?
 1. Is a previously required option becoming optional?
 1. Are the arguments for the reusable workflows changing?
 1. Is a previously optional option becoming required? _(breaking)_
 1. Is the structure of the generated files changing? _(breaking)_

**If the answer to any of the above questions is yes, then you need to stage
changes before pushing a release.**

:::{admonition} Not all changes need to be staged
:class: note

You might be able to think of situations that were not mentioned above. For
example, addressing a bug fix for something that can easily be verified with
internal tests does not absolutely need to fully stage changes for deployment.

Another situation is if the arguments for the underlying tools change, but
nothing about the input or output data change. Because everything is
encapsulated in the GitHub workflows, it is sufficient to test the workflows
using the GitHub app to confirm it works.

Sometimes a fix is urgent enough that you need to deploy without running through
the staging. It's okay to do this if the change is small enough, but for large
changes, you must stage the changes and verify that it works.

:::

## Elements you can inspect

There are two methods to verify that your changes are having the effect you want,
inspecting the artifacts and previewing the website.

### Inspecting the artifacts

This method is the least invasive because you can run the workflows as a "dry
run" and then download the github artifacts to make sure they look the way they
should. If no configuration files need to change, this can be done directly from
the control room with the hubDashboard GitHub app.

If it's data that are changing, you can even use the artifacts to preview the
website locally.

### Previewing the website on a fork

There are some situations where you want to preview the website on a fork of a
dashboard. You might want to do this if you have a breaking change and you need
to modify a config file. This is more involved.

## Performing the staging

In order to stage changes, you need to identify what needs to be modified.

## Using the app to generate artifacts

## Using a fork of a dashboard

