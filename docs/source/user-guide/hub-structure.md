# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in the `model-output` directory of a hub repository.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository. 


The directory and file structure of a modeling hub should contain only the following directories and files:

| Component | Hub name, location, format | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| `Documentation` file | e.g., `README.md` file, located in top level of hub and within each directory | File containing info about the hub structure and additional details about each of the directories| X |  |
| `Configuration` directory | `hub-config` --> /hub-config/ | Folder storing configuration files | X |  |
| Admin configuration file | `admin` --> /hub-config/admin.json | Structured text file containing overall configuration settings for the hub | X |  | 
| Modeling tasks configuration file | `tasks` --> /hub-config/tasks.json | Structured text file that defines modeling tasks and therefore implicity defines the assumed structure for any model submitted | X |  | 
| Model metadata configuration file | `model-metadata-schema` --> /hub-config/model-metadata-schema.json | Structured text file that defines the expected format of model metadata files submitted by modeling teams | X |  |  
| `Model output` directory | `model-output` --> /model-output | Folder to collect modeling team model submissions | X |  | 
| Model output subdirectory | `team1-modela` --> /model-output/team1-modela | Model-specific subdirectory for submissions from one modeling team |  | X | 
| Model output file | `<round-id1>-<model_id>` --> /model-output/team1-modela/<round-id1><model_id>.csv or .parquet| Round-specific model submission file |  | X | 
| `Model metadata` directory | `model-metadata` --> /model-metadata | Folder to collect modeling team model metadata submissions | X | | 
| Model metadata submission file | `team1-modela` --> /model-metadata/team1-modela.yml | Model-specific metadata submission file |  | X | 
| `Model abstracts` directory (optional) | `model-abstracts` --> /model-abstracts | Folder to collect optional round-specific model metadata | X |  | 
| Model abstract subdirectory | `team1-modela` --> /model-abstracts/team1-modela | Model-specific subdirectory for round-specific model metadata |  | X | 
| Model abstract submission file | `<round-id1>` --> /model-abstracts/team1-modela/<round-id1.md | Round-specific model metadata submission |  | X | 
| `Target data` directory (optional)| `target-data` --> /target-data| Folder to store actual observed (i.e., target) values of an outcome (or links to external open-access sources) and information on how  model targets can be calculated from target data | X | | 
| `Auxiliary data` directory (optional) | `auxiliary-data` --> /auxiliary-data | Folder to store any additional data related to modeling efforts | X |  | 
| `src` directory (optional) | `src` --> /src | Folder to store code that is present in the hub repository | X |  | 




* Optionally, any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. 

Although most hubs to date have been housed in GitHub repositories, the proposed structure is more general and can be adapted for use on any shared filesystem. 

