# Scripting Task Configuration  

The [`hubAdmin` package](https://hubverse-org.github.io/hubAdmin/index.html) provides tools to help with the configuration of [tasks](../user-guide/tasks.md) that are run on the hub. Specifically, the package has various [`create` functions](https://hubverse-org.github.io/hubAdmin/reference/index.html) that can be used to create objects that are used to build a [`"tasks"` config file](https://hubverse-org.github.io/hubAdmin/reference/create_config.html) that can ultimately be written as a [`tasks.json`](#model-tasks-schema) file.  

As was mentioned previously, the `tasks.json` file specifies the three components of modeling tasks ([task ID variables](#task-id-vars), [output types](#output-types), and [target metadata](#target-metadata)) that are used in the hub. The `hubAdmin` package provides functions to help with the creation of these objects.  

In this section, we will walk through the process of scripting task configuration using functions from the `hubAdmin` package, in an order similar to that used in the [previous "Configuring tasks" section](#tasks-json-edits).  

### Step 1: Create an `src` folder  

Open RStudio and make sure you are in the main folder of your repo. Create a new folder called `src` by clicking on the "New Folder" icon.  

```{image} ../images/src-folder.png
:alt: Screenshot for creating a new folder in RStudio called "src"
:class: bordered
```


 
 


Steps:
- Install the `hubAdmin` package
- Create src folder
- Create a new R script
- Load the `hubAdmin` package
- Follow steps here: https://hubverse-org.github.io/hubAdmin/reference/create_config.html 


