# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in the `model-output` directory of a hub repository.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository. 


The directory and file structure of a modeling hub should contain only the following directories and files:

| Component | Hub name, location, format | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | ------ | 
| Documentation file | e.g., README.md file, located in top level of hub and within each directory | File containing info about the hub structure and additional details about each of the directories| X | - |



| EW202242 | weekly rate | 1 | quantile | 0.25 | 2 |
| EW202242 | weekly rate | 1 | quantile | 0.5 | 3 |
| EW202242 | weekly rate | 1 | quantile | 0.75 | 10 |
| EW202242 | weekly rate | 1 | pmf | 0 | 0.1 |
| EW202242 | weekly rate | 1 | pmf | 0.1 | 0.2 |
| EW202242 | weekly rate | 1 | pmf | 0.2 | 0.7 |
| EW202242 | peak week | NA | pmf | EW202240 | 0.001 |
| EW202242 | peak week | NA | pmf | EW202241 | 0.002 |
| EW202242 | ... | ... | ... | ... | ... |
| EW202242 | peak week | NA | pmf | EW202320 | 0.013 |
| EW202242 | weekly rate | 1 | sample | 1 | 3 |
| EW202242 | weekly rate | 1 | sample | 2 | 3 |
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

