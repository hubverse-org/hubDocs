# Hub configuration files

## Directory structure
The `hub-config` directory in a modeling hub is required to contain three JSON[^json] files:
   1. `admin.json`{.codeitem} - JSON file containing generic information about the hub and static configuration settings for downstream tools such as validations, visualizations, etc. This file also contains optional cloud settings for hubs that use cloud storage. See the [hub administrative configuration (`admin.json`) interactive schema section](#hub-admin-config) below for details on the `admin.json` file.
   2. `tasks.json`{.codeitem} - JSON file specifying modeling tasks and model output formats, which may be round-specific. See the [hub model task configuration (`tasks.json` file) section](#tasks-metadata) below for more details on the `tasks.json` file.
   3. `model-metadata-schema.json`{.codeitem} - JSON file defining format of model metadata files. The [template metadata schema file section](#model-metadata-schema) has more information on the `model-metadata-schema.json` file.

Hubs with target data may contain the following optional JSON file:
   4. `target-data`{.codeitem} - JSON file defining a `target_data_metadata` object with top-level properties that describe expectations across target datasets 

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

The target data configuration file defines a `target_data_metadata` object with top-level properties that describe expectations across target datasets.

(hub-admin-config)=
### Hub target-data-schema configuration (`target-data.json`) interactive schema
https://github.com/reichlab/decisions/blob/main/decisions/2025-06-17-RFC-target-data-metadata.md#target-data-schemajson
