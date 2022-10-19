# Hub Metadata

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


Additionally, we note that there are some redundancies between the hub metadata and configuration files that are used for Zoltar and the schema for data format used in validation. We anticipate that it may be possible to generate those files from the hub metadata.
Recommended Standards
We divide the hub metadata into two files:
1. Generic information about the hub as well as static configuration settings for downstream tools such as validations, visualizations, etc.
2. Specifications of the modeling tasks and model output formats, which may be round-specific.


These are described separately in the following subsections.
