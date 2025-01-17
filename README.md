# Documentation for Infectious Disease Modeling Hubs  

This repository includes the content needed to generate the Hubverse static
documentation site. Included is documentation about how to build, manage, and
maintain collaborative modeling hubs.

## Sections

1. [How the site works](#how-the-site-works)
2. [Updating Hubverse documentation](#updating-hubverse-documentation)
3. [Updating Read the Docs and Sphinx](#updating-read-the-docs-and-sphinx)
4. [Documentation versioning](#documentation-versioning)
5. [Contribution guidelines](#contribution-guidelines)
6. [Style notes](#style-notes)

## How the site works

This site uses [ReadTheDocs](https://readthedocs.org/) and
[Sphinx](https://www.sphinx-doc.org/en/master/index.html) for building and
maintaining the content. The
[live version of the documentation can be found in this page](https://hubverse.io/en/latest/).

Useful links:

- Documentation for our current theme, [Jupyter Book](https://jupyterbook.org/en/stable/intro.html)
- Getting started guide for [Read the Docs and Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)

## Local development

This project uses [`uv`](https://docs.astral.sh/uv/) to manage Python installs,
dependencies, and virtual environments. The result is less work to set up
a development environment.

However, contributors who prefer different Python tools can still use them as
long as dependency updates follow the workflow of adding (or removing)
dependencies from `pyproject.toml` and re-generating an annotated
`requirements/requirements.txt` file. In other words, don't add update
the requirements.txt file directly.

### Updating Hubverse documentation

The main content of the Hubverse documentation lives in
[`docs/source`](docs/source/). That is where you will add/edit Markdown files
to change the site's content.

To preview the site locally after making updates:

1. Install uv on your machine (you will only need to do this once):
<https://docs.astral.sh/uv/getting-started/installation/>
2. Clone this repository. The rest of the instructions should be executed from
the repo's root directory.
3. Create a virtual environment for the project:

    ```script
    uv venv --seed
    ```

4. Install dependencies:

    ```script
    uv pip install -r requirements/requirements.txt
    ```

5. Build a local copy of the documentation:

    ```script
    uv run sphinx-autobuild docs/source docs/_build/html
    ```

    The output of this command provides the url to use for viewing the
    documentation. For example:

    ```script
    build succeeded, 4 warnings.

    The HTML pages are in docs/_build/html.
    [sphinx-autobuild] Serving on http://127.0.0.1:8000
    [sphinx-autobuild] Waiting to detect changes...
    ```

### Updating Read the Docs and Sphinx

To update the Read the Docs and Sphinx pieces of hubDocs, follow steps
1-4 above to set up a development environment. Then makes updates as needed
(for example, to the Sphinx `conf.py` configuration file).

If you need to add a dependency to hubDocs (for example, to add a Sphinx
extension):

1. Add the dependency to the project config (`pyproject.toml`):

    ```script
    uv add <name of package to add>
    ```

2. Generate an updated `requirements.txt` file:

    ```script
    uv pip compile pyproject.toml -o requirements/requirements.txt
    ```

3. Install the updated requirements into your development environment:

    ```script
    uv pip install -r requirements/requirements.txt
    ```

4. Use the same command as above to build and preview a local copy of the site:

    ```script
    uv run sphinx-autobuild docs/source docs/_build/html
    ```

To remove a dependency, the process is similar. Replace the first step above
with `uv remove` and follow the remaining steps.

## Documentation versioning  

Documentation is [versioned by using releases](https://docs.readthedocs.io/en/stable/versions.html). Releases should track releases of Hub schema versions in [`schemas` repository](https://github.com/hubverse-org/schemas). While changes to documentation text can be commited without creating a new release and will appear in the `latest` version of the documentation, **changes to documentation related to a new schema release must be accompanied by a new release in this repository**. New releases on `hubDocs` should use the same version number as the `schemas` release but without the `v` (e.g. a `v0.0.1` `schemas` version number would be released as `0.0.1` on `hubDocs`).

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
