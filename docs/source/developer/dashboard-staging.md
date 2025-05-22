# Staging dashboard changes

:::{important}

This chapter deals with what to do when you are staging changes to the
dashboard. This incorporates elements from the [local dashboard
workflow](./dashboard-local.md) and the [operational
workflows](./dashboard-workflows.md), so it is _very important_ to be familiar
with these resources before reading on.

Staging is only appropriate after you have thoroughly confirmed with unit tests
that the changes are expected to work.

:::

## Introduction

Any change to a dashboard component that adds a new feature should be staged
before release; that is, you should test the changes on a copy of a dashboard
and confirm the results are what you expected AND that nothing adverse happens
for dashboards that opt out of new features. **This is a practice known as
[integration testing](https://www.geeksforgeeks.org/software-engineering-integration-testing/).**

**This is not an exact science and you should use your best judgement when
moving changes into production.** The dashboards do have a lot of moving
pieces, but they are not infinite and not insurmountable. This chapter should
give you a few scenarios you can use to piece together the process for
confidently adding new features or fixing critical bugs in the dashboard
workflow.

### Generic steps of workflow tools

**An important concept to understand is that [the control
room](https://github.com/hubverse-org/hub-dashboard-control-room) workflows are
just that: workflows.** They implement the same basic steps as the [local
dashboard workflow](./dashboard-local.md) and push the individual outputs to
branches of the repository. In order to do that, they use the following steps:

1. install the tool that's required
2. download the dashboard configuration file
3. download the additional resources needed
4. run the command to generate output
5. push that output to a branch

When thinking about staging the changes, it is important to remember that there
is not a one-size-fits-all process for this. You have to think holistically and
look at the changes you want to make from the perspective of a hub administrator
who just wants a dashboard for their hub that they don’t have to keep fixing or adjusting
much. From that perspective, it does not really matter how elegant the tools are
as long as the workflows can run them. What matters is that the users have
sensible defaults and options they can add or omit from their configuration
files.

:::{admonition} Examples

For example in building the forecast data, the steps are:

1. install [hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart)
2. download `predtimechart-config.yml` and `site-config.yml` from the dashboard repo
3. download the hub (defined in `site-config.yml`)
4. run `ptc_generate_target_json_files` and `ptc_generate_json_files`
5. save the output in the `ptc/data` branch and push it

similarly, for building the site, the steps are:

1. launch an interactive shell in a container based on  the [hub-dash-site-builder](https://github.com/hubverse-org/hub-dash-site-builder) Docker image.
2. download `site-config.yml` from the dashboard repo
3. download the dashboard repo contents
4. run `render.sh`
5. save the output in the `gh-pages` branch and push it

:::

### Data flow

When staging dashboard changes, it is helpful to think about how the data flow
from the source to the branches in [the control
room](https://github.com/hubverse-org/hub-dashboard-control-room), which is
illustrated by the diagram below[^hub-source].

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

I've arranged the diagram starting with the configuration files because **in order
to know what pieces are affected by modification of a given tool, you should
start with the config file** and follow the arrows.

| configuration file  | tool | workflow | artifact | branch |
| :-----------------  | :--- | :------- | :------- | :----- |
| `site-config.yml`  | hub-dash-site-builder | `generate-site.yaml` | site | gh-pages |
| `predevals-config.yml`  | hubPredEvalsData-docker | `generate-data.yaml` | eval-data | predevals/data |
| `predtimechart-config.yml`  | hub-dashboard-predtimechart | `generate-data.yaml` | forecast-data | ptc/data |

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

Sometimes a fix is urgent enough that you need to deploy without running through
the staging. It's okay to do this if the change is small enough, but for large
changes, you must stage the changes and verify that it works.

:::


(dashboard-staging-where)=
## Where to stage changes

Depending on the type of change happening, you have, broadly two options to
stage the changes locally or in a remote build. In general, if nothing changes
about _how_ the resource is built or provisioned, then you can do local staging.

(dashboard-staging-option1)=
### Option 1: local staging

This option is ideal for **changes that do not affect _how_ the resource is
built or provisioned.** Doing local staging involves the same steps as the
[local workflow](./dashboard-local.md) except that you would install the development version of the tool
you are testing.

:::{admonition} Local staging example

For example, if you add a new option to `predtimechart-config.yml`, you would
follow this process:

1. implement change in new branch of
   [hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart)
   and install locally.
2. create a local copy of a dashboard repository and the hub it points to
3. [generate the forecasts data](#dashboard-local-forecasts) with the
   appropriate command
4. inspect the output (check that no files are missing or added)
5. [generate the site and preview](#dashboard-local-site) (NOTE: If the
   JavaScript component also changes, you will need to [post-edit the
   javascript components](#staging-javascript))
6. add the new option to `predtimechart-config.yml` and repeat steps 3--5.

:::

The following sections will cover local staging strategies based on what
component you are modifying. Note that you will often have to mix
testing strategies.

(staging-javascript)=
#### In JavaScript tools

**The JavaScript tools [PredTimeChart](https://github.com/reichlab/predtimechart)
and [PredEvals](https://github.com/hubverse-org/predevals) are both tools that
can be staged locally.** For either of the tools, the steps to perform local
staging is:

1. create a new branch to implement the change
2. implement the change and get a passing review on your pull request
3. download the `gh-pages` branch of [any dashboard
   repository](https://hubverse.io/tools/dashboards.html#examples) to your
   local machine
4. edit the first line of `resources/predtimechart.js` or
   `resources/predevals_interface.js` so that the app pulls from your branch or
   commit:
   ```{code-block} diff
   -import App from 'https://cdn.jsdelivr.net/gh/reichlab/predtimechart@v3/dist/predtimechart.bundle.js';
   +import App from 'https://cdn.jsdelivr.net/gh/reichlab/predtimechart@<branch-name>/dist/predtimechart.bundle.js';
   ```
5. in the root of the folder, run `python -m http.server 8080` and open a
   browser to <http://localhost:8080>
6. inspect the page and make sure that the page behaves as you expect.

The reason why these JavaScript tools can be staged locally is because they are
loaded when someone visits the site. The site builder does not know anything
about the underlying JavaScript.

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph site
        forecast.html
        eval.html
        subgraph resources
            predtimechart.js
            predevals_interface.js
        end
    end
    hub-dash-site-builder -..->|render.sh| site
    forecast.html -->|calls| predtimechart.js -->|loads| predtimechart["reichlab/predtimechart@v3"]
    predtimechart.js -->|fetches| ptc/data[(ptc/data)]
    predtimechart.js -->|updates| forecast.html
    eval.html -->|calls| predevals_interface.js -->|loads| predevals["hubverse-org/predevals@v1"]
    predevals_interface.js -->|fetches| predevals/data[(predevals/data)]
    predevals_interface.js -->|updates| eval.html
```

:::{admonition} Purge the cache on release of JavaScript modules
:class: important


The JavaScript components we provide to the webpage are known as _version
aliased_ URLs, which, at the time of writing, is signified by the `@v3` for PredTimeChart or `@v1` for
PredEvals. This means that the sites will always get the latest version up to
that major version number. For example, if we release version 1.1.0 of PredEvals,
then the users downstream will have that version delivered via the CDN, but if
we turn around and release version 2.0.0, they will still get the 1.1.0 version.

When you release a JavaScript module, <https://cdn.jsDeliver.com> will pick it
up within 12 hours, but user machines can keep it cached for up to seven days.

If you want your changes to show up near instantly, you can [purge jsDeliver's CDN cache](https://www.jsdelivr.com/tools/purge) by entering two URLs.

The way to do this is to **paste the URLs in the browser and replace `cdn` with `purge`**.
Note that you also need to do this for **the un-versioned URL** as well:

```{code-block}
:caption: URLs to clear the cache for PredTimeChart: copy and paste into your browser
https://purge.jsdelivr.net/gh/reichlab/predtimechart@v3/dist/predtimechart.bundle.js
https://purge.jsdelivr.net/gh/reichlab/predtimechart/dist/predtimechart.bundle.js
```

```{code-block}
:caption: URLs to clear the cache for PredEvals: copy and paste into your browser
https://purge.jsdelivr.net/gh/hubverse-org/predevals@v1/dist/predevals.bundle.js
https://purge.jsdelivr.net/gh/hubverse-org/predevals/dist/predevals.bundle.js
```

:::


#### Accessing pre-built data

The data generation workflows may take into account data that have already been
generated in order to save computational time. When you are staging locally, it
is a good idea to mimic the state of the control room as best you can.

Unlike the local workflow, the remote workflow stores the data in separate
orphan branches that do not share history with the main branch of the
repository. You can keep these branches local by using a [**git
worktree**](https://git-scm.com/docs/git-worktree). This is a strategy that we
use in the [site builder
tests](https://github.com/hubverse-org/hub-dash-site-builder/blob/77f40021cfb473cbcf2c9986b6aa518af13d863d/tests/run.sh#L94-L95).


The pattern to add a git worktree is:

```bash
git worktree add --checkout <directory> <branch>
```

```{code-block} bash
:emphasize-lines: 4-5
git clone https://github.com/reichlab/metrocast-dashboard.git
cd metrocast-dashboard
mkdir -p data/
git worktree add --checkout data/ptc ptc/data
git worktree add --checkout data/predevals predevals/data
```

From here, you can generate the data and you can use git to see what changed.


```bash
tmp=$(mktemp -d)
git clone https://github.com/reichlab/flu-metrocast.git "${tmp}"
mkdir -p data/ptc/forecasts
ptc_generate_json_files \
  "${tmp}" \
  predtimechart-config.yaml \
  data/ptc/predtimechart-options.json \
  data/ptc/forecasts
```

When you are done, you can remove the worktrees with

```bash
rm -rf data/
git worktree prune
```

(dashboard-staging-option2)=
### Option 2: remote staging

This option is necessary for **changes that modify workflows, affect _how_
the resource is built, and how the resource is provisioned**. Again, the root of
this process is based in the local workflow, but now you also have to effectively
make a copy of the dashboard AND a copy of the control room and connect them to
the right places.

:::{caution}

This process is the most involved and it requires careful planning. If you want
to avoid stepping into this process, the solution is to not make changes to the
public interface to your application. If you want to update something to allow
people to opt-in or opt-out of something, make it configurable via the
configuration file.

:::

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph control-room
        cro>"control-room (@main)"]
        crf>"control-room (@test)"]
    end
    dash["dashboard"]
    site>"dashboard@gh-pages"]
    dashf["user/dashboard"]
    sitef>"user/dashboard@gh-pages"]
    art[\"artifact"\]
    artf[\"artifact"\]
    subgraph tool
        toolv>"tool (@v1.1.1)"]
        toolf>"tool (@main)"]
    end
    dash --> cro
    toolv --> cro
    cro --> art --> site
    toolf --> crf
    dashf --> crf
    crf --> artf -->sitef
```

:::{admonition} Remote staging example

For example in late March 2025, we wanted to update the site builder to [v1.0.0](https://github.com/hubverse-org/hub-dash-site-builder/releases/tag/v1.0.0). This changed the interface so
instead of positional BASH arguments, we used argument flags:

```{code-block} bash
:caption: before, positional arguments
bash /render.sh "$OWNER" "$REPO" "ptc/data" "" "$HAS_FORECASTS"
```

```{code-block} bash
:caption: after, named arguments
render.sh -u "$OWNER" -r "$REPO"
```

In order to test this, we needed to do the following

1. build the image from the main branch
2. create a branch in the control room that would reference this image and modify the commands
3. create a fork of a dashboard that would point to this new branch in the control room


After merging [the updated dockerfile with new tests and interface](https://github.com/hubverse-org/hub-dash-site-builder/pull/21) into the main branch of the repository, I created the docker image from the main branch by using the [Create, Test, and Publish Docker Image workflow](https://github.com/hubverse-org/hub-dash-site-builder/actions/workflows/build-container.yaml). Note that this docker image has the `main` tag[^image-name], but it is not published.

[^image-name]: This was before we had fully ironed out the details of the docker publishing workflow, so the image tag is actually `znk-dispatch-fix-34`. I am writing this as if we had the workflow that we have now.

Once I did that, I opened [hubverse-org/hub-dashboard-control-room#59](https://github.com/hubverse-org/hub-dashboard-control-room/pull/59) and then modified the workflow to use the new container and the new interface (see [hubverse-org/hub-dashboard-control-room@58628f0f4](https://github.com/hubverse-org/hub-dashboard-control-room/pull/59/commits/58628f0f4cef7e5c2cb5dc9455dc63235f47ec1d)).

I created a fork of the dashboard repositories and changed their `build-site.yaml` workflows to use the branch I was testing[^testing-branch]

[^testing-branch]: In this process, I did not create any forks. Instead, I [modified the workflow for the
    app](https://github.com/hubverse-org/hub-dashboard-control-room/pull/59/commits/12c41a279fdcf70a8dde9878367edbc22690ae3b), ran it without pushing, and inspected the artifacts. This had the same
    effect, but meant that I could test several repositories at once.

```diff
-uses: hubverse-org/hubverse-org/hub-dashboard-control-room/.github/workflows/generate-site.yaml@main
+uses: hubverse-org/hubverse-org/hub-dashboard-control-room/.github/workflows/generate-site.yaml@znk/use-release-hsdb/58
```

I then ran the workflows from the dashboard forks to confirm that the site was correctly generated.

:::

:::{admonition} Staging without forks with the GitHub App
:class: note
:name: dashboard-staging-app

One tool that can help with staging is
[hubDashboard](https://github.com/apps/hubDashboard). It was originally
designed so that hub administrators could have a dashboard website without
needing to maintain GitHub workflows. We no longer use it for this purpose.

The app does two things:

1. any repository owner can "install" the app on their repository, giving it
   permissions to read and write repository contents
2. we can authenticate as the app in the control room, and use it to generate a
   temporary github PAT that will give us permissions to push to a repository
   that has the app installed. We control a list of [known hubs](https://github.com/hubverse-org/hub-dashboard-control-room/blob/main/known-hubs.json) that have the app installed.

Because of this, we have the following pattern:

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
    subgraph repo-flow
        subgraph dashboard
            d[dashboard workflows]
            s[dashboard-site]
            t[token]
        end
        d[dashboard] -->|uses| c[control-room] -->|builds to| s
        d[dashboard] -->|generates|t -->|used by| c
    end
    subgraph app-flow
        app -->|installed on| dashboard
        app -->|generates|token-->|used by| c
        c -->|builds to| s
    end
```

:::


The following sections will cover remote staging strategies based on what
component you are modifying working. Note that you will often have to mix
testing strategies.

(staging-control-room)=
#### In the control room

There are three situations that you will find yourself staging,

1. updates affecting [the control room generate workflows](#staging-control-room-generate)
2. updates affecting [the control room `push-things.yaml` workflow](#staging-control-room-push)
3. updates affecting [the control room scripts](#staging-control-room-scripts)


(staging-control-room-generate)=
##### Control room `generate-` workflows

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
##### Control room `push-things.yaml` workflow

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
##### Control room scripts

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

(staging-tools-ptc)=
#### hub-dashboard-predtimechart

To stage changes to the hub-dashboard-predtimechart from the control room:

1. implement change in new branch of
   [hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart)
2. create new branch in the control room and modify
   [`generate-data.yaml`](https://github.com/hubverse-org/hub-dashboard-control-room/tree/main/.github/workflows/generate-data.yaml) so that it points to your branch instead of `$latest`:
   ```diff
   - pip install "git+https://github.com/hubverse-org/hub-dashboard-predtimechart@$latest"
   + pip install "git+https://github.com/hubverse-org/hub-dashboard-predtimechart@<branch-name>"
   ```
3. fork a dashboard repository, point its workflows to the new control room
   branch
4. generate the data
5. generate the site and preview (NOTE: If the JavaScript component also
   changes, you will need to preview the site locally)
6. add the new option and repeat steps 4 and 5

If you do not need to change any options in the control room, then you can
delete the control room branch and the dashboard fork. However, **if arguments change**,
then there will be a period of time that the workflows will not work because you
need to release the update AND you need to update the control room right after.
To ensure things go smoothly, use the following steps:

0. **plan a time for the release and optionally announce it**
1. release the new version hub-dashboard-predtimechart
2. reset the control room's branch reference to hub-dashboard-predtimechart to be `$latest` (yes, the dollar sign is important for the workflow)
3. reset any the references to the reusable workflows back to `@main`
4. merge the control room branch to main and it will be live

(staging-tools-predevals)=
#### hubPredEvalsData-docker

To stage changes to hubPredEvalsData-docker from the control room:

1. implement change in
   [hubPredEvalsData-docker](https://github.com/hubverse-org/hubPredEvalsData-docker)
   and push to the `main` branch after testing.
2. publish a new image from the main branch (note that only tags will create an official release, so this is safe to do)
2. create new branch in the control room and modify
   [`generate-data.yaml`](https://github.com/hubverse-org/hub-dashboard-control-room/tree/main/.github/workflows/generate-data.yaml) so that it points to the `main` branch instead of `latest`:
   ```diff
    runs-on: ubuntu-latest
    container:
   -  image: ghcr.io/hubverse-org/hubpredevalsdata-docker:latest
   +  image: ghcr.io/hubverse-org/hubpredevalsdata-docker:main
      ports:
        - 80
      volumes:
        - ${{ github.workspace }}:/project
   ```
3. fork a dashboard repository, point its workflows to the new control room
   branch
4. generate the data
5. generate the site and preview (NOTE: If the JavaScript component also
   changes, you will need to preview the site locally)
6. add the new option and repeat steps 4 and 5

If you do not need to change any options in the control room, then you can
delete the control room branch and the dashboard fork. However, **if arguments change**,
then there will be a period of time that the workflows will not work because you
need to release the update AND you need to update the control room right after.
To ensure things go smoothly, use the following steps:

0. **plan a time for the release and optionally announce it**
1. release the new version hubPredEvalsData-docker
2. reset the control room's branch reference to hubPredEvalsData-docker to be `:latest`
3. reset any the references to the reusable workflows back to `@main`
4. merge the control room branch to main and it will be live


(staging-tools-stie)=
#### hub-dash-site-builder

To stage changes to hub-dash-site-bulder from the control room:

1. implement change in
   [hub-dash-site-bulder](https://github.com/hubverse-org/hub-dash-site-bulder)
   and push to the `main` branch after testing.
2. publish a new image from the main branch (note that only tags will create an official release, so this is safe to do)
2. create new branch in the control room and modify
   [`generate-site.yaml`](https://github.com/hubverse-org/hub-dashboard-control-room/tree/main/.github/workflows/generate-site.yaml) so that it points to the `main` branch instead of `latest`:
   ```diff
    runs-on: ubuntu-latest
    container:
   -  image: ghcr.io/hubverse-org/hub-dash-site-builder:latest
   +  image: ghcr.io/hubverse-org/hub-dash-site-builder:main
      ports:
        - 80
      volumes:
        - ${{ github.workspace }}:/project
   ```
3. fork a dashboard repository, point its workflows to the new control room
   branch
4. (optional) generate the data
5. generate the site and preview (NOTE: If the JavaScript component also
   changes, you will need to preview the site locally)
6. add the new option and repeat step 5

If you do not need to change any options in the control room, then you can
delete the control room branch and the dashboard fork. However, **if arguments change**,
then there will be a period of time that the workflows will not work because you
need to release the update AND you need to update the control room right after.
To ensure things go smoothly, use the following steps:

0. **plan a time for the release and optionally announce it**
1. release the new version hub-dash-site-bulder
2. reset the control room's branch reference to hub-dash-site-bulder to be `:latest`
3. reset any the references to the reusable workflows back to `@main`
4. merge the control room branch to main and it will be live

