# Configuring tasks

Every hub is organized around "modeling tasks" that are defined to meet the needs of a project. Modeling tasks are defined for a hub in the [`tasks.json` file](#model-tasks-schema), which specifies the three components of modeling tasks ([task ID variables](#task-id-vars), [output types](#output-types), and [target metadata](#target-metadata)). You can read a detailed definition of modeling tasks in the [defining modeling tasks section](../user-guide/tasks.md).

## Step 1: Open `tasks.json`

Make sure you are in  the `hub-config` folder. Then, click on `tasks.json` to open the file.

```{image} ../images/tasks-json.png
:alt: Screenshot of how to open tasks.json file in RStudio
:class: bordered
```

## Step 2: Examine the `tasks.json` file

You should see the code below in your source panel (upper left-hand panel). It has a specific structure that you can explore in the [interactive `tasks.json` schema explorer](#model-tasks-schema)

```{image} ../images/tasks-schema-0.png
:alt: Screenshot of the code in the tasks.json file
:class: bordered
```

This `tasks.json` file serves as a template and has very few values filled out, allowing users to adapt the hub to their needs. Nevertheless, to learn how to use this schema properly, we will use a "premade" `tasks.json` file from the [simple forecast hub example](https://github.com/hubverse-org/example-simple-forecast-hub) that already has values filled in, which will better illustrate what should go in each section.

## Step 3: Close the `tasks.json` file in RStudio

Ensure the `tasks.json` file in RStudio is closed by clicking the 'x' icon, as indicated below.

```{image} ../images/tasks-close.png
:alt: Screenshot of how to close tasks.json file in RStudio
:class: bordered
```

## Step 4: Download a premade `tasks.json` file

You can use the link to download the [`tasks.json` file](https://github.com/hubverse-org/example-simple-forecast-hub/blob/main/hub-config/tasks.json) from the example forecast hub by clicking on the *Download Raw File* icon as indicated below.

```{image} ../images/tasks-download.png
:alt: Screenshot of how to download a tasks.json file from GitHub
:class: bordered
```

Save the file in the `hub-config` folder (which is in [your repository on your local computer](#clone-repo)). This new file should replace the existing `tasks.json` file in this folder.

### 4.1: Examine the new `tasks.json` file

Open `tasks.json` and explore the content and structure. Simple explanations for elements in the example forecast hub file are offered below (*click on the hyperlinks for a full explanation of all the supported elements in a [`tasks.json` file](#model-tasks-schema) and definitions of [key concepts](../overview/definitions.md)*):

* `schema_version`{.codeitem}: Modeling hub schema versions are all housed in the [schemas repository](https://github.com/hubverse-org/schemas/).
* `round_id`{.codeitem}: The round identifier establishes which date from a forecast submission is used to identify the submission round it corresponds to (e.g., the origin date).
* `model_tasks`{.codeitem}: Model tasks include all the goals of the modeling effort, including the `task_ids`, `output_type`, and `target_metadata`.
* `task_ids`{.codeitem}: The task identifiers set the optional and required elements in a forecast submission, such as the `target`, `horizon`, `location`, and `origin date`.
* `origin_date`{.codeitem}: The date when a forecast was generated. More information on this and other dates, including using the `origin_date` to calculate the `target_date`, can be found in the [section on using task ID variables](#task-id-use).
* `horizon`{.codeitem}: Sets the time range for which forecast predictions are to be made. For instance, these can be days into the future or even days into the past, as in nowcasts.
* `location`{.codeitem}: The geographic identifier, such as country codes or FIPS state/county level codes.
* `output_type`{.codeitem}: A model output type establishes the valid model output types, such as the mean or specific quantiles. A more detailed explanation of model outputs can be found in the [section on model output formats](#model-output-format).

Now, read below for details on some of the lines of code in this file:

(tasks-json-edits)=
## Step 5: Define `"task_ids"`
### 5.1. Establishing the `"round_id"` and `"origin_date"` *(starting point)*:
- <mark style="background-color: #32E331">The code highlighted in green</mark> establishes that the *round identifier* is encoded by a *task id* variable in the data.
- <mark style="background-color: #38C7ED">The code highlighted in light blue</mark> sets the *round identifier* as `"origin_date"`.
- `task_ids` includes the variables `origin_date`, `target`, `horizon`, and `location`.
- <mark style="background-color: #FFE331">The first variable, `origin_date` is highlighted in yellow</mark> and states that no *origin dates* are required and that there are three valid, possible dates (`"2022-11-28", "2022-12-05", "2022-12-12"`). To be clear, no specific `origin_date` is required because every submission will have a different `origin_date` as each submission corresponds to a different forecasting period (compare this with `location`, where some specific locations may be required for every submission.

```{image} ../images/tasks-schema-1.png
:alt: Some of the initial lines of code in the tasks.json file
:class: bordered
```

### 5.2. Setting the `"target"`:
- <mark style="background-color: #32E331">The second line</mark> states that `"inc covid hosp"` for example is the required target. Additional required targets could be added here.
- <mark style="background-color: #38C7ED">The third line</mark> states that there are no other optional targets that are valid. You could add `["cum covid hosp"]`, for example, if you wanted to allow that target but not require it.

```{image} ../images/tasks-schema-2.png
:alt: Some lines of code in the tasks.json file
:class: bordered
```

### 5.3. Setting up the `"horizon"`:
- The `horizon` refers to the difference between the `target_date` and the `origin_date` in time units specified by the hub (these could be days, weeks, or months).
- <mark style="background-color: #32E331">The second line</mark> indicates that no horizons are required.
- <mark style="background-color: #38C7ED">The third line</mark> states that the forecast can be for up to 6 days **before** the `origin_date`, and up to 14 days **after** the `origin_date`.

```{image} ../images/tasks-schema-3.png
:alt: More lines of code in the tasks.json file
:class: bordered
```


(setting-up-location)=
### 5.4. Setting up `"location"`:
- The `location` refers to geographic identifiers such as country codes or FIPS state/county level codes.
- <mark style="background-color: #32E331">The second line</mark> states that no particular location is required, although, in some instances, specific locations might be required for all submissions.
- <mark style="background-color: #38C7ED">The third line</mark> indicates the locations that may be submitted. The locations in this example correspond to FIPS codes for US states and territories.

```{image} ../images/tasks-schema-4.png
:alt: Even more lines of code in the tasks.json file
:class: bordered
```

### 5.5. `required` and `optional` elements:

As seen previously, each `task_ids` has a `required` and an `optional` property to indicate expected and possible additional information, respectively.

- To indicate **no possible additional information**, **`optional` can be set to `null`**.
- If **`required` is set to `null`** but `optional` contains values, (see for example [`"location"`](#setting-up-location)): **no particular value is required, but at least one of the `optional` values is expected**.
- There may be cases where we have **multiple `model_tasks` and a given task ID is relevant to one or more model tasks but not others.** For example, in the code snippet below; on lines 8--14, the `horizon` task id is relevant to the first model task, whose `target` is `inc covid hosp`, and any one of the optional values specified is expected in the `horizon` column in a model output file.
  However, shown on lines 30--36, **`horizon` is irrelevant to the second model task**, whose `target` is `peak size`. For this model task, **both `required` and `optional` are set to `null`** in the `horizon` task ID configuration, and a missing value is expected in the `horizon` column in model output files.

```{code-block} json
:force: true
:lineno-start: 1
:emphasize-lines: 8-14,30-36
"model_tasks": [
    {
        "task_ids": {
            "origin_date": {
                "required": null,
                "optional": ["2022-11-28"]
            },
            "target": {
                "required": ["inc covid hosp"],
                "optional": null
            },
            "horizon": {
                "required": null,
                "optional": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            },
            "location": {
                "required": ["US"],
                "optional": null
            }
        },
        "output_type": {...},
        "target_metadata": [...]
    },
    {
        "task_ids": {
            "origin_date": {
                "required": null,
                "optional": ["2022-11-28"]
            },
            "target": {
                "required": ["peak size hosp"],
                "optional": null
            },
            "horizon": {
                "required": null,
                "optional": null
            },
            "location": {
                "required": ["US"],
                "optional": null
            }
        },
        "output_type": {...},
        "target_metadata": [...]
    }
]
```

## Step 6: Define `"output_type"`:
The [`output_type`](#model-output-format) specifies the types of outputs accepted for a given model task. This example includes `mean` and `quantile`, but `median`, `cdf`, `pmf`, and `sample` are other supported output types.

Each output type contains the following properties:

- **`output_type_id`** (or `output_type_id_params` in the case of `sample`):   specifies/configures valid output type ID values.
- **`value`**: specifies the format and rules for the output's values, such as the data type and any limits (e.g., minimum or maximum values).
- **`is_required`**: A true/false property to indicate whether an output type is required.

### 6.1. Setting the `"mean"`:

- Here, the `"mean"`{.codeitem} of the predictive distribution is set as a valid `output_type` value for a submission file.
- `"output_type_id"`{.codeitem} must be `null` for all point estimates (mean,
  median, etc). No output type IDs for these estimates are applicable, so in a
  model submission file, they are represented as missing data[^missy].
- `"value"`{.codeitem} sets the characteristics of this valid `output_type` (i.e., the mean). In this instance, the value must be an `integer` greater than or equal to `0`.
- `"is_required"`{.codeitem} defines if a mean prediction is required (`true`) or if it is optional (`false`). The code below shows that the mean output type is optional.

[^missy]: In a CSV file, this is represented as either a blank cell (default for Python) or `NA` (default for R).

```{code-block} json
:force: true
:lineno-start: 1
"mean": {
    "output_type_id": {
        "required": null
    },
    "value": {
        "type": "integer",
        "minimum": 0
    },
    "is_required": false
}
```

### 6.2. Setting up `"quantile"`:
- Here, the `quantile`{.codeitem} object configures what values are accepted in the `output_type_id` and `value` columns when the value in the `output_type` column in a submission file is `"quantile"`.
- `"output_type_id"`{.codeitem} (line 2) establishes the accepted probability levels at which quantiles of the predictive distribution will be recorded. In this case, quantiles are required at discrete levels that range from `0.01` to `0.99`. **Quantile `output_type_id` values must NOT contain trailing zeros** as this will cause submission validation checks to fail[^quant-fail].
- As before, `"value"`{.codeitem} (line 29) sets the characteristics of valid `quantile` `value` values. In this instance, the values must be integers greater than or equal to `0`.
- `"is_required"`{.codeitem} (line 33) defines whether a quantile prediction is required (`true`) or if it is optional (`false`). The code below shows that the quantile output type is required.

[^quant-fail]: During validation, the quantile output type IDs are compared as character strings instead of as numeric (floating point) values. There is a good reason for this: [floating point numbers have precision problems](https://en.wikipedia.org/wiki/Floating-point_arithmetic#Accuracy_problems).

```{code-block} json
:force: true
:lineno-start: 1
"quantile": {
    "output_type_id": {
        "required": [
            0.01,
            0.025,
            0.05,
            0.1,
            0.15,
            0.2,
            0.25,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.55,
            0.6,
            0.65,
            0.7,
            0.75,
            0.8,
            0.85,
            0.9,
            0.95,
            0.975,
            0.99,
        ]
    },
    "value": {
        "type": "integer",
        "minimum": 0
    },
    "is_required": true
}
```

## Step 7: Defining `"target_metadata"`:
- `"target_metadata"`{.codeitem} defines the characteristics of each unique `target`.
- To begin with, `"target_id"`{.codeitem} is a short description that uniquely identifies the target.
- Similarly, `"target_name"`{.codeitem} provides a longer, human readable description of the target.
- `"target_units"`{.codeitem} indicates the unit of observation used for this target.  In this instance, the unit is `"count"`.
- `"target_keys"`{.codeitem} expect either a `null` value or an object containing a single key/value pair that appropriately identifies the target. If providing a `null` value, the hub is assumed to have a single target that is not encoded in any task ID variables. The name of the target is instead provided through the `target_id` property. If a key/value pair is provided, the key must match the name of a task ID variable and the single value must match a valid task ID value of the task ID variable specified in the key.  In this instance, the key is the task ID variable name `"target"` and the value is `"inc covid hosp"`.
- The `"description"`{.codeitem} is a verbose explanation of the target, which might include details on the measure used for the target, as shown in the example below.
- The `"target_type"`{.codeitem} defines the target's statistical data type. In this instance, the target uses discrete data.
- `"is_step_ahead"`{.codeitem} indicates whether the target is part of a sequence of values.  In this instance, it is.
- `"time_unit"`{.codeitem} defines the units of the time steps. In this case, it is days.


```{code-block} json
:force: true
:lineno-start: 1
"target_metadata": [
    {
        "target_id": "inc covid hosp",
        "target_name": "Daily incident COVID hospitalizations",
        "target_units": "count",
        "target_keys": {
            "target": "inc covid hosp"
        },
        "description": "Daily newly reported hospitalizations where the patient has COVID, as reported by hospital facilities and aggregated in the HHS Protect data collection system.",
        "target_type": "discrete",
        "is_step_ahead": true,
        "time_unit": "day"
    }
]
```

## Step 8: Set up `"submissions_due"`:
- `"submissions_due"` establishes the dates by which model forecasts must be submitted to the hub. It is used by `hubValidations` when validating submission files.

The schema permits two ways to set the dates during which model forecasts can be submitted:

1. By setting a `"relative_to"` date, as well as `"start"` and `"end"` integers, which set the range of dates in which submissions are accepted, as explained in the example below.
- <mark style="background-color: #FFE331">`"relative_to"` specifies</mark> the *task id* variable with which submission start and end dates are calculated.  In this instance, it is `"origin_date"`.
- <mark style="background-color: #32E331">`"start"` is a number</mark> used to calculate the beginning of the submission period, based on the `origin_date`. In this example, the start date is six days **prior** to `origin_date`.
- <mark style="background-color: #38C7ED">On the other hand, `"end"` is a number</mark> used to calculate when the submission period is finished, based on the `origin_date`. In this example, the end date is one day **after** `origin_date`.
- For instance, as was mentioned before, in this file, `2022-11-28` is allowed as an `origin_date`. In this case, submissions are due between "2022-11-22" (six days prior) and "2022-11-29" (one day after).

```{image} ../images/tasks-schema-8.png
:alt: Last lines of code in the tasks.json file
:class: bordered
```
---
2. By setting explicit `"start"` and `"end"` dates (rather than integers as in the previous case), during which forecast submissions are accepted. In this case, the `"relative_to"` line should be omitted altogether, as in the example below:

```
"submissions_due": {
    "start": "2022-06-07",
    "end": "2022-07-20"
}
```
<br/>

 ## Step 9: Optional - set up `"output_type_id_datatype"`:

Once all modeling tasks and rounds have been configured, you may also choose to fix the `output_type_id` column data type across all model output files of the hub using the optional `"output_type_id_datatype"` property.

This property should be provided at the top level of `tasks.json` (i.e., sibling to `rounds` and `schema_version`) and can take any of the following values: `"auto"`, `"character"`, `"double"`, `"integer"`, `"logical"`, `"Date"`.

```{code-block} json
:force: true
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v*/tasks-schema.json",
  "rounds": [...],
  "output_type_id_datatype": "character"
}
```

For more context and details on when and how to use this setting, please see the [`output_type_id` column data type section](output-type-id-datatype) on the **model output** page.
