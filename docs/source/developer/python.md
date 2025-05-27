# Python Development and Releases

This document describes Python-specific details about the Hubverse's
development and release process.

```{contents} Table of Contents
:depth: 3
```

Hubverse Python packages that will be released to PyPI must go through a
one-time setup process as described in the
[Creating PyPI and TestPyPI workflows](releasing-python-packages)
section below.

Once that setup is complete, use the checklists below for updating and releasing
the package.

## Checklists

### Development checklist

To update a Hubverse Python package:

- [ ] If you're not a member of the core Hubverse development team, fork the
      package's repository to your GitHub account.
- [ ] Create a branch from `main` in the format of
`<initials>/<feature>/<issue>` (_e.g._, `kj/add-bucket-versioning/111` )
- [ ] Make and test your changes, including any related tests.
- [ ] Open a pull request (PR).
  - [ ] Pull requests should be as small as possible and should focus on
        independent features.
  - [ ] Each PR should include a corresponding update to the `[unreleased]`
        section at the top of `CHANGELOG.md` (if applicable).
  - [ ] In the PR description, include a link to the issue (_e.g._,
        `resolves #111`) as well as any context that will help code reviewers.
- [ ] If the PR introduces a breaking change, these changes should be tested
      and communicated with the community.
- [ ] Once the PR has been approved and all checks have passed, merge it.

:::{tip}
Review often brings up potential non-blocking features/bug fixes that are
orthogonal to the original PR. In these cases, instead of creating a PR to
merge into the original PR, it’s best to create a new issue from the PR review
and, after merging, create a new PR to fix that issue.
This helps keep disparate bugfixes and features separate.
:::

### Release checklist

When it's time to release the package to PyPI:

