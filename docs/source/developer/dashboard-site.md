# Generating the Dashboard Website

The [dashboard website
builder](https://github.com/hubverse-org/hub-dash-site-builder) is a [docker
image](#dashboard-tool-docker) which is thin wrapper around [the quarto
publishing system](#dashboard-tool-yq) and [yq](#dashboard-tool-yq). This tool
was designed under the following motivations:

1. Maintenance of this dashboard should be independent from hub maintenance.
2. Anyone should be able to deploy a dashboard as long as they have a hub with
   target data that they can access.
3. The only knowledge anyone should need is of Markdown, YAML, and basic
   operation of GitHub workflows. Knowledge of any particular [website
   generator](https://jamstack.org/generators/) is not required and the user
   should not need to handle any templating that cannot be easily automated.
4. We should not have to maintain a server to deploy these sites.


## Installation

You can install the latest version of this tool with docker:

```bash
docker pull ghcr.io/hubverse-org/hub-dash-site-builder:latest
```

(dashboard-site-source)=
## How the website is built (a tale of two sources)

The website that is built is a fully static site that can be viewed locally. It
is the result of a combination of two sources:

1. [dashboard website builder `static/` directory](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/static) and,
2. [the dashboard repository](https://github.com/hubverse-org/hub-dashboard-template/)

### Configuring the site

#### Minimal configuration

At the bare minimum, a dashboard source repository should contain two files:

 1. `site-config.yml` that has two required fields:
    - `hub`, the name of the hub
    - `pages`, a list of files in `pages/` to include, which should have `index.qmd`.
 2. `pages/index.qmd`

These two files will create a website that has a single page and is,
admittedly, not very useful other than providing basic information about a hub
with a link to it. However, the user has different options available to them.

#### Options for the site

 - **Forecasts**: if the user includes a [`predtimechart-config.yml`
   file](#dashboard-ptc), then the dashboard will include a forecast
   page.
 - **Evaluations**: if the user includes a [`predevals-config.yml`
   file](#dashboard-predevals-config), then the dashboard will include an
   evaluations page.
 - **Additional pages**: Any additional files included in `pages/` will be
   included in the site, so long as they are also declared in the
   `site-config.yml` file (described in detail in [Customizing the dashboard
   website](#dashboard-customization)).

For example, the [dashboard template](https://github.com/hubverse-org/hub-dashboard-template)
contains the following files:

- `site-config.yml`
- `pages/index.qmd` --- home page
- `pages/about.md` --- about the hub staff
- `pages/data.qmd` --- how to access data from S3[^pages-data]
- `pages/img/` --- images for the about page
- `predtimechart-config.yml`
- `predevals-config.yml`

[^pages-data]: This is an optional page for cloud-enabled hubs. The user has to
    manually add the S3 bucket name to the YAML header or delete this file if
    it's not relevant. This would normally be a page similar to the forecast
    and eval pages (i.e. generated optionally by the site builder). Since the
    hub administrator may want to add additional information or rephrase some
    elements, we left it as a boilerplate instead of attempting to try to code
    a situation where we have a partial template and join pages together.

When the site is rendered, you can see [source for the hub-dashboard-template
website](https://github.com/hubverse-org/hub-dashboard-template/tree/gh-pages),
shows the following files and folders.

| site component | from site builder | from user | optional |
| :-------- | :---------------- | :-------- | ------- |
| Menu Items | `static/_quarto.yml` | `site-config.yml` | no  |
| Theme      | `static/_quarto.yml` | `site-config.yml` | yes |
| `index.html` | --- | `pages/index.qmd` | no |
| `about.html` | --- | `pages/about.md` | yes |
| `data.html` | --- | `pages/data.qmd` | yes |
| `img/` | --- | `pages/img` | yes |
| `eval.html` | `static/eval.qmd` | `predevals-config.yml` | yes |
| `forecast.html` | `static/eval.qmd` | `predtimechart-config.yml` | yes |
| `resources/` | `static/resources/` | --- | no |
| `site_libs` | `static/_quarto.yml` | --- | no |

### An incomplete boilerplate

On its own, the `static/` directory of the dashboard site builder contains an
incomplete quarto website. The incomplete parts are:

1. `index.qmd` is missing
2. The JavaScript in `resources/` is incomplete. There is a single line that
   defines the root folder for resource access, with a placeholder called
   `{ROOT}`, which needs to be replaced by a local folder or URL for the
   resource:
   ```js
   const root = "{ROOT}";
   ```

The site builder image effectively performs four steps to complete and render
the site:

1. Combine the contents of `pages/` and `/static/` into a temporary directory, `/tmp/`.
2. Use `yq` to merge `site-config.yml` into `/tmp/_quarto.yml`.
3. Update the JavaScript files to point to the correct resources or discard unused files.
4. Run `quarto render /tmp/` and copy the output to the output directory (`out/`).

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
  subgraph dashboard
    pages/contents["pages/[contents]"]
    site-config.yml
    out/
  end
  subgraph docker
    subgraph /static/
        /static/contents["/static/[contents]"]
        /static/_quarto.yml["/static/_quarto.yml"]
    end
    yq{{"yq"}}
    subgraph /tmp/
        _quarto.yml["/tmp/_quarto.yml"]
        contents["/tmp/[contents]"]
        _site/["/tmp/_site/"]
        quarto{{"quarto"}}
    end
  end
  pages/contents --> contents
  site-config.yml --- yq
  /static/contents --> contents
  /static/_quarto.yml --- yq
  yq -->|yq -i '...' _quarto.yml | _quarto.yml
  _quarto.yml --> quarto
  contents --> quarto
  quarto -->|quarto render /tmp/| _site/ --> out/
```

The entirety of these steps are performed by [the `render.sh` script](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/render.sh), which exists
in the docker container as an executable.

### Optional Components

Hubs do not have to have data that are compatible with the forecast
visualization or evaluations to build a website. Case in point:
<https://reichlab.io/variant-nowcast-hub-dashboard/>. This dashboard does not
have the Forecast or Evals page. Instead, it has self-generated reports.

If a hub does not want to build either the forecast or evaluations pages, they
can omit the predevals or predtimechart config files. When this happens, the
site builder will remove these pages and the associated resources before
building the quarto site.

## How the visualizations work

If the dashboard is built independent from the data generation, how do the
visualizations work? They work because the visualization pages each call a
script that loads either predtimechart or predevals with a JavaScript function
that is designed to fetch data for these modules. All of the work of fetching
the data is done by the browser, but this does require data to exist.

For public hubs, these data live on a separate branch that we can access via
a `raw.githubusercontent.com` URL. For private hubs, data can be built locally
and bundled with the site.


## How the image is built

The images is built using GitHub actions and [deployed to GitHub's container registry](https://github.com/hubverse-org/hub-dash-site-builder/pkgs/container/hub-dash-site-builder/406574245?tag=latest).

We initially cribbed the build workflow from [GitHub's Publishing Docker images
guide](https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-docker-images#publishing-images-to-github-packages),
but we also wanted to be able to test the image and only publish when we
created a tag or release AND we wanted to be mindful of good security practices
with GitHub workflows (especially with respect to the principle of least
permission).

The workflow that we came up with is called [build-container.yaml](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/.github/workflows/build-container.yaml) and it contains three jobs:

### Build image

- **purpose**: build and test the docker image and then save it as an artifact
- **permissions**: read-all
- **runs on**: pull request, push to main, tags that start with `v`, and manual
  trigger.

There is a bit of a dance that's required for this job to run, which is
described in GitHub's Publishing Docker images guide (see above for link).
The reason for this dance is so we can extract metadata for the image.

The important bit is the "Build and export" step, which builds the docker image
on the GitHub runner and saves it as a tar file. The image is then loaded and
tested against the reichlab/flusight-dashboard. At the end, assuming all tests
pass, the image is uploaded as an artifact.

### Test

- **purpose**: test the built docker image against the tests from the main branch.
- **permissions**: read-all
- **runs on**: pull request, and manual trigger not on main branch.

This job is needed to ensure the tests from the main branch continue to work and
are there to prevent potentially malicious pull requests from forcing tests to
pass. It has two steps:

1. fetch the image artifact
2. load and test the artifact against the tests as they exist on the main branch.

This is not run from the main branch or on a tag because by this time, the tests
from the build image job will be redundant.

### Publish

- **purpose**: publish the built docker image
- **permissions**: read-all
- **runs on**: push of a tag that starts with "v" and a workflow dispatch from
  main where "publish" is selected

This is similar to the build image except that instead of building the image,
we are loading it from an artifact and pushing it to the registry.

The final step of this job is to generate an artifact attestation, which is a
way to provide a build provenance for downstream validation.


## Testing

The running container can be tested with [the `tests/run.sh`
script](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/tests/run.sh).

These tests are not written with any specific framework in mind, but they record
the number of tests and count the number that fail. If the number that fail is
zero, then the script returns with status code 0, otherwise, it returns with
status code 1, which is an error.


## References

Here are links to some concepts that are used in the website builder.

- [Building a website using quarto](https://quarto.org/docs/websites/)
- [BASH scripting cheat sheet](https://devhints.io/bash)
- `yq` [tips and tricks](https://mikefarah.gitbook.io/yq/usage/tips-and-tricks)
  and [recipes](https://mikefarah.gitbook.io/yq/recipes). Specific operators
  can be found in the comments of the
  [`modify-quarto-yml.sh`](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/modify-quarto-yml.sh)
  file in the hub-dash-site-builder repository.
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
