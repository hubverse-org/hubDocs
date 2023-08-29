# Hub model tasks configuration  

Every Hub is organized around "modeling tasks" that are defined to meet the needs of a project. Modeling tasks are defined for a hub in the [`tasks.json`](../user-guide/hub-config.md#model-tasks-tasks-json-interactive-schema) file, which specifies the model tasks (task ids and targets) as well as model output types. A detailed definition of modeling tasks can be found [here](../user-guide/tasks.md).  

## Step 1: Open `tasks.json`  

Check to be sure you are in  the `hub-config` folder. Click on `tasks.json` to open the file.  

![Screenshot of how to open tasks.json file in RStudio](../images/tasks_json.png)  

## Step 2: Examine the `tasks.json` file  

In your source panel (upper left hand panel), you should see the code below. A description of each line of code in `tasks.json` can be found [here](../user-guide/hub-config.md#model-tasks-tasks-json-interactive-schema).  

![Screenshot of how to open tasks.json file in RStudio](../images/tasks_schema_0.png)  

This `tasks.json` file serves as a template, and has very few values filled out, which gives the user flexibility to adapt the Hub to their own needs. Nevertheless, in order to learn how to properly use this schema, we will use a "premade" `tasks.json` file from the [Simple Forecast Hub Example](https://github.com/Infectious-Disease-Modeling-Hubs/example-simple-forecast-hub) that already has values filled in, which will better illustrate what should go in each section.  

## Step 3: Close the `tasks.json` file in RStudio  

Make sure the `tasks.json` file in RStudio is closed, by clicking on the 'x' icon, as indicated below.  

![Screenshot of how to close tasks.json file in RStudio](../images/tasks_close.png)  

## Step 4: Download a premade `tasks.json` file  

Download [the `tasks.json` file from the Simple Forecast Hub Example](https://github.com/Infectious-Disease-Modeling-Hubs/example-simple-forecast-hub/blob/main/hub-config/tasks.json) by clicking on the *Download Raw File* icon as indicated below.  

![Screenshot of how to download a tasks.json file from GitHub](../images/tasks_download.png)  

Save the file in the `hub-cofig` folder (which is [in your repository on your local computer](getting-started.md#step-4-clone-your-repository)). This new file should replace the existing `tasks.json` file that was in this folder.  

## Step 5: Examine the new `tasks.json` file  

Open `tasks.json` and read the explanations below on what these lines of code stand for:  
- This is a <mark style="background-color: #FFFF00">highlighted test</mark>  

![Some of the initial lines of code in the tasks.json file](../images/tasks_schema_1.png)  
