(hub-metadata)=
# Hub configuration files

## Directory Structure
The `hub-config` directory in a modeling hub is required to contain three files:
   1. `admin.json` - JSON  file defining Hub modeling targets
   2. `tasks.json` - JSON file defining information about model submission validation
   3. `model-metadata-schema.json` - Json or yaml file defining format of model metadata files

```{caution}
Note:  Due to technical issues, we do not currently support json references or yaml metadata files.
```


## Purpose
Hub metadata specifies general configurations for a hub as well as (possibly round-specific) details of what model outputs are requested or required. Hub metadata are used for:
* Validating model output submissions
   * submissions must adhere to the file formats and value combinations specified in the hub metadata.
* Scoring model outputs
   * the hub metadata specifies the scores that are used
   * the task id variables specified in the hub metadata can be used to join model output data with truth data for the purpose of scoring forecasts.
* Configuring model output visualizations
   * Visualization tools may benefit from the ability to programmatically identify task id variables so that a separate visualization of model outputs can be generated for each combination of those variables (e.g. via facetting or menu selections). For example, it may be beneficial to produce separate visualizations for different locations or scenario ids.
   * Visualization tools may give special treatment to the hub’s ensemble and baseline models, which are identified in the hub metadata.
* Report generation
   * The hub’s ensemble and baseline models may be treated specially in reports

## Recommended Standards
We divide the hub metadata into two files:
1. `admin.json` Generic information about the hub as well as static configuration settings for downstream tools such as validations, visualizations, etc.
2. `tasks.json`: Specifications of the modeling tasks and model output formats, which may be round-specific.

These are described separately in the following subsections.

## Hub administrative metadata (`admin.json` file)

The administrative hub metadata file contains settings that are expected to remain fixed throughout a hub’s existence, or for which it is not required to retain past values in order to work with hub data.

### Hub administrative metadata (`admin.json`) Interactive Schema

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/schemas/main/v0.0.1/admin-schema.json"></script>

   Other things we may want to consider adding here:
* Something about truth data?
* Something about scoring?
* Something about report generation?

(tasks_metadata)=
## Hub model task metadata (`tasks.json` file)
The hub model task metadata file specifies the model tasks and model output formats for the hub. 

### Model Tasks (`tasks.json`) Interactive Schema

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/schemas/main/v0.0.1/tasks-schema.json"></script>
