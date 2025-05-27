# Forecasts dashboard

The forecasts dashboard provides an interactive time series visualization of the
prediction forecasts against the existing target data. The interactivity is
provided by the [PredTimeChart](https://github.com/reichlab/predtimechart)
JavaScript module, which reads in JSON-formatted data and produces a dashboard
interface that allows the user to explore predictions based on target and task
IDs.

The data sources are the [target time series](#target-time-series)
and [model output](../user-guide/model-output.md). These are transformed to JSON
format via
[hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart),
which creates JSON files that subdivide the data in the format of
`[target]_[location]_[date].json`[^round-note]. For each combination of target, location,
and round, two files are generated: one that records the X and Y values for the
target data and one that records the predictions for each model. Finally, a file
called `predtimechart-options.json` is created that sets up the initial
parameters for the interactive graph.

[^round-note]: The `date` element is always synonymous with a target end date,
    which, in turn is expected to match the round date. One of the [limitations
    for forecast dashboards](#ptc-limitations) is that each round ID must be in
    the `YYYY-MM-DD` date format.

The final file structure that the forecasts dashboard expects looks like this
(using the [flu metrocast dashboard as an
example](https://reichlab.io/metrocast-dashboard/forecast.html)) where the targets are
`Flu-ED-visits-pct` (locations: Texas metropolitan areas) and `ILI-ED-visits`
(locations: Boroughs of New York City) and the dates start in January 2025.

```{code-block}
:emphasize-lines: 4,7,10,13
.
├── predtimechart-options.json
├── forecasts
│   ├── ..._2025-01-25.json
│   ├── Flu-ED-visits-pct_Austin_2025-04-19.json
│   ├── Flu-ED-visits-pct_...
│   ├── ILI-ED-visits_...
│   └── ILI-ED-visits_Staten-Island_2025-04-19.json
└── targets
    ├── ..._2025-01-25.json
    ├── Flu-ED-visits-pct_Austin_2025-04-19.json
    ├── Flu-ED-visits-pct_...
    ├── ILI-ED-visits_...
    └── ILI-ED-visits_Staten-Island_2025-04-19.json
```

## Generated file structure

The three file types generated have slightly different structures


`predtimechart-options.json`
: This object is responsible for setting the boundaries and text for the
  visualiation and is described in [the PredTimeChart
  README](https://github.com/reichlab/predtimechart?tab=readme-ov-file#example-options-object)

files in `forecasts/`
: These contain one JSON object per model that contains the X axis coordinates
  (target end date) and the Y axis coordinates for each of the quantiles (0.025,
  0.25, 0.5, 0.75, and 0.975).
  ```{code-block} json
  :force: true
  {
    "epiENGAGE-GBQR": ...,
    "epiENGAGE-ensemble_mean": {
      "target_end_date": [
        "2025-04-05",
        ...
        "2025-05-10"
      ],
      "q0.025": [
        0.301087635550679,
        ...
        0.0579447375
      ],
      "q0.25": [
        0.653925763611294,
        ...
        0.165562
      ],
      "q0.5": [
        0.805770325514081,
        ...
        0.275778
      ],
      "q0.75": [
        0.957430826181607,
        ...
        0.9342365
      ],
      "q0.975": [
        1.63488906483369,
        ...
        2.48783975
      ]
    },
    "epiENGAGE-INFLAenza": ...
  }
  ```

files in `targets/`
: These contain the record of the time series target data _as of_ the target date
  on the file. This is a simpler structure that records the date and the y axis
  values:
  ```{code-block} json
  :force: true
  {
    "date": [
      "2022-10-01",
      ...,
      "2025-03-29"
    ],
    "y": [
      1.38,
      ...,
      0.84
    ]
  }
  ```

## Installation

The `hub-dashboard-predtimechart` tool is a python app that can be installed
with `pip`. It installs a command line interface that can build the resources
for PredTimeChart.


You can install the development version with:

```bash
pip install git+https://github.com/hubverse-org/hub-dashboard-predtimechart
```

The latest version can be installed by finding the latest release and appending that to the above command. For example, here's how to install v2.2.0:

```bash
pip install git+https://github.com/hubverse-org/hub-dashboard-predtimechart@v2.2.0
```

You can also get the latest version by using the GitHub API:

```bash
latest=$(gh api -X GET "repos/hubverse-org/hub-dashboard-predtimechart/releases/latest" --jq ".tag_name")
pip install git+https://github.com/hubverse-org/hub-dashboard-predtimechart@$latest
```

## How forecast data are built

There are two steps to build the data for the forecast dashboard:

1. build the forecast data and the configuration options
2. build the target data

Both of these require a hub and a `predtimechart-config.yml` file

### Building the forecasts

You need these two things to build the forecasts and config file:

1. a `predtimechart-config.yml` file
2. a hub with submissions for the current round in the `model-output` directory

The code below assumes you are starting with a dashboard repository that has
a `predevals-config.yml` file inside of it. We first clone the hub repository
locally and then run the script

```{code-block} bash
:emphasize-lines: 4-8
git clone <hub-git-url> hub
mkdir -p data/ptc/forecasts

ptc_generate_json_files \
  hub \
  predtimechart-config.yml \
  data/ptc/predtimechart-options.json \
  data/ptc/forecasts
```

There are two things that govern how the data are written:

1. The current target end date is set by the date of the most recent model
   submission.
2. By default the tool will not overwrite any files that exist with the
   exception of the current target end date.

It is not possible to override 1, but you can override 2 by passing the
`--regenerate` flag, which will rebuild any files that exist and are valid (it
will not clean up, though).


### Building the targets

You need these two things to build the targets:

1. a `predtimechart-config.yml` file
2. a hub with time series data (if it is hubverse-formatted data with an `as_of`
   column, historical data can be generated)

The code below assumes you are starting with a dashboard repository that has
a `predevals-config.yml` file inside of it. We first clone the hub repository
locally and then run the script

```{code-block} bash
:emphasize-lines: 4-8
git clone <hub-git-url> hub
mkdir -p data/ptc/targets

ptc_generate_target_json_files \
  hub \
  predtimechart-config.yml \
  data/ptc/targets
```

There are three things that govern how the data are written:

1. The current target end date is set by the date of the most recent model
   submission.
2. By default the tool will not overwrite any files that exist.
3. If there is an `as_of` column, data will be back-filled based on that column

Similar to the forecast generation, if you need override 2, you can use the
`--regenerate` flag.


## Testing

This tool has unit tests via pytest.
