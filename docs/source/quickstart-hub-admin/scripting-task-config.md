# Scripting task configuration  

The [`hubAdmin` package](https://hubverse-org.github.io/hubAdmin/index.html) provides tools to help with the [configuration of tasks](../user-guide/tasks.md) that are run on the hub. Specifically, the package has various [`create` functions](https://hubverse-org.github.io/hubAdmin/reference/index.html) that can be used to create objects that are used to build a [`"tasks"` config file](https://hubverse-org.github.io/hubAdmin/reference/create_config.html) that can ultimately be written as a [`tasks.json` file](#model-tasks-schema).  

As mentioned previously, the `tasks.json` file specifies the three components of modeling tasks ([task ID variables](#task-id-vars), [output types](#output-types), and [target metadata](#target-metadata)) used in the hub. The `hubAdmin` package provides functions to help create these objects.  

In this section, we will walk through the process of scripting task configuration using functions from the `hubAdmin` package in an order similar to that used in the [previous configuring tasks section](#tasks-json-edits).  

## Step 1: Create an `src` folder  

Open RStudio and ensure you are in your repo's main folder. Click on the "New Folder" icon to create a new folder called `src`.  

```{image} ../images/src-folder.png
:alt: Screenshot for creating a new folder in RStudio called "src", as described in the text.
:class: bordered
```

## Step 2: Create a new R script within the `src` folder  

In the files pane, click on the `src` folder and ensure you are inside the folder by checking the path at the top of the pane. The path (circled below in green) should now show the `src` folder. Click on the "New Blank File" icon and select "R Script". Name the file "scripting-task-config".  

```{image} ../images/new-scripting-task-config.png
:alt: Screenshot for creating a new R Script called "scripting-task-config" in the "src" folder, as described in the text.
:class: bordered
```
 
## Step 3: Install the `hubAdmin` package  

In the Console of RSudio, install the [latest version of the `hubAdmin` package from the R-universe](https://hubverse-org.r-universe.dev/hubAdmin) by running the following command:  

``` r
install.packages("hubAdmin", repos = c("https://hubverse-org.r-universe.dev", "https://cloud.r-project.org"))
```

```{image} ../images/install-hubAdmin.png
:alt: Screenshot showing command for installing hubAdmin package, as described in text.
:class: bordered
```

## Step 4: Write the script to create and configure a `"tasks"` config file  

For this step, please visit the [Scripting task configuration files vignette](https://hubverse-org.github.io/hubAdmin/dev/articles/scripting-tasks-config.html) from the `hubAdmin` package and follow the steps in the [Creation of a `tasks.json` file section](https://hubverse-org.github.io/hubAdmin/dev/articles/scripting-tasks-config.html#creation-of-a-tasks-json-file).
 
And note, while you can copy and paste the code snippets to your console, we strongly recommend to manually enter the commands in your script and run them as you go along.

## Step 5: Save and run the script  

Click on the "save" icon to save the script. Then, click on the "Source" icon to run the script.  

```{image} ../images/save-run-scripting-task-config.png
:alt: Screenshot for saving and running the `scripting-task-config` script in RStudio
:class: bordered
```

## Congratulations!  

You have successfully scripted the task configuration for your modeling hub. The `tasks.json` file has been created and saved in the `hub-config` folder. You can now move on to [configuring the model metadata](model-metadata-schema.md) for your hub.  

