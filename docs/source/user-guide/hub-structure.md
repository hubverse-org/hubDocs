# Structure of hub repositories

A hub repository should be structured according to the following guidelines:

1. Code and scripts must not be present in a hub repository's `model-output`[^model-output] directory.
2. If code is included in the hub repository, it should live in a centrally located directory, which we recommend naming `src`.
3. If code has the potential to disrupt or break other continuous integration operations in the hub (e.g., validation of incoming submissions),
it should be moved to another repository.
4. Large target data files may be partitioned, but they should be stored in parquet format in the `target-data` directory and follow Apache Hive naming conventions (see Data and Code section below). 

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
| Oracle output data | `target-data/oracle-output.csv` or .parquet | File containing data derived from the time series data; represents the model output that would have been generated if the target data values were known ahead of time. For parquet files, column data types in the `oracle-output` file(s) should be consistent with the schema defined in the config file, with the `oracle-value` column having the same data type as the model output `value` column. | X |  |
| Auxiliary data directory | `auxiliary-data/` | Folder storing any additional data related to modeling efforts | X |  |
| Source code directory | `src/` | Folder storing code that is present in the hub repository, including code to access target time series data and/or oracle output programmatically | X |  |
```
* Partitioned target data files should be stored in the `target-data` directory, in either a 'target-data/times-series` or 'target-data/oracle-output` subdirectory.  
* Partitioned target data should follow Apache Hive naming conventions. In Apache Hive, the file name format of partitioned data depends on the partition column names and their values. The files corresponding to each partition are stored in subdirectories, and the directory names encode the partition column names and their values, e.g. <partition_column_1>=<value_1>/<partition_column_2>=<value_2>/.../<data_files>. This means Hive-style partitioned data subdirectories are self describing and can be easily read by partition-aware data readers.

* Here's an example of oracle output data in the `target-data/oracle-output` directory partitioned by target_end_date:

```{code block} json
├── target_end_date=2023-06-03
│   └── part-0.parquet
├── target_end_date=2023-06-10
│   └── part-0.parquet
└── target_end_date=2023-06-17
    └── part-0.parquet
```

* Hubs can use their own file naming convention or retain the file names that are generated by the library they use for partitioning. Since Hive-partitioned datasets are not expected to store data in the file names themselves, tooling to read them ignores file names altogether. 

## Additional notes

* Optionally, a hub may store any files necessary to define continuous integration workflows, such as those for validating submissions or updating target data.

* Although most hubs have been housed in GitHub repositories, the proposed structure is general enough to be adapted to any shared filesystem.

