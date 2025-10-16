# Hub configuration files

## Directory structure
The `hub-config` directory in a modeling hub is required to contain three JSON[^json] files:
   1. `admin.json`{.codeitem} - JSON file containing generic information about the hub and static configuration settings for downstream tools such as validations, visualizations, etc. This file also contains optional cloud settings for hubs that use cloud storage. See the [hub administrative configuration (`admin.json`) interactive schema section](#hub-admin-config) below for details on the `admin.json` file.
   2. `tasks.json`{.codeitem} - JSON file specifying modeling tasks and model output formats, which may be round-specific. See the [hub model task configuration (`tasks.json` file) section](#tasks-metadata) below for more details on the `tasks.json` file.
   3. `model-metadata-schema.json`{.codeitem} - JSON file defining format of model metadata files. The [template metadata schema file section](#model-metadata-schema) has more information on the `model-metadata-schema.json` file.

Hubs with target data may contain the following optional JSON file:  
* `target-data`{.codeitem} - JSON file defining a `target_data_metadata` object with top-level properties that describe expectations across target datasets, with the ability to override these defaults for specific dataset types (`time-series` and `oracle-output`). See the [target data configuration (`target-data.json`) preview](#target-data-config) below. 

[^json]: We do not currently support json references or yaml metadata files due to technical issues.


## Purpose

The files within the `hub-config` directory specify general configurations for a hub and (possibly round-specific) details of what model outputs are requested or required. Hub configuration files are used for:
* Validating model output submissions
   * `tasks.json`{.codeitem} file specifies the file format, task ID, output type, and value combinations (both required or optional) the submitted model output data must adhere to
   * `tasks.json`{.codeitem} file also specifies the submission window for each round (with the time zone information in the `admin.json` file)
* Scoring model outputs
   * the hub configuration files specify the scores that are used
   * the task ID variables specified in the `tasks.json` can be used to join model output data with truth data to score forecasts
* Configuring model output visualizations
   * Visualization tools may benefit from programmatically identifying task ID variables so that a separate visualization of model outputs can be generated for each combination of those variables (e.g., via facetting or menu selections). For example, producing separate visualizations for different locations or scenario IDs may be beneficial.
   * The `tasks.json` file contains metadata about the targets, including a human-readable description and units that can be used for visualization.


## Hub administrative configuration (`admin.json` file)

The administrative hub configuration file contains global administrative settings expected to remain fixed throughout a hub’s existence. These settings apply to all rounds in a hub.

As of v2.0.1, `admin.json` contains optional settings for hubs that store their configuration and model-output data in the cloud (at this time, Amazon Web Services is the supported cloud provider). Like other admin settings, the cloud information should not be updated once the hub has been launched (doing so will break the process that syncs hub data to the cloud).

(hub-admin-config)=
### Hub administrative configuration (`admin.json`) interactive schema

#### Schema Version: {{schema_version}}

Please note that the preview below does not show the required fields. Please click on the raw schema link below to see all required fields.

{{'See [raw schema](https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/admin-schema.json)'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

{{'<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/admin-schema.json"></script>'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

(tasks-metadata)=
## Hub model task configuration (`tasks.json` file)
The hub model task configuration file specifies the model tasks (task IDs and targets) and model output types. The `tasks.json` file is flexible enough to accommodate different hub styles. Hubs can vary from a simple forecast hub (see [US Forecast Hub example](/user-guide/intro-data-formats.md) to a more complex round-related scenario hub (see [US Scenario Modeling Hub example](/user-guide/intro-data-formats.md)).

(model-tasks-schema)=
### Model tasks (`tasks.json`) interactive schema

#### Schema Version: {{schema_version}}
{{'See [raw schema](https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/tasks-schema.json)'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

{{'<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/tasks-schema.json"></script>'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

## Hub target data configuration (`target-data.json` file)

For hubs that use target data, the optional target data configuration file defines a `target_data_metadata` object with top-level properties that describe expectations across target datasets. Top-level properties can be overridden  as well as time series- and oracle output-specific configuration.

(target-data-config)=
### Hub target data configuration (`target-data.json`) schema preview
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/target-data-schema.json",
    "title": "Schema for Modeling Hub target data definitions",
    "description": "This is the schema of the target-data.json configuration file that defines metadata about target data used to visualise and evaluate modeling hub model outputs.",
    "type": "object",
    "description": "Target data metadata.",
    "properties": {
        "target_data_metadata": {
            "type": "object",
            "properties": {
                "observable_unit": {
                            "description": "Names of columns whose unique value combinations define the minimum observable unit in time-series data. Each combination of values must be unique across `as_of` data versions if applicable. The majority are expected to correspond to task ID names but may include other columns as well (e.g. the general `date` column).",
                        "type": "array",
                        "uniqueItems": true,
                        "items": {
                            "type": "string"
                        }
                },
                "date_col": {
                    "description": "Name of the date column across hub data (time-series, oracle-output and model output). This is the column that stores the date on which observed data actually occured.",
                    "type": ["string", "null"],
                    "default": null
                },
                "time-series": {
                    "type": "object",
                    "properties": {
                        "non_task_id_schema": {
                            "type": "object",
                            "uniqueItems": true,
                            "description": "Key-value pairs of non-task ID column names and data types found in time-series data. Include any columns in the time-series data that does not correspond exactly to a task ID. If an `as_of` column is included, it should be specified here as well.",
                            "examples": [
                                {
                                    "location_name": "character"
                                },{
                                    "date": "Date"
                                }
                            ],
                            "additionalProperties": {
                                "type": "string",
                                "enum": ["character", "double", "integer","logical", "Date"]
                            }
                        },
                        "versioned": {
                            "description": "Indicates whether time-series data are versioned using `as_of` dates. If true, the data is expected to have a date `as_of` column that indicates the version of each data point.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "additionalProperties": false
                },
                "oracle-output": {
                    "type": "object",
                    "properties": {
                        "has_output_type_ids": {
                            "type": "boolean",
                            "description": "Indicates whether the oracle output data have an `output_type` and `output_type_id` column. These columns are necessary if hub includes `pmf` and `cdf` output types but optional otherwise.",
                            "default": false
                        },
                        "observable_unit": {
                            "description": "Names of task IDs whose unique value combinations define an observable unit in oracle output data. Each combination of values must be unique once combined with output type IDs. Can be used to override default observable units in situations where some output types require additional task ID value to map onto target data.",
                            "type": "array",
                            "uniqueItems": true,
                            "items": {
                                "type": "string"
                            }
                        },
                        "versioned": {
                            "description": "Indicates whether oracle-output data are versioned using `as_of` dates. If true, the data is expected to have a date `as_of` column that indicates the version of each data point.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "additionalProperties": false
                }
            },
            "required": ["observable_unit", "date_col"],
            "additionalProperties": false
        }
    }
}
```

