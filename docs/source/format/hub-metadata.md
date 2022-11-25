# Hub Metadata

## Directory Structure
The `hub-config` directory in a modeling hub is required to contain three files:
   1. `admin.json` - JSON  file defining Hub modeling targets
   2. `tasks.json` - JSON file defining information about model submission validation
   3. `model-metadata-schema.json` - Json or yaml file defining format of model metadata files.

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


   <script src="../../node_modules/docson/public/js/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/schemas/main/admin-schema.json"></script>

   Other things we may want to consider adding here:
* Something about truth data?
* Something about scoring?
* Something about report generation?

## Hub model task metadata (`tasks.json` file)
The hub model task metadata file specifies the model tasks and model output formats for the hub. To reduce redundancy, hubs may optionally specify a 'defaults' entry with values that apply unless they are overridden by round-specific entries; this may be particularly useful for forecast hubs, which typically accept the same formats for all rounds.


The hub model task metadata should follow this format:


* Top level object
   * property named `“model_tasks”`, which is an object
      * Each element of the model_tasks object corresponds to one submission round; its name specifies the round id. Hubs may optionally specify one entry named `“default”`, with settings that apply to all rounds; as noted above, this will primarily be of use in forecast hubs. The element for a single submission round is an array.
         * Each element of the array for a single submission round is an object with two properties: `“task_ids”` and `“output_types”`.
            * “Task_ids”
   * Optionally, the top level object may contain other objects that define model task or output type definitions that are referenced multiple times.

```json
{
  "model_tasks": [
    "default": [
      {
        "task_ids": {
          "location": {
            "required": {
              "$ref": "#/$defs/task_ids/location/us_states"
            },
            "optional": {
              "$ref": "#/$defs/task_ids/location/us_counties"
            },
          },
          "age_group": {
            "required": {
              "$ref": "#/$defs/task_ids/age_group/all_ages"
            },
            "optional": {
              "$ref": "#/$defs/task_ids/age_group/age_subdivisions"
            },
          },
          "horizon": {
            "required": null,
            "optional": {
              "$ref": "#/$defs/task_ids/horizon/valid_horizons"
            },
          },
          "outcome_variable": {
            "required": null,
            "optional": {
              "$ref": "#/$defs/task_ids/outcome_variable/cases"
            },
          }
        },
        "output_types": {
          "mean": {
            "required": false
          },
          "bin_prob": {
            "required": {
              "$ref": "#/$defs/output_type_ids/short_term_inc_bins"
            },
            "optional": null
          }
        }
      },
      {
        "task_ids": {
          "location": {
            "required": {
              "$ref": "#/$defs/task_ids/location/us_states"
            },
            "optional": null,
          },
          "age_group": {
            "required": {
              "$ref": "#/$defs/task_ids/age_group/all_ages"
            },
            "optional": {
              "$ref": "#/$defs/task_ids/age_group/age_subdivisions"
            },
          },
          "horizon": {
            "required": null,
            "optional": {
              "$ref": "#/$defs/task_ids/horizon/valid_horizons"
            },
          },
          "outcome_variable": {
            "required": null,
            "optional": {
              "$ref": "#/$defs/task_ids/outcome_variable/hosps_and_deaths"
            },
          }
        },
        "output_types": {
          "mean": {
            "required": false
          },
          "cdf": {
            "required": [10.0, 20.0],
            "optional": null
          }
        }
      },
      {
        "task_groups":
        "output_types":
      },
    ],
    "round-1": [
      // if needed, a complete specification of settings for round 1 here
    ],
    "round-2": [
      // if needed, a complete specification of settings for round 2 here
    ]
  ],


  "$defs": {
    "task_ids": {
      "location": {
        "us_nat_states": ["US", "01", "02", ..., "56"],
        "us_counties": ["01001", ..., "56045"]
      },
      "age_group": {
        "all_ages": ["all_ages"]
        "age_subdivisions": ["0-5 yr", ..., "65+ yr"]
      },
      "horizon": {
        "weekly_horizons": [1, 2, 3, 4],
        "daily_horizons": [1, .., 28]
      },
      "outcome_variable": …
    }
  }
}
```

With options for `task_ids` and forecast representations broken down into those that are required and those that are optional, with valid values/combinations of values specified using something like a `$ref` to a top-level list of options.

### Model Tasks (`tasks.json`) Interactive Schema

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/schemas/main/tasks-schema.json"></script>
