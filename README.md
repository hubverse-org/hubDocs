# Documentation for Infectious Disease Modeling Hubs

This GitHub repository includes the content needed to generate the static site 
that contains the documentation about how to build, manage and maintain 
collaborative modeling hubs.

## How the site works

This site uses [ReadTheDocs](https://readthedocs.org/) and
[Sphinx](https://www.sphinx-doc.org/en/master/index.html) for building and 
maintaining the content. The live version of the documentation can be found
[here](https://hubdocs.readthedocs.io/).

The main content of the site lives in [`docs/source`](docs/source/). That is 
where you will add/edit Markdown files to populate the content of the site.

[This page](https://jupyterbook.org/en/stable/intro.html) provides useful documentation on how to use the Jupyter Book theme, which is the theme currently used by our documentation site.

# Installation 

To build and preview the site locally, the following steps 
(assuming you already have python installed) are adapted from the 
[ReadTheDocs site](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html):

1. Install sphinx: `pip install sphinx`.
2. We are using [MyST to enable Markdown](https://github.com/executablebooks/MyST-Parser/edit/master/docs/syntax/syntax.md), 
so you need to install myst-parser: `pip install myst-parser`.
3. Install the theme we are using: `pip install sphinx-book-theme`. Documentation on theme-specific elements can be found [here](https://sphinx-book-theme.readthedocs.io/en/stable/index.html).
4. In the `docs` folder, run `make html` to build the site locally to inspect changes.


# Using a conda environment for local development

It is preferable to work with the project in a project specific conda environment. For this you will need [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

You can check whether `conda` is installed by running `conda list`.  If `conda` is installed and working, this will display a list of installed packages and their versions.

## Create environment and install dependencies

You first need to create a python 3.9  `hubdocs` environment and install all additonal python dependencies within it.

```bash
# Create hubdocs environment containing python 3.9
conda create -n hubdocs python=3.9

# Activate hubdocs environment
conda activate hubdocs

# Install python dependencies
pip install -r docs/requirements.txt
```

## Activate environment

Any time you return to the project, you will need to activate the `hubdocs` environment.

```bash
# Activate hubdocs environment
conda activate hubdocs
```

## Deactivate environment

When finished, you can deactivate the conda environment with:

```bash
conda deactivate
```

## Build site

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


# Versioning

Documentation is [versioned by using releases](https://docs.readthedocs.io/en/stable/versions.html). Releases should track releases of Hub schema versions in [`schemas` repository](https://github.com/Infectious-Disease-Modeling-Hubs/schemas). While changes to documentation text can be commited without creating a new release and will appear in th `latest` version of the documentation, **changes to documentation related to a new schema release must be accompanied by a new release in this repository**. New releases on `hubDocs` should use the same version number as the `schemas` release but without the `v` (e.g. a `v0.0.1` `schemas` version number would be released as `0.0.1` on `hubDocs`).

Before making a new release, **ensure that URLs to schema files which power the interactive docson widget visualisation of schemas in the [`docs/source/format/hub-metadata.md` page](https://github.com/Infectious-Disease-Modeling-Hubs/hubDocs/blob/main/docs/source/format/hub-metadata.md?plain=1) are updated** to display the new versions of `admin.json` and `tasks.json` schema files.

## Contribution guidelines
In general, contributions should be made via pull requests to the `main` branch. 
Note that PRs should trigger preview builds of the site, so you should be able
to double-check that your changes look as expected.
