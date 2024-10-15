# Model metadata

## Directory structure  
The `model-metadata` directory in a modeling hub is required to contain yaml metadata files, one for each model submitting models such as forecasts to the hub. So, the contents of the directory will be a set of files named as follows:  

* `team1-modela.yml`  
* `team1-modelb.yml`  
* `team2-modela.yml`  

Note that the same team can submit more than one model.  

## Purpose  
Model metadata describes the characteristics of models contributing to a hub.  
The general goals for model metadata are that  
1. explicit requirements for model metadata should be minimal  
2. hubs may set fields to be required as necessary for that hub.  

Note: Model metadata is a required feature of a hub and describes the characteristics of models contributing to a hub, while [model abstracts](../user-guide/model-abstracts.md) is an optional feature of a hub that is useful for keeping track of round-specific detailed narrative descriptions modeling methods and results.

## Recommended standards  
Many hubs will use a standard set of metadata fields, which we place in the following template schema. Individual hubs may want to add additional metadata fields. These should be selected to specify fields likely to remain stable across rounds, leaving model attributes expected to change across rounds to be described in round-specific abstracts. For consistency across Hubs, we encourage using a common set of metadata fields with standard names and definitions. We describe fields used in past Hubs in a second section below the template file.  

(model-metadata-schema)=
## Template metadata schema file  

The following is a [template `model-metadata-schema.json` file from the **example complex forecast hub**](https://github.com/hubverse-org/example-complex-forecast-hub/blob/main/hub-config/model-metadata-schema.json), which is itself drawn from the [**FluSight Forecast Hub**](https://github.com/cdcepi/FluSight-forecast-hub/blob/main/model-metadata/README.md). Many Hubs will use the same fields listed in the *template metadata schema file*, but some may need fewer or more. A hub's *model metadata schema file* should include either the single combined field `model_id`, or both of the fields `team_abbr` and `model_abbr`. Administrators can remove other fields as needed and use [additional optional metadata fields from this list](#optional-additional-metadata-fields). We encourage administrators to use the same standard names and definitions to maintain consistency across hubs.  

   <script src="../_static/docson/widget.js" data-schema="https://raw.githubusercontent.com/hubverse-org/example-complex-forecast-hub/main/hub-config/model-metadata-schema.json"></script>


(optional-additional-metadata-fields)=
## Optional additional metadata fields  
Depending on the goals and context of a particular hub, it may be beneficial to collect more information about the modeling assumptions made by models. The following fields have been included within the model_details metadata field in past Hubs. Where applicable, we recommend that hubs draw from this list to encourage standardization of terminology across Hubs. If Hubs develop new model metadata items, these should be added to this list for future reference.  

   <script src="../_static/docson/widget.js" data-schema="../../_static/other-metadata-fields.json"></script>

