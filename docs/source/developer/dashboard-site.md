# Generating the Dashboard Website

The [dashboard website
builder](https://github.com/hubverse-org/hub-dash-site-builder) is a thin
wrapper around [the quarto publishing system](https://quarto.org) and
[yq](#dashboard-tool-yq). This tool was designed under the following
motivations:

1. Maintenance of this dashboard should be independent from hub maintenance.
2. Anyone should be able to deploy a dashboard as long as they have a hub with
   target data that they can access.
3. Knowledge of any particular website generator is not required.

## Sources and sinks

The website that is built is a fully static site that can be viewed locally. It
is the result of a combination of two sources, the
[dashboard website builder `static/` directory](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/static) and [the dashboard repository](https://github.com/hubverse-org/hub-dashboard-template/).

For example, the [source for the hub-dashboard-template website](https://github.com/hubverse-org/hub-dashboard-template/tree/gh-pages), shows the following files and folders.

| site component | from site builder | from user |
| :-------- | :---------------- | :-------- |
| Menu Items | `static/_quarto.yml` | `site-config.yml` |
| Theme      | `static/_quarto.yml` | `site-config.yml` |
| `index.html` | | `pages/index.qmd` |
| `about.html` | | `pages/about.md` |
| `data.html` | | `pages/data.qmd` |
| `img/` | | `pages/img` |
| `eval.html` | `static/eval.qmd` | |
| `forecast.html` | `static/eval.qmd` | |
| `resources/` | `static/resources/` | |
| `site_libs` | `static/_quarto.yml` | `site-config.yml` |

The site builder effectively performs three steps to render the site:

1. copy the contents of `static/` into `pages/`
2. merge `site-config.yml` into `_quarto.yml`
3. run `quarto render`
