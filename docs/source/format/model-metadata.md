# Model metadata

## Directory structure
The `model-metadata` directory in a modeling hub is required to contain yaml metadata files, one for each model that is submitting forecasts to the hub. So the contents of the directory will be a set of files named as follows:

* `team1-modela.yml`
* `team1-modelb.yml`
* `team2-modela.yml`

Note that the same team can submit more than one model.

## Purpose
Model metadata describe characteristics of models contributing to a Hub.
General goals for model metadata are that
1. explicit requirements for model metadata should be minimal
2. hubs may set fields to be required as necessary for that hub.

## Recommended Standards
Many hubs will use a common set of metadata fields, which we place in the following template schema. Individual hubs may want to add additional metadata fields. These should be selected with the goal of specifying fields that are likely to remain stable across rounds, leaving model attributes that are likely to change across rounds to be described in round-specific abstracts. For consistency across Hubs, we encourage the use of a common set of metadata fields with standard names and definitions. We describe fields that have been used in past Hubs in a second section below the template file.

## Template metadata schema file

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/Infectious-Disease-Modeling-Hubs/schemas/main/v0.0.0.9/model-schema.json"></script>


```yaml
$schema: "http://json-schema.org/draft-07/schema"[am]
title: ForecastHub model metadata
description: >
  This is the schema of the model metadata file, please refer to
  https://github.com/epiforecasts/covid19-forecast-hub-europe/wiki/Metadata[an]
  for more information.
type: object
properties:
  team_name:
    description: The name of the team submitting the model
    type: string
  team_abbr:
    description: Abbreviated name of the team submitting the model
    type: string
    pattern: ^[a-zA-Z0-9_+]+$
    maxLength: 16
  model_name:
    description: The name of the model
    type: string
  model_abbr:
    description: Abbreviated name of the model
    type: string
    pattern: ^[a-zA-Z0-9_+]+$
    maxLength: 16[ao]
  model_version:
    description: Identifier of the version of the model
    type: string[ap]
  model_contributors:
    type: array
    items:
      type: object
      properties:
        name:
          type: string
        affiliation:
          type: string
        orcid:
          type: string
          # This is a quite loose pattern. See https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
          pattern: ^\d{4}\-\d{4}\-\d{4}\-[\dX]{4}$
        email:
          type: string
          format: email
        twitter:
          type: string
        additionalProperties: false[aq]
  website_url:
    description: Public facing website for the model
    type: string
    format: uri[ar]
  repo_url:
    description: code for the model
    type: string
    format: uri
  license:
    description: License for use of model output data
    type: string
    enum:
      - "apache-2.0"
      - "cc-by-4.0"
      - "cc-by-nc-4.0"
      - "cc-by-nc-nd-4.0"
      - "cc-by-sa-4.0"
      - "gpl-3.0"
      - "lgpl-3.0"[as]
      - "mit"[at][au][av]
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
  citation:
    type: string[az]
  team_funding:
    type: string
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

## Optional additional metadata fields
Depending on the goals and context of a particular Hub, it may be beneficial to collect more information about the modeling assumptions made by models. The following fields have been included within the model_details metadata field in past Hubs. Where applicable, we recommend that hubs draw from this list to encourage standardization of terminology across Hubs. If Hubs develop new model metadata items, they should be added to this list for future reference.

```yaml
      ensemble_of_hub_models:
        description: >
          Indicator for whether this model is an ensemble of other Hub models
        type: boolean
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
```