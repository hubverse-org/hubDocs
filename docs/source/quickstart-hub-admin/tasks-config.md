# Configuring tasks  

Every Hub is organized around "modeling tasks" that are defined to meet the needs of a project. Modeling tasks are defined for a hub in the [`tasks.json`](#model-tasks-schema) file, which specifies the three components of modeling tasks ([task ID variables](#task-id-vars), [output types](#output-types), and [target metadata](#target-metadata)). Here is [a detailed definition of modeling tasks](../user-guide/tasks.md).  

## Step 1: Open `tasks.json`  

Check to be sure you are in  the `hub-config` folder. Click on `tasks.json` to open the file.  

```{image} ../images/tasks-json.png
:alt: Screenshot of how to open tasks.json file in RStudio
:class: bordered
```

## Step 2: Examine the `tasks.json` file  

In your source panel (upper left hand panel), you should see the code below. [Here is a description of each line of code in `tasks.json`](#model-tasks-schema).  

```{image} ../images/tasks-schema-0.png
:alt: Screenshot of the code in the tasks.json file
:class: bordered
```

This `tasks.json` file serves as a template, and has very few values filled out, which gives the user flexibility to adapt the Hub to their own needs. Nevertheless, in order to learn how to properly use this schema, we will use a "premade" `tasks.json` file from the [Simple Forecast Hub Example](https://github.com/hubverse-org/example-simple-forecast-hub) that already has values filled in, which will better illustrate what should go in each section.  

## Step 3: Close the `tasks.json` file in RStudio  

Make sure the `tasks.json` file in RStudio is closed, by clicking on the 'x' icon, as indicated below.  

```{image} ../images/tasks-close.png
:alt: Screenshot of how to close tasks.json file in RStudio
:class: bordered
```

## Step 4: Download a premade `tasks.json` file  

You can [use this link to download the `tasks.json` file](https://github.com/hubverse-org/example-simple-forecast-hub/blob/main/hub-config/tasks.json) from the Example Forecast Hub by clicking on the *Download Raw File* icon as indicated below.  

```{image} ../images/tasks-download.png
:alt: Screenshot of how to download a tasks.json file from GitHub
:class: bordered
```

Save the file in the `hub-config` folder (which is [in your repository on your local computer](#clone-repo)). This new file should replace the existing `tasks.json` file that was in this folder.  

### 4.1: Examine the new `tasks.json` file  

Open `tasks.json` and explore the content and structure. Some [key concepts are defined here](../overview/definitions.md), and [a full explanation of all the supported elements in a `tasks.json` file can be found here](https://raw.githubusercontent.com/hubverse-org/schemas/main/v2.0.1/tasks-schema.json). Simple explanations for elements in the Example Forecast Hub file are offered below:  

* `schema_version`: Modeling Hub [Schema](../overview/definitions.md) versions are all housed in [this repository](https://github.com/hubverse-org/schemas/).  
* `round_id`: The [round](../overview/definitions.md) identifier establishes which date from a forecast submission is used to identify the submission round it corresponds to (e.g., the origin date).  
* `model_tasks`: Model [tasks](../overview/definitions.md) include all the goals of the modeling effort, including the `task_ids`, `output_type`, and `target_metadata`.  
* `task_ids`: The [task](../overview/definitions.md) identifiers set the optional and required elements that go into a forecast submission, such as the `target`, `horizon`, `location`, and `origin date`.  
* `origin_date`: The date when a forecast was generated. More information on this and other dates, including how to use the `origin_date` to calculate the `target_date` can be found [in the section on the usage of task ID variables](#task-id-use).  
* `horizon`: Sets the time range for which forecast predictions are to be made. For instance, these can be days into the future, or even days into the past, as in [nowcasts](../overview/definitions.md).  
* `location`: The geographic identifier, such as country codes or FIPS state/county level codes.  
* `output_type`: A [Model output](../overview/definitions.md) type establishes the valid model output types such as the mean, or specific quantiles. A more detailed explanation of model outputs can be found [in the section on model output formats](#model-output-format).  

Now, read below for details on some of the lines of code in this file:  

(tasks-json-edits)=
## Step 5: Define `"task_ids"`
### 5.1. Establishing the `"round_id"` and `"origin_date"` *(starting point)*:  
- <mark style="background-color: #32E331">The code highlighted in green</mark> establishes that the *round identifier* is encoded by a *task id* variable in the data.  
- <mark style="background-color: #38C7ED">The code highlighted in light blue</mark> sets the *round identifier* as `"origin_date"`.  
- `task_ids` includes the variables `origin_date`, `target`, `horizon`, and `location`.  
- <mark style="background-color: #FFE331">The first variable, `origin_date` is highlighted in yellow</mark> and states that no *origin dates* are required, and that there are three valid, possible dates (`"2022-11-28", "2022-12-05", "2022-12-12"`). To be clear, no specific `origin_date` is required because every submission will have a different `origin_date` as each submission corresponds to a different forecasting time period (compare this with `location`, where some specific locations may be required for every submission.  

```{image} ../images/tasks-schema-1.png
:alt: Some of the initial lines of code in the tasks.json file
:class: bordered
```

### 5.2. Setting the `"target"`:  
- <mark style="background-color: #32E331">The second line</mark> states that `"inc covid hosp"` for example is the required target. Additional required targets could be added here.  
- <mark style="background-color: #38C7ED">The third line</mark> states that there are no other optional targets that are valid. You could add `["cum covid hosp"]` for example if you wanted to allow that target, but not require it.  

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

[Further details explaining how to use `target_date` and `target_end_date` can be found here](https://raw.githubusercontent.com/hubverse-org/schemas/main/v2.0.1/tasks-schema.json#L400).  

(setting-up-location)=
### 5.4. Setting up `"location"`:  
- The `location` refers to the geographic identifier, such as country codes or FIPS state/county level codes.  
- <mark style="background-color: #32E331">The second line</mark> states that no particular location is required, although in some instances, certain locations might be required for all submissions.  
- <mark style="background-color: #38C7ED">The third line</mark> indicates the locations that may be submitted. In this example, they are FIPS codes for US states and territories.  

```{image} ../images/tasks-schema-4.png
:alt: Even more lines of code in the tasks.json file
:class: bordered
```

### 5.5. `required` and `optional` elements:  

As seen previously, each `task_ids` has a `required` and an `optional` property, to indicate expected information and possible additional information, respectively.  

- To indicate **no possible additional information**, **`optional` can be set to `null`**.  
- If **`required` is set to `null`** but `optional` contains values, (see for example [`"location"`](#setting-up-location)): **no particular value is required but at least one of the `optional` values is expected**.  
- There may be cases where we have **multiple `model_tasks` and a given task id is relevant to one or more model tasks, but not to others.** For example, in the code snippet below, the `horizon` task id is relevant to the first model task, whose `target` is `inc covid hosp`, and any one of the optional values specified are expected in the `horizon` column in a model output file. However, **`horizon` is not relevant to the second model task**, whose `target` is `peak size`. For this model task, **both `required` and `optional` are set to `null`** in the `horizon` task ID configuration and `NA` is expected in the `horizon` column in model output files.  

```
"model_tasks": [{
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
                ],
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
                "target_metadata": [
                    {
                       "target_id": "peak size hosp",
                       "target_name": "COVID-19 peak size hospitalizations",
                       "target_units": "count",
                       "target_keys": {
                           "target": "peak size hosp"
                       },
                       "description": "Magnitude of the peak of hospitalizations where the patient has COVID",
                       "target_type": "discrete",
                       "is_step_ahead": false
                    }
                ]
            }]


```

## Step 6: Define [`"output_type"`](#model-output-format):  
- The [`output_type`](#model-output-format) is used to establish the valid model output types for a given modeling task. In this example they include `mean` and `quantile`, but `median`, `cdf`, `pmf`, and `sample` are other supported output types. Output types have two additional properties, an `output_type_id` and  a `value` property, both of which establish the valid values that can be entered for this output type.  

### 6.1. Setting the `"mean"`:  
- <mark style="background-color: #FFE331">Here, the `"mean"` of the predictive distribution</mark> is set as a valid value for a submission file.  
- <mark style="background-color: #32E331">`"output_type_id"` is used</mark> to determine whether the `mean` is a required or an optional `output_type`. Both `"required"` and `"optional"` should be declared, and the option that is chosen (required or optional) should be set to `["NA"]`, whereas the one that is not chosen, should be set to `null`. In this example, the mean is optional, not required. If the mean is required, `"required"` should be set to `["NA"]`, and `"optional"` should be set to `null`.  
- <mark style="background-color: #38C7ED">`"value"` sets the characteristics</mark> of this valid `output_type` (i.e., the mean). In this instance, the value must be an `integer` greater than or equal to `0`.  

```{image} ../images/tasks-schema-6-1.png
:alt: Some more lines of code in the tasks.json file
:class: bordered
```

### 6.2. Setting up `"quantile"`:  
- <mark style="background-color: #FFE331">Here, `quantile` specifies</mark> what quantiles of the predictive distribution are valid values for a submission file.  
- <mark style="background-color: #32E331">In this case, `"output_type_id"` establishes</mark> that this is a required `output_type`, and it sets the accepted probability levels at which quantiles of the predictive distribution will be recorded. In this case, quantiles are required at discrete levels that range from `0.01` to `0.99`.  **Quantile `output_type_id` values must NOT contain trailing zeros** as this will cause submission validation checks to fail.  
- <mark style="background-color: #38C7ED">As before, `"value"` sets the characteristics</mark> of valid `quantile` values. In this instance, the values must be integers greater than or equal to `0`.  

```{image} ../images/tasks-schema-6-2.png
:alt: And more lines of code in the tasks.json file
:class: bordered
:width: 300px
```

## Step 7: Defining `"target_metadata"`:  
- `"target_metadata"` defines the characteristics of each unique `target`.  
- <mark style="background-color: #FFE331">To begin with, `"target_id"` is</mark> a short description that uniquely identifies the target.  
- <mark style="background-color: #32E331">Similarly, `"target_name"` provides</mark> a longer, human readable description of the target.  
- <mark style="background-color: #38C7ED">`"target_units"` indicates</mark> the unit of observation used for this target.  In this instance, the unit is count.  
- <mark style="background-color: #F50088">`"target_keys"` must match</mark> a target set in `task_ids`, to appropriately identify it.  In this instance, the target is `"inc covid hosp"`.  
- The `"description"` is a verbose explanation of the target, which might include details on the measure used for the target, as shown in the example below.  
- <mark style="background-color: #FF4D18">The `"target_type"` defines</mark> the target's statistical data type. In this instance, the target uses discrete data.  
- <mark style="background-color: #FFE331">`"is_step_ahead"` indicates</mark> whether the target is part of a sequence of values.  In this instance, it is.  
- <mark style="background-color: #32E331">`"time_unit"` defines</mark> the units of the time steps. In this case, it is days.  

```{image} ../images/tasks-schema-7.png
:alt: Target metadata lines of code in the tasks.json file
:class: bordered
```

## Step 8: Set up `"submissions_due"`:  
- `"submissions_due"` establishes the dates by which model forecasts must be submitted to the hub. It is used by `hubValidations` when validating submission files.  
  
There are [two ways](https://github.com/hubverse-org/schemas/blob/de580d56b8fc5c24dd36a32994182e37b8b0ac95/v2.0.0/tasks-schema.json#L1323-L1380) in which one can set the dates during which model forecasts can be submitted:  
  
1. By setting a `"relative_to"` date, as well as `"start"` and `"end"` integers which set the range of dates in which submissions are accepted, as explained in the example below.  
- <mark style="background-color: #FFE331">`"relative_to"` specifies</mark> the *task id* variable in relation to which submission start and end dates are calculated.  In this instance it is `"origin_date"`.  
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
  
 ## Step 9: Optional - Set up `"output_type_id_datatype"`:   

Once all modeling tasks and rounds have been configured, you may also choose to fix the `output_type_id` column data type across all model output files of the hub using the optional `"output_type_id_datatype"` property.

This property should be provided at the top level of `tasks.json` (i.e. sibling to `rounds` and `schema_version`) and can take any of the following values: `"auto"`, `"character"`, `"double"`, `"integer"`, `"logical"`, `"Date"`.

```json
{
  "schema_version": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v3.0.1/tasks-schema.json",
  "rounds": [...],
  "output_type_id_datatype": "character"
}
```

For more context and details on when and how to use this setting, please see the [`output_type_id` column data type](output-type-id-datatype) section on the **model output** page.
