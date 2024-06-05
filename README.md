# Documentation for Infectious Disease Modeling Hubs  

This GitHub repository includes the content needed to generate the static site that contains the documentation about how to build, manage and maintain collaborative modeling hubs.

## Sections  
1. [How the site works](#how-the-site-works)  
2. [Installation and building](#installation-and-building)  
3. [View local site](#view-local-site)  
4. [Documentation versioning](#documentation-versioning)  
6. [Contribution guidelines](#contribution-guidelines)  
7. [Style notes](#style-notes)  

## How the site works  

This site uses [ReadTheDocs](https://readthedocs.org/) and [Sphinx](https://www.sphinx-doc.org/en/master/index.html) for building and  maintaining the content. The [live version of the documentation can be found in this page](https://hubverse.io/en/latest/).

The main content of the site lives in [`docs/source`](docs/source/). That is 
where you will add/edit Markdown files to populate the content of the site.

[This page](https://jupyterbook.org/en/stable/intro.html) provides useful documentation on how to use the Jupyter Book theme, which is the theme currently used by our documentation site.  

## Installation and building  

To build and preview the site locally, the following steps 
(assuming you already have python installed) are adapted from the 
[ReadTheDocs site](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html):

1. Install sphinx: `pip install sphinx`.
2. We are using [MyST to enable Markdown](https://github.com/executablebooks/MyST-Parser/edit/master/docs/syntax/syntax.md), 
so you need to install myst-parser: `pip install myst-parser`.
3. Install the theme we are using: `pip install sphinx-book-theme`. Documentation on theme-specific elements can be found [here](https://sphinx-book-theme.readthedocs.io/en/stable/index.html).
4. In the `docs` folder, run `make html` to build the site locally to inspect changes.


### Using a conda environment for local development

It is preferable to work with the project in a project specific conda environment. For this you will need [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

You can check whether `conda` is installed by running `conda list`.  If `conda` is installed and working, this will display a list of installed packages and their versions.

### Create environment and install dependencies

You first need to create a python 3.9  `hubdocs` environment and install all additonal python dependencies within it.

```bash
# Create hubdocs environment containing python 3.9
conda create -n hubdocs python=3.9

# Activate hubdocs environment
conda activate hubdocs

# Install python dependencies
pip install -r docs/requirements.txt
```

### Activate environment

Any time you return to the project, you will need to activate the `hubdocs` environment.

```bash
# Activate hubdocs environment
conda activate hubdocs
```

### Deactivate environment

When finished, you can deactivate the conda environment with:

```bash
conda deactivate
```

### Build site

To build html pages from source, navigate to the `docs/` directory and run `make html`. 
The resulting HTML pages can be found in the `docs/build/` directory.

```bash
cd docs
make html
```

## View local site  

To view the site locally, open any of the html files the `docs/build/` directory in a browser (by right clicking and selecting the application to open the file with.)

### Using Live Server in VSCode

If you are using VSCode, you can use the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension to run a live version of the site which will update in real time as you make changes.

To use Live Server:
1. Make sure the extension is installed on your system. Install it from [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
2. Once installed, a **Go Live** button will appear at the bottom of left of the VSCode toolbar when viewing any html file. ![](https://user-images.githubusercontent.com/5583057/203735663-f6b1954d-db0a-444b-8d75-643d04a98946.png) Clicking on it launches a live server on the open html file page.
3. When the Live Server is running, you will see the port it it is being served on at the bottom of left of the VSCode toolbar. ![](https://user-images.githubusercontent.com/5583057/203736634-5a3a398d-7067-4962-a457-f7db35e2244c.png) 
4. To disconnect the server, click on :no_entry_sign:.

## Documentation versioning  

Documentation is [versioned by using releases](https://docs.readthedocs.io/en/stable/versions.html). Releases should track releases of Hub schema versions in [`schemas` repository](https://github.com/Infectious-Disease-Modeling-Hubs/schemas). While changes to documentation text can be commited without creating a new release and will appear in the `latest` version of the documentation, **changes to documentation related to a new schema release must be accompanied by a new release in this repository**. New releases on `hubDocs` should use the same version number as the `schemas` release but without the `v` (e.g. a `v0.0.1` `schemas` version number would be released as `0.0.1` on `hubDocs`).

When creating a new release version:

1. Checkout the main branch and ensure you pull all changes from the remote repository.
2. Create a new branch of the main branch and name it using the convention `br-<version-number>`
3. Open `docs/source/conf.py` file and update the value of the `schema_version` variable with the version of the schema in the `schemas` repository you want the release to accompany (e.g. `v0.0.1`). This propagates the appropriate version to various substitution text elements within the docs, including the URLs pointing docson widgets to raw config schema files.
4. If the version of the schema you are preparing the release for has not been released to `main` branch in the `schemas` repository, you can set the value of the `schema_branch` variable to the name of the branch in the `schemas` repository in which the version is being prepared (e.g. `br-v1.0.0`). This allows you to see what development versions of the schema will look like in the docson widgets while developing locally and in a pull request. If the schema has been released to `main` in the `schemas` repo, set `schema_branch` to `"main"`. The value of this variable is overriden automatically when READTHEDOCS builds the documentation on the `main` branch (or any other branch for that matter, in contrast to a pull request build) after a merge or a new release.
5. Any any changes to the documentation needed.
6. Commit and push changes (including changes to `conf.py`)
7. Create pull request and merge after review.
8. [Create a release on GitHub](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository?tool=webui#creating-a-release) labelling it with the same version number as the `schemas` release this release is associated with but without the `v` (e.g. a `v0.0.1` `schemas` version number would be released as `0.0.1` on `hubDocs`).

## Contribution guidelines  
In general, contributions should be made via pull requests to the `main` branch. Note that PRs should trigger preview builds of the site, so you should be able to double-check that your changes look as expected.

## Style notes  
- New pages have to be added to an existing or new subfolder and indexed within the table of contents in `docs/source/index.md` (e.g., `user-guide/sample-output-type.md`).  
- File names and directories should be in lower case, and hyphens should be used in place of spaces (not underscores) for consistency, to make searches easier, and to help with accessibility. [Additional explanations and suggestions can be found in this page](https://developers.google.com/style/filenames).  
- Formatting of pages should try to use (1) native Markdown formatting first, (2) HTML formatting when Markdown formatting is insufficient or inadequate, (3) customization of HTML through CSS using `custom.css` (`docs/_static/css/custom.css`).
- Images used in Markdown pages should be stored in `docs/source/images` or in some instances under `docs/_static`.  
- Files that are not Markdown files (e.g., html files, json files, pdf files) should be stored in `docs/source/files` or in some instances under `docs/_static`.  
- Additional stylistic suggestions can be found in [this style guide for Sphinx-based documentations](https://documentation-style-guide-sphinx.readthedocs.io/en/latest/).  