- [ ] Proofread `CHANGELOG.md` and change the `[unreleased]` heading at the top
to the new release's version number. Make sure to acknowledge any contributors
outside of the core dev team by linking to their GitHub handles.
- [ ] Submit a PR, get a review, and merge the `CHANGELOG.md` updates.
- [ ] Create a new tag for the release as described in the
[Hubverse Release Process](#hubverse-release-process-releases).
- [ ] If you created the release tag locally, push it to the package's
repository (for example, `git push v0.2.4`).

### Hotfix checklist

A hotfix is a bug fix that is independent from in-development features and
needs to be deployed within a day. Details on hotfixes can be found on the
[hotfix page](hotfix.md).

To patch and release a hotfix:

- [ ] Create a new branch from the latest tag using pattern
`<initials>/hotfix/<issue>`

    ```sh
    (main)$ git switch --detach 0.14.0 # checkout the tag
    ((0.14.0))$ git switch -c znk/hotfix/143 # create a new branch
    (znk/hotfix/143)$
    ```

- [ ] Write a test, fix the bug, and update `CHANGELOG.md` with the
[patch version](#patch) and description. Push these changes
upstream:

    ```sh
    (znk/hotfix/143)$ git commit -m 'hotfix for #143'
    (znk/hotfix/143)$ git push -u origin znk/hotfix/143 # push the hotfix
    ```

- [ ] Create a PR, get a review, and confirm that tests pass against the
released version of the package.
- [ ] From the hotfix branch, create a tag for the release.
- [ ] Resolve conflicts in the PR and merge into main.

## Creating a new Hubverse Python package

Unlike R, the Python ecosystem doesn't have a single, agreed-upon
best practice for package creation, structure, and development. In general,
Hubverse Python packages:

- Use [uv](https://docs.astral.sh/uv/) for managing Python versions,
  virtual environments, and dependencies
- Use a [`pyproject.toml` file](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
  to describe the project (versus the older `setup.py`)
- Use the src layout (the
  [pyOpenSci website](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html#what-is-the-python-package-source-layout)
  has a good overview of this layout)
- Type hint function arguments and return values (at a minimum—other code may
  have type hints for clarity)
- Use [numpy-style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)
- Use [ruff](https://github.com/astral-sh/ruff) for linting and code formatting
  (generally with the default settings)
- Use [pytest](https://docs.pytest.org/en/stable/) for creating and running tests
- Use [Sphinx](https://www.sphinx-doc.org/en/master/) for documentation
  (the page you're reading now was created with Sphinx)
- Prefer logging to stdout over print statements

### Creating a new Python package (empty)

The[`uv init`](https://docs.astral.sh/uv/reference/cli/#uv-init) command can
create an new, empty Python package structure using the `src` layout. The
following command creates a directory called `new-package`
in the current working directory:

```bash
uv init --package new-package
```

The resulting directory structure looks like this:

```bash
new-package
├── README.md
├── pyproject.toml
└── src
    └── new_package
        └── __init__.py
```

### Creating a new Python package (with logging setup, test harness, CI, and docs)

The [pyprefab package](https://bsweger.github.io/pyprefab/index.html)
is a simple, prompt-driven tool for creating new Python
packages that has boilerplate code for logging, testing, GitHub actions,
Sphinx documentation, and a Python-based `CONTRIBUTING.md` file.

You don't need to install pyprefab to use it. The
[tools feature of uv](https://docs.astral.sh/uv/guides/tools/) can invoke
pyprefab directly:

```bash
uvx pyprefab
```

This command will then prompt for a package name, author name, and a few other
pieces of information. The resulting package will have the following structure:

```bash
new-package
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── docs
│   └── source
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       ├── _static
│       │   └── custom.css
│       ├── conf.py
│       ├── index.rst
│       ├── readme.md
│       └── usage.md
├── pyproject.toml
├── src
│   └── new_package
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       └── logging.py
└── test
    └── test_app.py
```

(releasing-python-packages)=
## Releasing Python packages

Unlike CRAN, Python's official package index, [PyPI](https://pypi.org/), does
not require manual review. Thus, the Hubverse can release Python packages
right to PyPI without an intermediary like R-Universe. In addition,
[TestPyPI](https://test.pypi.org/) allows us to test release processes and
tools without publishing to the real index.

The documentation below assumes that Hubverse PyPI packages will be released
to PyPI, allowing us to follow the "main = stable dev branch" release process
as outlined in the [Hubverse release process](release-process.md).

### Overview

PyPI (and TestPyPI) allow
[_trusted publishers_](https://docs.pypi.org/trusted-publishers/) as way to
publish packages via GitHub actions without embedding secrets in the project
repository.

Any Hubverse Python packages published to PyPI will use trusted publishing,
which protects against supply chain attacks and credential leaks.

- merges to the stable dev branch (`main`) will be released on TestPyPI as an end-to-end test
- adding a release tag to the repo (_i.e._, vX.Y.Z) will trigger a release to PyPI

This article contains a clearly-written deep dive into
[how trusted publishing works and the advantages of using it](https://blog.trailofbits.com/2023/05/23/trusted-publishing-a-new-benchmark-for-packaging-security/).

### TestPYPI setup

Once you complete the GitHub and TestPYPI setup as outlined below, the new
Hubverse package will be pushed to TestPyPI automatically. You will only need
to do this once.

Publishing to TestPyPI doesn't release the software. Instead, it's a way to test
the end-to-end publication process each time a new update is merged to the
package's `main` branch.

#### GitHub

1. In the package's GitHub repo,
   [create an environment](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
   called `pypi-test` to use for the TestPyPI deployment.

    :::{note}
    Because this environment is for test deployments, you don't need to add
    protection rules or fill out any other information when configuring it.
    :::

2. Add the `publish-pypy-test.yaml` workflow the package's Github repo:
    - Copy the [`publish-pypi-test.yaml` workflow from hubverse-developer-actions](https://github.com/hubverse-org/hubverse-developer-actions/tree/main/publish-pypi-test/publish-pypi-test.yaml).
    - Change `<package>` in the TestPyPI url to the name of your package
    (_e.g._, `https://test.pypi.org/p/hubDataPy`)

#### TestPyPI

1. [Create a TestPyPI account](https://test.pypi.org/account/register/) if you
don't already have one.
2. Log in to TestPyPI.
3. [Create a new Trusted Publisher](https://test.pypi.org/manage/account/publishing/)
for the Hubverse package.
    - PyPI Project Name: name in the `[project]` section of the package's
    `pyproject.toml` file
    - Owner: GitHub organization name (`hubverse-io`)
    - Repository name: the package's GitHub repository name
    - Workflow name: full file name of the GitHub workflow that publishes to
    TestPyPI (_e.g._ `publish-pypi-test.yaml`)
    - Environment name: name of the GitHub environment created above
    (`pypi-test`)

### PyPI setup

Once you complete the GitHub and PyPI setup as outlined below, your package will
be published to PyPI whenever a new release tag is pushed to the package's
repository.

You will only need to do this once.

#### GitHub

1. In the package's GitHub repo,
   [create an environment](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
   called `pypi` to use for the PyPI deployment.

    :::{important}
    Because this environment will be used for publishing to production,
    check the `Required reviewers` option and add a list of Hubverse devs who
    are authorized to approve releases.
    :::

2. Add the `publish-pypy.yaml` workflow the package's Github repo:
    - Copy the [`publish-pypi` workflow from hubverse-developer-actions](https://github.com/hubverse-org/hubverse-developer-actions/tree/main/publish-pypi/publish-pypi.yaml).
    - Change `<package>` in the PyPI url to the name of your package
    (_e.g._, `https://pypi.org/p/hubDataPy`)

#### PyPI

1. [Create a PyPI account](https://pypi.org/account/register/) if you
don't already have one.
2. Log in to PyPI.
3. [Create a new Trusted Publisher](https://pypi.org/manage/account/publishing/)
for the Hubverse package:
    - PyPI Project Name: name in the `[project]` section of the package's
    `pyproject.toml` file
    - Owner: GitHub organization name (`hubverse-io`)
    - Repository name: the package's GitHub repository name
    - Workflow name: full file name of the GitHub workflow that publishes to
    PyPI (_e.g._ `publish-pypi.yaml`)
    - Environment name: name of the GitHub environment created above
    (`pypi`)

### Add package maintainers

To ensure continuity, it's important that Hubverse packages on both PyPI and
TestPYPI have multiple maintainers and collaborators. You can add other Hubverse
devs to these roles from the project's _Collaborators_ page on PyPI/TestPyPI.
