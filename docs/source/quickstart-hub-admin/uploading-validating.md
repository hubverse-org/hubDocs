# Uploading and validating config files  

You have now made all the changes necessary to start using the simple hub, but the changes to `admin.json` and `tasks.json` are only on your local computer. You should also apply them to your GitHub repository.

## Uploading changes from your local computer to GitHub  

Follow [GitHub directions](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) to add files to a repository.  

Once you have uploaded those two files onto your GitHub repository, you will notice that they have been updated by looking at the last commit date, as indicated below.  

```{image} ../images/github-commits.png
:alt: Screenshot of GitHub repository page with arrows pointing at the time of last commits
:class: bordered
```

## Validating your config files  

Now, you should validate the config files to be sure they are properly functional. You can use the `validate_config` function from [`hubAdmin`](https://hubverse-org.github.io/hubAdmin/index.html) to check whether Hub config files are valid. The steps are as follows:  

1. First, you must [follow the instructions to install the R package `hubAdmin` in the R console](https://github.com/hubverse-org/hubAdmin#installation).  
2. Next, you need to validate the Hub's config files. 
- [`validate_hub_config()`](https://hubverse-org.github.io/hubAdmin/reference/validate_hub_config.html) validates the `admin.json`, `tasks.json`, `model-metadata-schema.json` hub config files in a single call.
- If you get any errors, you can pass the result of the above functions to `view_config_val_errors()`, which prints a concise and informative version of the validation errors table.
- Click on the link for more [detailed instructions and explanations](https://hubverse-org.github.io/hubAdmin/articles/hub-setup.html#validate-config-files).

## Congratulations!  

Your simple hub repository is now ready to be used! You created a simple hub and modified the `config.json` and `task.json` files. You now have:  
- [x] Created a hub repository
- [x] Cloned the hub repository to your local computer
- [x] Configured the modeling hub by: 
  - [x] Modifying `admin.json`
  - [x] Modifying `tasks.json`
- [x] Uploaded modified files from your local computer to GitHub
- [x] Validated config files

```{image} ../images/simple-hub-directory.png
:alt: Screenshot showing a directory of simple files on a local computer and GitHub
```

Next, it is time to start using your modeling hub.  
