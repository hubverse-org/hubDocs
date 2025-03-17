# Dashboards

The hubverse provides a modular system for building a dashboard website for a modeling hub. This includes three main components:

1. A system for creating a website with multiple pages by creating a set of markdown files with site contents and a yaml file specifying configuration settings. This is based on the [quarto publishing system](https://quarto.org/).
2. An optional module for interactive visualizations of model outputs (predictions) and target data.
3. An optional module for interactive exploration of scores for model predictions.

The website contents, including the web pages as well the data backing interactive visualizations and evaluations, are built by GitHub actions that can be set to run on a regular schedule or manually as needed. By default, the website is hosted on a GitHub pages site, though it could also be hosted on another static website hosting platform if desired.

Below, we describe how to set up each of these three components of the dashboard system and the use of GitHub actions for building the site.

## Quickstart -- building a dashboard

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
    1. `hub` is the github slug for your active hub. This example defaults to the CDC FluSight hub
    2. `title` is the title of your dashboard
    3. `pages` is a list of pages you want included in the top bar. These will be shown after the home page (index.html) and the visualizaton and evaluation pages if they are included (see the next points).
3. To include a visualization page in the dashboard, update `predtimechart-config.yml` to specify configuration settings for your hub. If you don't want to include a visualization page in the dashboard, delete this configuration file.
4. To include an evaluation page in the dashboard, update `predevals-config.yml` to specify configuration settings for your hub. If you don't want to include an evaluation page in the dashboard, delete this configuration file.
5. If necessary, update the GitHub workflows to change the timing of scheduled builds of site contents and data.

Once these steps are performed, the workflows will automatically generate the website on the `gh-pages` branch on your behalf. Once this branch is created, you can activate your website to deploy from this branch.

:::{admonition} Setting up GitHub pages
:class: note

At the moment, the first time you create your repository, to set up hosting of
your dashboard on GitHub pages, you will need to manually switch on GitHub
pages by going to `<repo>/settings/pages` and selecting `gh-pages` as the branch
to deploy from:

![screenshot of the "Build and Deployment" section of the pages setting. There are two sub-headings that say "source" and "branch". The Source heading has a dropdown that is selected to "Deploy from a branch". The Branch heading shows a dropdown with `gh-pages`, `main`, `ptc/data`, and `None` as options for the "branch" dropdown. A red arrow is pointing to the `gh-pages` option, which is highlighted.](../images/github-pages-select-branch.png)

:::

## Customizing the dashboard website

### Page organization and content

Each individual page within the dashboard is defined by a corresponding markdown file located within the `pages` folder of the dashboard repository. These files use the [Pandoc markdown syntax](https://quarto.org/docs/authoring/markdown-basics.html) to specify page contents. By default, the dashboard template comes with a landing page (defined in `index.qmd`) and an "about" page (defined in `about.qmd`). The file extension `.qmd` indicates that these will be used with Quarto. Additional pages can also be added to the dashboard by creating more Quarto markdown files. To be findable by dashboard users, these additional pages must either be added to the main navigation menu for the dashboard (see the next section for how to do this), or linked to from another page.

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

## PredTimeChart visualization (optional)

The PredTimeChart visualization module creates an interactive display of step-ahead predictions, including scenario projections, hindcasts, nowcasts, and forecasts. Dashboard users can select different models to include, the reference date (also referred to as the origin date) when predictions were created, and the values of task id variables to show (such as location). The visualization shows predictions alongside the latest available target data and the version of the target that was available at the time the predictions were created.

```{figure} ../images/dashboard-viz-screenshot.png
---
figclass: margin-caption
alt: A screenshot of the visualization in the FluSight dashboard. The visualization shows predictions (median and 95% prediction intervals) of weekly incident influenza hospitalizations in the United States from two models.
name: dashboard-viz-screenshot
---
A screenshot of the visualization in the FluSight dashboard.
```

### Configuring the PredTimeChart visualization module

If you don't want to include a visualization using the PredTimeChart module in your dashboard, delete the `predtimechart-config.yml` file from your dashboard repository.

To include the PredTimeChart visualization, edit the `predtimechart-config.yml` file to match your hub. You can view the [raw schema](https://raw.githubusercontent.com/hubverse-org/hub-dashboard-predtimechart/main/src/hub_predtimechart/ptc_schema.py) for this file to see the detailed specification of its contents. Below, we give an example file based on the [FluSight forecast hub](https://github.com/cdcepi/FluSight-forecast-hub) and describe the fields to include:

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

This file is written in the [YAML format](https://en.wikipedia.org/wiki/YAML), and it contains the following fields:

 - `rounds_idx`: The 0-based index of the `rounds` entry in the hub's `tasks.json` configuration file to use for the visualization.
    - As is described in more detail in the limitations section below, the visualization is currently only able to show predictions for defined within one block of the `rounds` section of the `tasks.json` configuration.
 - `model_tasks_idx`: The 0-based index of the `model_tasks` entry under `rounds_idx` to use for the visualization.
    - As is described in more detail in the limitations section below, the visualization is currently only able to show predictions that are defined in a single "model tasks block".
 - `reference_date_col_name`: The name of the column that represents the reference date (sometimes also referred to as the origin date) for step-ahead predictions.
 - `target_date_col_name`: The name of the column that represents the target date for a step-ahead prediction.
 - `horizon_col_name`: The name of the column that represents the forecast horizon for a step-ahead prediction.
 - `initial_checked_models`: An array of model ids that should be displayed when the visualization is first loaded.
 - `target_data_file_name` (**deprecated**): This specifies the name of the file with observed target data stored within the hub. This parameter is deprecated, and should not be used for new hub dashboards. To use the PredTimeChart module, hubs must follow the [Hubverse conventions for target time series data](../user-guide/target-data.md).
 - `disclaimer` (**optional**): Text that is displayed immediately above the visualization to provide important information to dashboard users.
 - `task_id_text` (**optional**): A mapping of values for task id variables to text that is displayed in the visualization. In the example above, this is be used to replace numeric location codes with location names. Each task id variable with a value-to-text mapping should be listed as a property under `task_id_text`. Within that entry, keys (on the left hand side of the `:`) are values of the task id variable as specified in the `tasks.json` config file, and values (on the right hand side of the `:`) give the corresponding text to display in the visualization.

### PredTimeChart limitations and requirements

Here we summarize some important limitations of the visualization functionality that is currently available:

 - The visualization tool can only display step-ahead predictions that use the quantile output type.
 - It can only display predictions for tasks that are defined in a single entry in the `rounds` section of the hub's `tasks.json` configuration file. Note that it is possible to display predictions for multiple rounds, and a dashboard typically will do that. However, those rounds must be defined in a single `rounds` block.
 - It can only display predictions for modeling tasks that are defined in a single entry of the `model_tasks` section of the hub's `tasks.json` configuration file. Again, this allows for display of predictions across multiple modeling tasks as long as the values of the task id variables defining those modeling tasks are specified in the same `model_tasks` block.
 - Currently, only a single prediction target is supported. Specifically, the `target_metadata` array in the specified `model_tasks` object within the specified `rounds` object must contain exactly one object, which must have a single key in the `target_keys` object.
 - The following quantile levels (`output_type_id`s) must be present: `0.025`, `0.25`, `0.5`, `0.75`, `0.975`. These quantiles define the predictive median and the bounds of 50% and 95% prediction intervals.
 - The hub must have task id variables defining:
    - A reference date for when predictions were created (e.g., `reference_date`, `origin_date`, or similar)
    - The target date of a predicted event (e.g., `target_date`, `target_end_date`, or similar)
    - The forecast horizon, defined as the difference between the target date and the reference date (e.g. `horizon` or similar)
 - Model metadata must contain a boolean `designated_model` field. The visualization only includes models where this field has been set to `true`.
 - As was noted above, the target time series data must be stored in the hub using the [Hubverse conventions for target time series data](../user-guide/target-data.md). Additionally, at this time only a single `.csv` file with time series data is supported (i.e., this module corrently does not support the `parquet` format or hive partitioned data).

## PredEvals evaluation (optional)

The PredEvals module creates an interactive display of scores for predictions. Dashboard users can view overall scores in a table, or see line plots or heatmaps visualizing scores broken down by a task id variable.

```{figure} ../images/dashboard-eval-table.png
---
figclass: margin-caption
name: dashboard-eval-table
---
A screenshot of the evaluation table in the COVID-19 Forecast Hub dashboard. The table shows overall scores for each model.
```

```{figure} ../images/dashboard-eval-lineplot.png
---
figclass: margin-caption
name: dashboard-eval-lineplot
---
A screenshot of the COVID-19 Forecast Hub dashboard showing a line plot of relative WIS values for models, broken down by the target end date of the prediction.
```

```{figure} ../images/dashboard-eval-heatmap.png
---
figclass: margin-caption
name: dashboard-eval-heatmap
---
A screenshot of the COVID-19 Forecast Hub dashboard showing a heatmap of relative WIS values for models, broken down by the location of the prediction.
```

### Configuring the PredEvals module

If you don't want to include an evaluation page using the PredEvals module in your dashboard, delete the `predevals-config.yml` file from your dashboard repository.

To include the PredEvals component, edit the `predevals-config.yml` file to match your hub. Here, we give an example configuration file that is adapted from the [FluSight forecast hub](https://github.com/cdcepi/FluSight-forecast-hub):

```yaml
schema_version: https://raw.githubusercontent.com/hubverse-org/hubPredEvalsData/main/inst/schema/v1.0.0/config_schema.json
targets:
- target_id: wk inc flu hosp
  metrics:
  - wis
  - ae_median
  - interval_coverage_50
  - interval_coverage_95
  relative_metrics:
  - wis
  - ae_median
  baseline: FluSight-baseline
  disaggregate_by:
  - location
  - reference_date
  - horizon
  - target_end_date
eval_sets:
- eval_set_name: Full season
  round_filters:
    min: '2024-11-30'
  task_filters:
    location:
    - "01"
    - "02"
    - "04"
    - "05"
    - "06"
    - "08"
    - "09"
    - "10"
    - "11"
    - "12"
    - "13"
    - "15"
    - "16"
    - "17"
    - "18"
    - "19"
    - "20"
    - "21"
    - "22"
    - "23"
    - "24"
    - "25"
    - "26"
    - "27"
    - "28"
    - "29"
    - "30"
    - "31"
    - "32"
    - "33"
    - "34"
    - "35"
    - "36"
    - "37"
    - "38"
    - "39"
    - "40"
    - "41"
    - "42"
    - "44"
    - "45"
    - "46"
    - "47"
    - "48"
    - "49"
    - "50"
    - "51"
    - "53"
    - "54"
    - "55"
    - "56"
    - "72"
    horizon:
    - 0
    - 1
    - 2
    - 3
- eval_set_name: Last 4 weeks
  round_filters:
    min: '2024-11-30'
    n_last: 5
  task_filters:
    location:
    - "01"
    - "02"
    - "04"
    - "05"
    - "06"
    - "08"
    - "09"
    - "10"
    - "11"
    - "12"
    - "13"
    - "15"
    - "16"
    - "17"
    - "18"
    - "19"
    - "20"
    - "21"
    - "22"
    - "23"
    - "24"
    - "25"
    - "26"
    - "27"
    - "28"
    - "29"
    - "30"
    - "31"
    - "32"
    - "33"
    - "34"
    - "35"
    - "36"
    - "37"
    - "38"
    - "39"
    - "40"
    - "41"
    - "42"
    - "44"
    - "45"
    - "46"
    - "47"
    - "48"
    - "49"
    - "50"
    - "51"
    - "53"
    - "54"
    - "55"
    - "56"
    - "72"
    horizon:
    - 0
    - 1
    - 2
    - 3
task_id_text:
  location:
    US: United States
    '01': Alabama
    '02': Alaska
    '04': Arizona
    '05': Arkansas
    '06': California
    '08': Colorado
    '09': Connecticut
    '10': Delaware
    '11': District of Columbia
    '12': Florida
    '13': Georgia
    '15': Hawaii
    '16': Idaho
    '17': Illinois
    '18': Indiana
    '19': Iowa
    '20': Kansas
    '21': Kentucky
    '22': Louisiana
    '23': Maine
    '24': Maryland
    '25': Massachusetts
    '26': Michigan
    '27': Minnesota
    '28': Mississippi
    '29': Missouri
    '30': Montana
    '31': Nebraska
    '32': Nevada
    '33': New Hampshire
    '34': New Jersey
    '35': New Mexico
    '36': New York
    '37': North Carolina
    '38': North Dakota
    '39': Ohio
    '40': Oklahoma
    '41': Oregon
    '42': Pennsylvania
    '44': Rhode Island
    '45': South Carolina
    '46': South Dakota
    '47': Tennessee
    '48': Texas
    '49': Utah
    '50': Vermont
    '51': Virginia
    '53': Washington
    '54': West Virginia
    '55': Wisconsin
    '56': Wyoming
    '60': American Samoa
    '66': Guam
    '69': Northern Mariana Islands
    '72': Puerto Rico
    '74': U.S. Minor Outlying Islands
    '78': Virgin Islands
```

This file is written in the [YAML format](https://en.wikipedia.org/wiki/YAML). You can view the [raw schema](https://raw.githubusercontent.com/hubverse-org/hubPredEvalsData/main/inst/schema/v1.0.0/config_schema.json) for this file to see the detailed specification of its contents, or use the widget below to explore the schema interactively:

<!-- - `schema_version`: 
    - URL to a version of the `hubPredEvalsData` `config_schema.json` file. Used to declare the schema version a `predevals-config.yml` file is compatible with. The URL provided should be the URL to the raw content of the schema file on GitHub.
- `targets`: Targets for which to compute evaluation metrics, as well as a specification of how predictions for each target should be computed. This is a YAML array with one entry for each target. In the example above, only one target is included, `"wk inc flu hosp"`. For each target, the following properties should be specified:
    - `target_id`: The target id, matching a value given in the `target_metadata.target_id` field in the hub's `tasks_config.json` file
    - `metrics`: Names of metrics to compute for this target.  These should be names of metrics supported by `hubEvals::score_model_out`.
    - `relative_metrics`: Optional names of metrics for which to compute pairwise relative skill for this target.  These should be a subset of the metrics for the target. These must be proper scores (e.g., interval coverage metrics are not allowed here).
    - `baseline`: Name of the model to use as a baseline for relative skill metrics for this target. Required if `relative_metrics` is provided.
    - `disaggregate_by`: Optional list of task id columns to disaggregate by. Overall scores for each model will always be computed.
- `eval_sets`: A YAML array of specifications for sets of prediction tasks that are used for score computations. Separate scores will be calculated and available in the dashboard for each evaluation set. Evaluation sets may be specified using two types of filters, `round_filters` and `task_filters` (see the following points). If multiple filtering criteria are provided, they are combined with 'and' logic, i.e. the evaluation set will include the intersection of the sets of prediction tasks specified by those criteria. If no filtering criteria are provided, the evaluation set will include all scorable predictions.

### Schema version: v1.0.0 -->

<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/hubPredEvalsData/main/inst/schema/v1.0.0/config_schema.json"></script>

In the example above, we specify that scores should be computed for a single target, `"wk inc flu hosp"`. We specify four metrics to compute: the weighted interval score (WIS), absolute error of the median, and prediction interval coverage at the 50% and 95% levels. Relative skill will be computed for two of those metrics: WIS and absolute error. In relative skill computations, scores will be normalized relative to the `FluSight-baseline` model. Finally, the evaluations will include overall scores for each model in the table, as well as the option to plot scores broken down by the `location`, `reference_date`, `horizon`, and `target_end_date` task id variables (breaking scores down by one variable at a time).

Unlike the PredTimeChart module, PredEvals supports scoring for multiple targets. We could specify another target for evaluation by adding an entry for it at the same level as the `"wk inc flu hosp"` target, complete with specifications for the `target_id`, the `metrics` and `relative_metrics` to compute, the `baseline` to use for relative metrics (if applicable), and the task id variables to `disaggregate_by` for that target.

The example specifies two evaluation sets, named `"Full season"` and `"Last 4 weeks"`. In the evaluation dashboard, a dropdown menu allows users to select the evaluation set for which results are displayed. Both evaluation sets are specified using a combination of filters on the modeling round (`round_filters`) and other filters on the modeling tasks (`task_filters`). Two types of `round_filters` are available. Both evaluation sets use the `min` setting to specify the earliest round id that is included in the evaluation set. The value of this setting must be a valid value of the task id variable that is used for the `round_id_from_variable` in the hub's `tasks.json` configuration file. The `"Last 4 weeks"` evaluation set additionally specifies `n_last`, which gives the trailing number of modeling rounds to include in the evaluation set.

:::{admonition} More detail about the `n_last` setting
:class: note

In the example above, the `"Last 4 weeks"` evaluation set uses the setting `n_last: 5`, which is admittedly confusing! The correct value to use here depends on details of scheduling for when scores are calculated after a round closing relative to when modelers submit predictions.

The `n_last` setting specifies the number of modeling rounds with any available model output data that should be included in the evaluation set. In this case, the last 5 modeling rounds with any available model output data are included in the evaluation set.  However, for the FluSight dashboard, scores are calculated and the dashboard is updated the day after the data release occurs and model submissions are due. This means that at the time the scores are calculated, model predictions are available for a round that just closed and for which no observed data are available yet to use in score computations. Since the predictions from that final round can't be scored, they are effectively discarded and in practice only the previous 4 rounds are included in the evaluation set. If it was possible to schedule the evaluations to run after a given data release but before any model predictions for the next round were submitted, we could set `n_last` to 4 instead of 5.

:::

In addition to `round_filters`, both of the evaluation sets in the example above use `task_filters`. In these examples, scores will be calculated for all state-level locations (discarding forecasts at the national level) and only for horizons 0 through 3 (discarding "hindcasts" made at horizon -1).

For each evaluation set, all filters are combined with "and" logic.  For example, the "Full season" evaluation set includes all predictions made in modeling rounds on or after `'2024-11-30'`, for state-level locations at non-negative forecast horizons.

:::{admonition} Redundancy of `round_filters` and `task_filters`
:class: note

In principle, it would be possible to implement `round_filters` by specifying the set of rounds to include within the `task_filters` block. While this is possible, specifying `round_filters` is more convenient and maintainable, so we recommend using those settings where appropriate.

:::

### PredEvals limitations and requirements

The PredEvals module has several important limitations:

 - The evaluation tool only supports hubs that have a single entry in the `rounds` section of the `tasks.json` configuration file.
 - Only hubs with `round_id_from_variable` set to `true` in the `tasks.json` configuration file are supported.
 - Supported output types include `mean`, `median`, `quantile`, and `pmf`. However, support for ordinal pmf predictions is still experimental. The `sample` and `cdf` output types are not supported.

## Using GitHub actions to build site contents and data

The template dashboard repository comes with a set of GitHub workflows that can be used to build the dashboard site contents either according to a recurring schedule or on an as-needed basis by hub administrators.

TODO: add information about how to do these things.
