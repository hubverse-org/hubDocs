# Model metadata

## Directory structure  
The `model-metadata` directory in a modeling hub is required to contain yaml metadata files, one for each model that is submitting models such as forecasts to the hub. So the contents of the directory will be a set of files named as follows:  

* `team1-modela.yml`  
* `team1-modelb.yml`  
* `team2-modela.yml`  

Note that the same team can submit more than one model.  

## Purpose  
Model metadata describe characteristics of models contributing to a Hub.  
General goals for model metadata are that  
1. explicit requirements for model metadata should be minimal  
2. hubs may set fields to be required as necessary for that hub.  

Note: Model metadata is a required feature of a hub and describes the characteristics of models contributing to a Hub, while [Model abstracts](../user-guide/model-abstracts.md) is an optional feature of a hub that is useful for keeping track of round-specific detailed narrative descriptions modeling methods and results.

## Recommended Standards  
Many hubs will use a common set of metadata fields, which we place in the following template schema. Individual hubs may want to add additional metadata fields. These should be selected with the goal of specifying fields that are likely to remain stable across rounds, leaving model attributes that are likely to change across rounds to be described in round-specific abstracts. For consistency across Hubs, we encourage the use of a common set of metadata fields with standard names and definitions. We describe fields that have been used in past Hubs in a second section below the template file.  

## Template metadata schema file  

The following is a [*template metadata schema file* from the **Example Complex Forecast Hub**](https://github.com/Infectious-Disease-Modeling-Hubs/example-complex-forecast-hub/blob/main/hub-config/model-metadata-schema.json), which is itself drawn from the [FluSight Forecast Hub](https://github.com/cdcepi/FluSight-forecast-hub/blob/main/model-metadata/README.md). Many Hubs will use the same fields used below, but some may need fewer or more. Administrators can remove fiels as needed, and can pick [additional optional metadata fields from the list below](#optional-additional-metadata-fields). We encourage administrators to use the same names to maintain consistency in naming across Hubs.  

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/example-complex-forecast-hub/main/hub-config/model-metadata-schema.json"></script>


## Optional additional metadata fields  
Depending on the goals and context of a particular Hub, it may be beneficial to collect more information about the modeling assumptions made by models. The following fields have been included within the model_details metadata field in past Hubs. Where applicable, we recommend that hubs draw from this list to encourage standardization of terminology across Hubs. If Hubs develop new model metadata items, they should be added to this list for future reference.  

[Test](../files/other-metadata-fields.json)

   <script src="../_static/docson/widget.js" data-schema="../_static/other-metadata-fields.json"></script>



```yaml
      include_viz:
        description: >
          Indicator for whether the model should be included in the
          Hub’s visualization
        type: boolean
      include_ensemble:
        description: >
          Indicator for whether the model should be included in the
          Hub’s ensemble
        type: boolean
      include_eval:
        description: >
          Indicator for whether the model should be scored for inclusion in the
          Hub’s evaluations
        type: boolean[aw][ax][ay]
      ensemble_of_hub_models:
        description: >
          Indicator for whether this model is an ensemble of other Hub models
        type: boolean
      model_details:[ba]
        type: object
        properties:
          data_inputs:
            type: string
          methods:
            type: string
            maxLength: 200
          methods_long:
            type: string
        additionalProperties: false
        required:
          - data_inputs
          - methods
      modeling_NPI:
        type: string
      compliance_NPI:
        type: string
      contact_tracing:
        type: string
      testing:
        type: string
      vaccine_efficacy_transmission:
        type: string
      vaccine_efficacy_delay:
        type: string
      vaccine_hesitancy:
        type: string
      vaccine_immunity_duration:
        type: string
      natural_immunity_duration:
        type: string
      case_fatality_rate:
        type: string
      infection_fatality_rate:
        type: string
      asymptomatics:
        type: string
      age_groups:
        type: string
      importations:
        type: string
      confidence_interval_method:
        type: string
      calibration:
        type: string
      spatial_structure:
        type: string[bc]
additionalProperties: false
required:
  - team_name
  - team_abbr
  - model_name
  - model_abbr
  - model_contributors
  - website_url
  - license
  - include_viz
  - include_ensemble
  - include_eval
  - model_details
```
