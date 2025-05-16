# Staging dashboard changes

This chapter deals with what to do when you are staging changes to the
dashboard. This incorporates elements from the [local dashboard
workflow](./dashboard-local.md) and the [operational
workflows](./dashboard-workflows.md), so it is _very important_ to be familiar
with these resources before reading on.

When staging dashboard changes, it is helpful to think about how the data flow
from the source to the branches, which is illustrated by the simplified diagram
below[^hub-source].

[^hub-source]: This graph is simplified in the following ways: 1. in reality,
    the inputs flow directly into the generate workflows. 2. data from the hub
    is explicitly used in the `generate-data.yaml` workflow from the control
    room, the hub is defined in `site-config.yml`

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph dashboard
        contents[/"[site contents]"/]
        site-config.yaml[/site-config.yml/]
        predtimechart-config.yaml[/predtimechart-config.yml/]
        predevals-config.yaml[/predevals-config.yml/]
        build-data.yaml
        build-site.yaml
    end
    subgraph control-room
        generate-site.yaml
        generate-data.yaml
    end
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
    contents --> build-site.yaml
    site-config.yaml --> build-site.yaml
    site-config.yaml --> build-data.yaml
    predevals-config.yaml --> build-data.yaml
    predtimechart-config.yaml --> build-data.yaml
    build-site.yaml --> generate-site.yaml --> artifacts
    build-data.yaml --> generate-data.yaml --> artifacts
    artifacts --> push-things.yaml --> dashboard-branches
```

I've arrange the diagram starting with the configuration files because in order
to know what pieces are affected by modification of a given tool, you should
start with the config file and follow the arrows.

| tool | configuration file | workflow | artifact | branch |
| :--- | :----------------- | :------- | :------- | :----- |
| hub-dash-site-builder | `site-config.yml` | `generate-site.yaml` | site | gh-pages |
| hubPredEvalsData-docker | `predevals-config.yml` | `generate-data.yaml` | eval-data | predevals/data |
| hub-dashboard-predtimechart | `predtimechart-config.yml` | `generate-data.yaml` | forecast-data | ptc/data |

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

