# Uploading and validating config files  

You have now made all the changes necessary to start using the simple hub, but the changes to `admin.json` and `tasks.json` are only on your local computer. You want to move them to your GitHub repository.

## Uploading changes from your local computer to GitHub  

Follow GitHub directions [here](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) for adding files to a repository.  

Once you have uploaded those two files onto your GitHub repository, you will notice that they have been updated by looking at the last commit date, as indicated below.  

```{image} ../images/github_commits.png
:alt: Screenshot of GitHub repository page with arrows pointing at time of last commits
:class: bordered
```

## Validating your config files  

Now you should validate the config files, to be sure they are properly functional. You can use the `validate_config` function from [`hubUtils`](https://infectious-disease-modeling-hubs.github.io/hubUtils/index.html) to check whether Hub config files are valid. The steps are as follows:  

1. First, you need to install the package `hubUtils`. [Here are instructions for installing `hubUtils` in the R console](https://github.com/Infectious-Disease-Modeling-Hubs/hubUtils#installation).  
2. Next, you need to validate the config files. [Here are detailed instructions and explanations](https://infectious-disease-modeling-hubs.github.io/hubUtils/articles/hub-setup.html#validate-config-files), and following is sample code you can copy to validate the config files:  
```
library(hubUtils)

validate_config(
    hub_path = ".",
    config = c("tasks", "admin"), 
    config_path = NULL, 
    schema_version = "from_config", 
    branch = "main"
)
```

Below is an example using the simple hub. You can see that the config files were successfully validated.  

```{image} ../images/validate_simple-hub-config.png
:alt: Screenshot of code showing validation of config files
:class: bordered
```

## Congratulations!  

Your simple hub repository is now ready to be used! You created a simple hub and modified the `config.json` and `task.json` files. You now have:  
- [x] Created a hub repository
- [x] Cloned the hub repository to your local computer
- [x] Configured the modeling hub by: 
  - [x] Modifying `admin.json`
  - [x] Modifying `tasks.json`
- [x] Uploaded modified files from your local computer to GitHub
- [x] Validated config files

```{image} ../images/simple-hub_directory.png
:alt: Screenshot showing directory of simple files on local computer and GitHub
```

Next, it is time to start using your modeling hub.  

