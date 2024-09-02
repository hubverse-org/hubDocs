# Hub configuration files

## Directory Structure
The `hub-config` directory in a modeling hub is required to contain three files:
   1. `admin.json` - JSON file containing generic information about the hub as well as static configuration settings for downstream tools such as validations, visualizations, etc. This file also contains optional cloud settings for hubs that use cloud storage. [More details found below](#hub-admin-config).  
   2. `tasks.json` - JSON file specifing modeling tasks and model output formats, which may be round-specific. [More details found below](#tasks-metadata).  
   3. `model-metadata-schema.json` - JSON file defining format of model metadata files. [More information can be found here](#model-metadata-schema).  

```{caution}
Note:  Due to technical issues, we do not currently support json references or yaml metadata files.
```

## Purpose
The files within the `hub-config` directory specify general configurations for a hub as well as (possibly round-specific) details of what model outputs are requested or required. Hub configuration files are used for:
* Validating model output submissions
   * `tasks.json`{.codeitem} file specifies the file format and task id, output type, value combinations (both required or optional) that submitted model output data must adhere to.
   * `tasks.json`{.codeitem} file also specifies the window of submission for each round (with the time zone information in the `admin.json` file). 
* Scoring model outputs
   * the hub configuration files specify the scores that are used
   * the task id variables specified in the `tasks.json` can be used to join model output data with truth data for the purpose of scoring forecasts.
* Configuring model output visualizations
   * Visualization tools may benefit from the ability to programmatically identify task id variables so that a separate visualization of model outputs can be generated for each combination of those variables (e.g. via facetting or menu selections). For example, it may be beneficial to produce separate visualizations for different locations or scenario ids.
   * Visualization tools may give special treatment to the hub’s ensemble and baseline models, which are identified in the hub configuration files.
   * The `tasks.json` file contains metadata regarding the targets including human readable description and units which can be used for visualization 
* Report generation
   * `admin.json`{.codeitem} allows configuration of ensemble and baseline models to be treated specially in reports.


## Hub administrative configuration (`admin.json` file)

The administrative hub configuration file contains global administrative settings that are expected to remain fixed throughout a hub’s existence and applies to all rounds in a hub.

As of v2.0.1, `admin.json` contains optional settings for hubs that store their configuration and model-output data in the cloud (at this time, Amazon Web Services is the supported cloud provider). Like other admin settings, the cloud information should not be updated once the hub has been launched (doing so will break the process that syncs hub data to the cloud).

(hub-admin-config)=
### Hub administrative configuration (`admin.json`) Interactive Schema

#### Schema Version: {{schema_version}}

Please note that the preview below does not show the required fields. Please click on the raw schema link below to see all required fields. 

{{'[See raw schema](https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/admin-schema.json)'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

{{'<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/admin-schema.json"></script>'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

```{note}
   Other things we may want to consider adding here:
* Something about truth data?
* Something about scoring?
* Something about report generation?
```

(tasks-metadata)=
## Hub model task configuration (`tasks.json` file)
The hub model task configuration file specifies the model tasks (tasks id and targets) as well as model output types. The `tasks.json` file is flexible enough to accomodate different style of hubs. Hubs can vary from a simple forecast hub (see [US Forecast Hub example](/user-guide/intro-data-formats.md) to a more complex round related scenario hub (see [US Scenario Modeling Hub example](/user-guide/intro-data-formats.md)).

(model-tasks-schema)=
### Model Tasks (`tasks.json`) Interactive Schema

#### Schema Version: {{schema_version}}
{{'[See raw schema](https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/tasks-schema.json)'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

{{'<script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/schemas/BRANCH/SCHEMA_VERSION/tasks-schema.json"></script>'.replace('SCHEMA_VERSION', schema_version).replace('BRANCH', schema_branch)}}

