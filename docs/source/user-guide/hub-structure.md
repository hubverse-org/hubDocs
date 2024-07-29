# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in the `model-output` directory of a hub repository.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository. 


The directory and file structure of a modeling hub should contain only the following directories and files:

* Documentation files
   * Hubs should provide a documentation file (e.g., `README.md`) at the top level that describes the overall structure of the hub, as well as a documentation file within each folder that provides more detail.

* `hub-config ` directory (see {doc}`/user-guide/hub-config`)

* `model-output` directory (see {doc}`/user-guide/model-output`) 

* `model-metadata` directory (see {doc}`/user-guide/model-metadata`)

* `model-abstracts` directory (optional, see {doc}`/user-guide/model-abstracts`)

* `target-data` directory (optional, see {doc}`/user-guide/target-data`)

* `auxiliary-data` directory (optional, see {doc}`/user-guide/target-data`)
  
* `src` directory (optional, for code that is present in the hub repository)

* Optionally, any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. 

Although most hubs to date have been housed in GitHub repositories, the proposed structure is more general and can be adapted for use on any shared filesystem. 

