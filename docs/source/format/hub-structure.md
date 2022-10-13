# Structure of Hub repositories

## Recommended standards

A Hub should contain the following items. Links are to sections of this document that provide more detail.

* Documentation files:
   1. Hubs should provide a documentation file (e.g., README.md) at the top level that describes the overall structure of the hub, as well as a documentation file within each folder that provides more detail
* hub-metadata directory
   1. hub-meta.json - Json or yaml[i][j] file defining Hub modeling targets
   2. hub-tasks.json - Json or yaml file defining information about model submission validation
   3. model-metadata-schema.json - Json or yaml file defining format of model metadata files
* model-output directory: e.g., Forecast data or scenario projections produced by participating models/teams
   1. team1-modela
      * <round-id1>.csv[k] (or parquet, etc)
      * <round-id2>.csv (or parquet, etc)
   2. team1-modelb
      * <round-id1>.csv (or parquet, etc)
   3. team2-modela
      * <round-id1>.csv (or parquet, etc)
* model-metadata directory: Metadata describing the modeling approach and contributors generally
   1. team1-modela.yml
   2. team1-modelb.yml
   3. team2-modela.yml
* model-abstracts directory: Round-specific metadata – If applicable to the hub, round-specific updates to the metadata, e.g. describing modeling assumptions specific to one modeling round. Note: as part of a separate workflow, hubs may find it helpful to associate round-specific metadata with the corresponding model output files.
   1. team1-modela
      * <round-id1>.md
      * <round-id2>.md
   2. team1-modelb
      * <round-id1>.md
   3. team2-modela
      * <round-id1>.md
* target-data directory (if applicable[l][m])
   1. Many Hubs will focus on modeling tasks where the goal is to estimate or predict a quantity that is in principle observable. In those cases, the Hub should provide:
      * Ground truth data for the variables that are used to define modeling targets, either within the hub itself or with a pointer to an external source providing the data. Critically, this truth data source should be openly accessible and should provide access to historical versions of the data that were available as of past dates.
      * A precise specification of how all modeling targets can be calculated from the ground truth data, ideally with functions implementing those calculations in multiple commonly used programming languages
* (auxiliary-data)?
   1. Other data sources that models might want to use as inputs
   2. outliers
   3. locations
* Optionally, any files necessary to define continuous integration workflows, for example for the purpose of validating submissions or updating target data. To the extent possible, only the workflow definition files should be stored within the Hub repository, with any additional scripts or functionality residing in an external repository.


The Hub repository is intended primarily as a storage space for primary data. All other code and outputs related to model output validation, visualizations, reports, ensemble construction, etc., should be placed in repositories other than the primary Hub repository.

## Current practices
* US COVID-19 Forecast Hub
   1. I think that documentation doesn’t exist in a single place
   2. Data and related code is organized into the following repositories:
      * Forecast hub itself contains:
         * Forecast data in `data-processed`
         * Truth data in `data-truth`
         * Json file described below defining forecast targets (described more below)
         * Definitions of github action workflows for:
            * Validating submissions
            * Uploading forecasts to Zoltar
            * Updating truth data
         * Code for creating reports in code/reports/…
         * Code related to uploading submissions to Zoltar
         * A bunch of other legacy code that is not used anymore
      * Validations repository implements the logic for validations
      * Viz repository has the viz dashboard
         * A nuxt module implementing the viz as a (somewhat) reusable nuxt component is in a separate repo here
         * We are working on refactoring this so that it is written in plain javascript and can be used as a component in sites built using other web frameworks
      * covidEnsembles repository has code for building ensembles.  We have a goal to clean this up and put it elsewhere. A rough start on that was made in hubEnsembles
* US Influenza Forecast Hub
   1. Basically the same as US COVID-19 Forecast Hub, but forecasts are saved in a folder called data-forecasts instead of data-processed
* US Scenario Modeling Hub:
   1. I don’t think that documentation exists either.
   2. We use multiple packages (some internal) for the whole processing. The SMH repo is only used for Submission and storage.
      * We are also currently updating the whole process as we are adding FLU SMH and will be adding new repositories and updating others.
* EU Hubs:
   1. Example
   2. Contains (mostly) forecasts & code for reports
   3. We’ve tried to outsource code to packages as much as possible
   4. Ideally, the main repo would contain only submissions. It’s not uncommon to adopt this kind of structure in projects that contain a lot of contributed data (e.g., zotero translators repo).
      * Benefits:
         * Fewer mistakes where contributors upload their submission in the wrong folder
         * Easier for external researchers to access hub data
      * Downsides:
         * at the moment, it’s clunky to have to fetch data from another repo (either through cloning or the GitHub API) in downstream analyses.

