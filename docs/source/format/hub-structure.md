# Structure of Hub repositories

A Hub should be structured according to the following recommendations. Links are to sections of the documentation that provide more detail.

* Documentation files
   1. Hubs should provide a documentation file (e.g., `README.md`) at the top level that describes the overall structure of the hub, as well as a documentation file within each folder that provides more detail.

* `hub-metadata` directory (see {doc}`/format/hub-metadata`)
   1. hub-meta.json - Json or yaml file defining Hub modeling targets
   2. hub-tasks.json - Json or yaml file defining information about model submission validation
   3. model-metadata-schema.json - Json or yaml file defining format of model metadata files

* `model-output` directory (see {doc}`/format/model-outputs`) with structure as follows
   1. `team1-modela`
      * `<round-id1>.csv` (or parquet, etc)
      * `<round-id2>.csv` (or parquet, etc)
   2. `team1-modelb`
      * `<round-id1>.csv` (or parquet, etc)
   3. `team2-modela`
      * `<round-id1>.csv` (or parquet, etc)

* `model-metadata` directory (see {doc}`/format/model-metadata`)  with structure as follows
   1. `team1-modela.yml`
   2. `team1-modelb.yml`
   3. `team2-modela.yml`

* `model-abstracts` directory: Round-specific metadata – If applicable to the hub, round-specific updates to the metadata, e.g. describing modeling assumptions specific to one modeling round. Note: as part of a separate workflow, hubs may find it helpful to associate round-specific metadata with the corresponding model output files.
   1. `team1-modela`
      * `<round-id1>.md`
      * `<round-id2>.md`
   2. `team1-modelb`
      * `<round-id1>.md`
   3. `team2-modela`
      * `<round-id1>.md`

* `target-data` directory (if applicable)
   1. Many Hubs will focus on modeling tasks where the goal is to estimate or predict a quantity that is in principle observable. In those cases, the Hub should provide:
      * Ground truth data for the variables that are used to define modeling targets, either within the hub itself or with a pointer to an external source providing the data. Critically, this truth data source should be openly accessible and should provide access to historical versions of the data that were available as of past dates.
      * A precise specification of how all modeling targets can be calculated from the ground truth data, ideally with functions implementing those calculations in multiple commonly used programming languages

* `auxiliary-data` (optional)
   1. Other data sources that models might want to use as inputs
   2. outliers
   3. locations

* Optionally, any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. To the extent possible, only the workflow definition files should be stored within the Hub repository, with any additional scripts or functionality residing in an external repository.


The Hub repository is intended primarily as a storage space for primary data. All other code and outputs related to model output validation, visualizations, reports, ensemble construction, etc., should be placed in repositories other than the primary Hub repository.
