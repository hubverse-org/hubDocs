# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in a hub repository's `model-output`[^model-output] directory.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository.

[^model-output]: The directory is required, but the name is flexible. You can
  use a custom directory path by setting the `"model_output_dir"` property in the
  `admin.json` file. More details can be found in the `admin.json` schema
  definition.

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
| Modeling tasks configuration file | `hub-config/tasks.json` | Structured text file that defines modeling tasks and, therefore, implicitly defines the assumed structure for any model submitted | X |  |
| Model metadata configuration file | `hub-config/model-metadata-schema.json` | Structured text file that defines the expected format of model metadata files submitted by modeling teams | X |  |
```

``` {table} Model Output Submissions (model-output/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ |
| Model output directory | `model-output/` | Folder to collect modeling team model submissions | X |  |
| Model output subdirectory | `model-output/team1-modela/` | Model-specific subdirectory for submissions from one modeling team |  | X |
| Model output file | `model-output/team1-modela/<round-id1>-<model_id>.csv` or .parquet| Round-specific model submission file |  | X |
```

``` {table} Model Metadata (model-metadata/)
| Component | Location | Description | Hub provides | Modeler provides |
| ------ | ------ | ------ | ------ | ------ |
| Model metadata directory | `model-metadata/` | Folder to collect modeling team model metadata submissions | X | |
| Model metadata submission file | `model-metadata/team1-modela.yml` | Model-specific metadata submission file |  | X |
```


## Optional Components

The following components are not required for a hub but may be useful:

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
| Time series data | `target-data/time-series.csv` or .parquet | File with observed counts or rates partitioned for each unique combination of `task id` values | X |  | 
| Oracle output data | `target-data/oracle-output.csv` or .parquet | File containing data derived from the time series data; represents the model output that would have been generated if the target data values were known ahead of time. For parquet files, could data types in the `oracle-output` files shoudl be consistent with the schema defined in the cong file, with the `oracle-value` column having the same data type as the model output `value` column. | X |  |
| Auxiliary data directory | `auxiliary-data/` | Folder storing any additional data related to modeling efforts | X |  |
| Source code directory | `src/` | Folder storing code that is present in the hub repository | X |  |
```


* Optionally, a hub may store any files necessary to define continuous integration workflows, such as those for validating submissions or updating target data.

Although most hubs have been housed in GitHub repositories, the proposed structure is more general and can be adapted to any shared filesystem.

