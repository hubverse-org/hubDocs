(hub-structure)=
# Structure of Hub repositories

A Hub should be structured according to the following recommendations.  

Generally, Hub file structure is intended primarily as a storage space for primary data. All other code and outputs related to model output validation, visualizations, reports, ensemble construction, etc., should be placed in repositories other than the primary Hub location.

The directory and file structure of a modeling hub should contain only the following directories and files:

* Documentation files
   * Hubs should provide a documentation file (e.g., `README.md`) at the top level that describes the overall structure of the hub, as well as a documentation file within each folder that provides more detail.

* `hub-metadata` directory (see {doc}`/format/hub-metadata`)

* `model-output` directory (see {doc}`/format/model-output`) 

* `model-metadata` directory (see {doc}`/format/model-metadata`)

* `model-abstracts` directory (optional, see {doc}`/format/model-abstracts`)

* `target-data` directory (optional, see {doc}`/format/target-data`)

* `auxiliary-data` (optional, see {doc}`/format/target-data`)

* Optionally, any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. To the extent possible, only the workflow definition files should be stored within the Hub file space, with any additional scripts or functionality residing in an external location.

Although most hubs to date have been housed in GitHub repositories, the proposed structure is more general and can be adapted for use on any shared filesystem. 

