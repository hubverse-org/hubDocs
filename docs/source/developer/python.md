# Python Development and Releases

This document describes Python-specific details about the Hubverse's
development and release process.

- [Checklists](#python-checklists)
    - [Development checklist](#development-checklist)
    - [Release checklist](#release-checklist)
    - [Hotfix checklist](#hotfix-checklist)
- [Releasing Python packages](#releasing-python-packages)
    - [Overview](#releasing-python-pkg-overview)
    - [TestPYPI setup](#testpypi-setup)
    - [PyPI setup](#pypi-setup)
    - [Add package maintainers](#add-package-maintainers)

Hubverse Python packages that will be released to PyPI must go through a
one-time setup process as described in the
[Creating PyPI and TestPyPI workflows](#releasing-python-packages)
section below.

Once that setup is complete, use the checklists below for updating and releasing
the package.

(python-checklists)=
## Checklists

(development-checklist)=
### Development checklist

To update a Hubverse Python package:

- [ ] Create a branch from `main` in the format of
`<initials>/<feature>/<issue>` (_e.g._, `kj/add-bucket-versioning/111` )
- [ ] Solve the issue, update/add test if necessary, commit, push
- [ ] Open a pull request (PR).
  - [ ] Pull requests should be as small as possible and should focus on
    independent features.
  - [ ] Each PR should include a corresponding update to the `[unreleased]`
    section at the top of `CHANGELOG.md` (if applicable). Changelog
    contents and style should follow the guidelines outlined in
    [keepachangelog.com](https://keepachangelog.com/).
  - [ ] In the PR description, include a link to the issue (_e.g._,
    `resolves #111`) as well as any context that will help code reviewers.
- [ ] If the PR introduces a breaking change, these changes should be tested
  and communicated with the community.
- [ ] Once the PR has been approved and all checks have passed, merge it.

:::{tip}
Review often brings up potential non-blocking features/bug fixes that are orthogonal to the original PR. In these cases, instead of creating a PR to merge into the original PR, it’s best to create a new issue from the PR review and, after merging, create a new PR to fix that issue. This helps keep disparate bugfixes and features separate.
:::

(release-checklist)=
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

(hotfix-checklist)=
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

(releasing-python-pkg-overview)=
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

(testpypi-setup)=
### TestPYPI setup

Once you complete the GitHub and TestPYPI setup as outlined below, the new
Hubverse package will be pushed to TestPyPI automatically. You will only need
to do this once.

Publishing to TestPyPI doesn't release the software. Instead, it's a way to test
the end-to-end publication process each time a new update is merged to the
package's `main` branch.

#### GitHub

1. In the package's GitHub repo,
[create an environment](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment) called `pypi-test` to use for the
TestPyPI deployment.

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

(pypi-setup)=
### PyPI setup

Once you complete the GitHub and PyPI setup as outlined below, your package will
be published to PyPI whenever a new release tag is pushed to the package's
repository.

You will only need to do this once.

#### GitHub

1. In the package's GitHub repo,
[create an environment](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment) called `pypi` to use for the
PyPI deployment.

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

(add-package-maintainers)=
### Add package maintainers

To ensure continuity, it's important that Hubverse packages on both PyPI and
TestPYPI have multiple maintainers and collaborators. You can add other Hubverse
devs to these roles from the project's _Collaborators_ page on PyPI/TestPyPI.

