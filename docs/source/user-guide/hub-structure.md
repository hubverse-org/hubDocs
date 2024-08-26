# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in the `model-output` directory of a hub repository.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository. 


The directory and file structure of a modeling hub should contain only the following directories, subdirectories, and files:

## Required Components

``` {table} Documentation (README.md)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Documentation file | e.g., `README.md` file, located in the top level of a hub and within each directory | File containing info about the hub structure and additional details about each of the directories| X |  |
```

``` {table} Configuration (hub-config/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Configuration directory | `hub-config/` | Folder storing configuration files | X |  |
| Admin configuration file | `hub-config/admin.json` | Structured text file containing overall configuration settings for the hub | X |  | 
| Modeling tasks configuration file | `hub-config/tasks.json` | Structured text file that defines modeling tasks and therefore implicity defines the assumed structure for any model submitted | X |  | 
| Model metadata configuration file | `hub-config/model-metadata-schema.json` | Structured text file that defines the expected format of model metadata files submitted by modeling teams | X |  |  
```

``` {table} Model Output Submissions (model-output/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Model output directory | `model-output/` | Folder to collect modeling team model submissions | X |  | 
| Model output subdirectory | `model-output/team1-modela/` | Model-specific subdirectory for submissions from one modeling team |  | X | 
| Model output file | `model-output/team1-modela/<round-id1><model_id>.csv` or .parquet| Round-specific model submission file |  | X | 
```

``` {table} Model Metadata (model-metadata/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Model metadata directory | `model-metadata/` | Folder to collect modeling team model metadata submissions | X | | 
| Model metadata submission file | `model-metadata/team1-modela.yml` | Model-specific metadata submission file |  | X | 
```


## Optional Components

The following components are not required for a hub, but may be useful:

``` {table} Model Abstracts (model-abstracts/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Model abstracts directory (optional) | `model-abstracts/` | Folder to collect optional round-specific model metadata | X |  | 
| Model abstract subdirectory | `model-abstracts/team1-modela/` | Model-specific subdirectory for round-specific model metadata |  | X | 
| Model abstract submission file | `model-abstracts/team1-modela/<round-id1>.md` | Round-specific model metadata submission |  | X | 
```

``` {table} Data and Code
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ | 
| Target data directory | `target-data/` | Folder storing actual observed (i.e., target) values of an outcome (or links to external open-access sources) and information on how  model targets can be calculated from target data | X | | 
| Auxiliary data directory | `auxiliary-data/` | Folder storing any additional data related to modeling efforts | X |  | 
| Source code directory | `src/` | Folder storing code that is present in the hub repository | X |  | 
```


* Optionally, a hub may store any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. 

Although most hubs to date have been housed in GitHub repositories, the proposed structure is more general and can be adapted for use on any shared filesystem. 

