# Dashboards

The hubverse provides a modular system for building a dashboard website for a modeling hub. This includes three main components:

1. A system for creating a website with multiple pages by creating a set of markdown files with site contents and a yaml file specifying configuration settings. This is based on the [quarto publishing system](https://quarto.org/).
2. An optional module for interactive visualizations of model outputs (predictions) and target data.
3. An optional module for interactive exploration of scores for model predictions.

The website contents, including the web pages as well the data backing interactive visualizations and evaluations, are built by GitHub actions that can be set to run on a regular schedule or manually as needed. By default, the website is hosted on a GitHub pages site, though it could also be hosted on another static website hosting platform if desired.

Below, we describe how to set up each of these three components.

## Quickstart -- Building a Dashboard

The Hubverse provides a [template dashboard repository](https://github.com/hubverse-org/hub-dashboard-template) to facilitate the process of setting up a dashboard for a modeling hub. Use this template to create a dashboard repository for your hub by clicking the "Use this template" button near the top right of the GitHub page for the template:

```{figure} ../images/hub-dashboard-template-use-template.png
---
figclass: margin-caption
alt: A screenshot of the GitHub repository for the hub dashboard template. There is a red circle around the "Use this template" button.
name: hub-data-relations
---
Creating a hub dashboard from the template.
```

Then do the following to customize your dashboard (see the sections below for more detail):

1. Add markdown content to `pages/`
2. Update `site-config.yml`
    i. `hub` is the github slug for your active hub. This example defaults to the CDC FluSight hub
    ii. `title` is the title of your dashboard
    iii. `pages` is a list of pages you want included in the top bar. These will be shown after the home page (index.html) and the visualizaton and evaluation pages if they are included (see the next points).
3. To include a visualization page in the dashboard, update `predtimechart-config.yml` to specify configuration settings for your hub. If you don't want to include a visualization page in the dashboard, delete this configuration file.
4. To include an evaluation page in the dashboard, add `predevals-config.yml` and specify configuration settings for your hub. If you don't want to include an evaluation pages in the dashboard, omit this configuration file.
5. If necessary, update the GitHub workflows to change the timing of scheduled builds of site contents and data.

Once these steps are performed, the workflows will automatically generate the website on the `gh-pages` branch on your behalf. Once this branch is created, you can activate your website to deploy from this branch.

> [!NOTE]
>
> At the moment, the first time you create your repository, you will need to
> manually switch on your github pages by going to `<repo>/settings/pages` and
> selecting `gh-pages` as the branch to deploy from:
>
> ![screenshot of the "Build and Deployment" section of the pages setting. There are two sub-headings that say "source" and "branch". The Source heading has a dropdown that is selected to "Deploy from a branch". The Branch heading shows a dropdown with `gh-pages`, `main`, `ptc/data`, and `None` as options for the "branch" dropdown. A red arrow is pointing to the `gh-pages` option, which is highlighted.](../images/github-pages-select-branch.png)

## Customizing the Dashboard Website

### Page Organization and Content

Each individual page within the dashboard is defined by a corresponding markdown file located within the `pages` folder of the dashboard repository. These files use the [Pandoc markdown syntax](https://quarto.org/docs/authoring/markdown-basics.html) to specify page contents. By default, the dashboard template comes with a landing page (defined in `index.qmd`) and an "about" page (defined in `about.qmd`). The file extension `.qmd` indicates that these will be used with Quarto. Additional pages can also be added to the dashboard by creating more Quarto markdown files. To be findable, these additional pages must either be added to the main navigation menu for the dashboard (see the next section for how to do this), or linked to from another page.

### Configuration

The [`site-config.yml`](site-config.yml) is a simplified form of [A Quarto Website](https://quarto.org/docs/websites/#config-file). This simplified form is intended to allow you to set up a dashboard website in a matter of minutes while allowing for flexibility of theme.

A simple configuration is presented in [the template `site-config.yml`](https://github.com/hubverse-org/hub-dashboard-template/blob/main/site-config.yml) file
with three keys:

 - hub: the GitHub slug to your active hub that contains quantile forecast data
 - title: the title of your hub dashboard website
 - pages: a [YAML array](https://www.commonwl.org/user_guide/topics/yaml-guide.html#arrays) that lists files _relative to [the `pages` directory](pages/)_ that should be included in the dashboard site. The name of each page is encoded in the `title:` element of the file header (but this can be overridden with [site customization](#customization)).

Other than the `hub` field all remaining fields have the following mapping equivalents in the Quarto configuration file:

| `site-config.yml`  | `_quarto.yml` |
| ------------------ | ------------- |
| `.title`           | `.website.title` |
| `.pages`           | [`.website.navbar.left`](https://quarto.org/docs/websites/website-navigation.html#top-navigation) |
| `.html` (optional) | [`.format.html`](https://quarto.org/docs/reference/formats/html.html#format-options) |

### Customization

When the page is built with [the hub dashboard site builder](https://github.com/hubverse-org/hub-dash-site-builder), this configuration file is merged with [the default quarto config file](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/static/_quarto.yml). This allows for customization of the page. Below
are examples of customization.

#### Icons added to pages

You can add icons to the page title bars with a YAML map. If you wanted to add an icon of people for the "about" page, you would use `.pages.icon: "people-fill"`.

```yaml
pages:
  - icon: "people-fill"
    href: "about.md"
  - icon: "mortarboard-fill"
    href: "citation.md"
```

The full list of available icons can be found on the [Bootstrap icons website](https://icons.getbootstrap.com/).

#### Theme

The default site is built on top of the [Bootstrap yeti theme](https://bootswatch.com/yeti/) with [custom CSS](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/static/resources/css/styles.css).

If you wanted to use [a different theme](https://quarto.org/docs/output-formats/html-themes.html), you can change it by setting `.html.theme`. You can reset the css by setting `.html.css: null`

```yaml
html:
  theme: "litera"
  css: null
```

#### Contents

If you wanted to add custom HTML to appear at the bottom or top of every page,
you can use `.html.include-after-body` or `.html.include-before-body`. Remember
that all resources are _relative to the `pages/` directory_, so if you wanted
to include an HTML snippet at the end of every page you would:

1. add a file called `resources/after-body.html` into `pages/`
2. add this to your yaml:
   ```yaml
   html:
     include-after-body: "resources/after-body.html"
   ```

## PredTimeChart Visualization (optional)

Edit the `predtimechart-config.yml` file to match your hub. You can view the [raw schema](https://raw.githubusercontent.com/hubverse-org/hub-dashboard-predtimechart/main/src/hub_predtimechart/ptc_schema.py) for this file to see the detailed specification of its contents. Below, we give an example file based on the [FluSight forecast hub](https://github.com/cdcepi/FluSight-forecast-hub) and describe the fields to include:

```yaml
---
rounds_idx: 0
model_tasks_idx: 1
reference_date_col_name: 'reference_date'
target_date_col_name: 'target_end_date'
horizon_col_name: 'horizon'
initial_checked_models: ['FluSight-ensemble', 'FluSight-baseline']
target_data_file_name: 'target-hospital-admissions.csv'
disclaimer: 'Be careful when interpreting these forecasts.'
task_id_text:
  location:
    "US": "United States"
    "01": "Alabama"
    "02": "Alaska"
    "04": "Arizona"
    "05": "Arkansas"
    "06": "California"
```

This file is given in the [YAML format](https://en.wikipedia.org/wiki/YAML), and it contains the following fields:

 - `rounds_idx`: The 0-based index of the `rounds` entry in the hub's `tasks.json` configuration file to use for the visualization.
    - As is described in more detail in the limitations section below, the visualization is currently only able to show predictions for defined within one block of the `rounds` section of the `tasks.json` configuration.
 - `model_tasks_idx`: The 0-based index of the `model_tasks` entry under `rounds_idx` to use for the visualization.
    - As is described in more detail in the limitations section below, the visualization is currently only able to show predictions that are defined in a single "model tasks block".
 - `reference_date_col_name`: The name of the column that represents the reference date (sometimes also referred to as the origin date) for step-ahead predictions.
 - `target_date_col_name`: The name of the column that represents the target date for a step-ahead prediction.
 - `horizon_col_name`: The name of the column that represents the forecast horizon for a step-ahead prediction.
 - `initial_checked_models`: An array of model ids that should be displayed when the visualization is first loaded.
 - `target_data_file_name` (**deprecated**): This specifies the name of the file with observed target data stored within the hub. This parameter is deprecated, and should not be used for new hub dashboards.
 - `disclaimer` (**optional**): Text that is displayed immediately above the visualization to provide important information to dashboard users.
 - `task_id_text` (**optional**): A mapping of values for task id variables to text that is displayed in the visualization. For instance, this can be used to replace numeric location codes with human-readable location names. Each task id variable with a value-to-text mapping should be listed as a property under `task_id_text`. Within that entry, keys (on the left hand side of the `:`) are values of the task id variable as specified in the `tasks.json` config file, and values (on the right hand side of the `:`) give the corresponding text to display in the visualization.

### PredTimeChart Limitations

Here we summarize some important limitations of the visualization functionality that is currently available.

## PredEvals Evaluation (optional)

To include an evaluation page in the dashboard, add a file named `predevals-config.yml` to the root of your dashboard repository. In the following section, we provide A link to the schema for this configuration file and an interactive view of the schema.

### Schema Version: v1.0.0

See the [raw schema](https://raw.githubusercontent.com/hubverse-org/hubPredEvalsData/main/inst/schema/v1.0.0/config_schema.json), or explore the schema interactively below:

<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/hubPredEvalsData/main/inst/schema/v1.0.0/config_schema.json"></script>

### PredEvals Limitations



## Using GitHub Actions to Build Site Contents and Data


