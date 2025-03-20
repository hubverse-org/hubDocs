# Hubverse Release Process

Parts of this document are adapted for The Hubverse from
[The Carpentries Developer's Handbook](https://carpentries.github.io/workbench-dev/releases.html) (c) The Carpentries under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

**Looking for a checklist?**

- [R package release checklist](r.md)
- [Python package release checklist](python.md)

## Executive Summary

The release process is now a general workflow that can help to reduce the size
of pull requests:

1. Iterate on small bug fixes and PRs on branches, merging into main as a
   stable development branch
2. When ready, bump the version, add an annotated git tag, and release
3. Bump the version in `main` back to a development version

This workflow applies to both R and Python packages, although the implementation
specifics will vary between languages.

## Background

While the release process described here applies to both R and Python, the
impetus for adopting it was making the Hubverse R packages available on the
[Hubverse R-Universe][r-universe]. R-Universe checks for new versions hourly,
which allows users to get up-to-date packages without running out of GitHub API
query attempts.

The Hubverse does not have a Python equivalent to the R-Universe. Instead,
Python packages are distributed via [PyPI](https://pypi.org/), Python's package
index.

In order to maintain quality, packages are only sent to the R-Universe or PyPi
if they have been formally released on GitHub. This allows us to add new
experimental, non-breaking features incrementally, without changing the stable
deployments.

(previous-state)=
### Previous state

Prior to updating the Hubverse release process in August 2024, **each pull
request merged to the `main` branch of a repository effectively meant the
release of a new version**. Ideally, this meant that our Git history would look
like a series of adjacent belt loops:

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh (0.14.0)"
    branch feature1
    checkout main
    checkout feature1
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge feature1 id: "gpne (0.14.1)"
    branch feature2
    checkout feature2
    commit id: "qrst"
    commit id: "uvwx"
    checkout main
    merge feature2 id: "punx (0.14.2)"
```

However, a pattern often emerges where more than one feature in a particular
release is desired and, because we release directly to `main`, the graph looks
like a thundercloud:

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh (0.14.0)"
    branch feature1
    checkout main
    checkout feature1
    commit id: "ijkl"
    commit id: "mnop"
    branch feature2
    checkout feature2
    commit id: "qrst"
    checkout feature1
    commit id: "uvwx"
    checkout feature2
    commit id: "yz12"
    checkout feature1
    merge feature2 id: "xu12"
    checkout main
    merge feature1 id: "gpxe (0.14.1)"
```

The problem with the second graph is that, as the number of extra features grows,
the size of the PR that will be the release becomes larger and larger.
Moreover, the exact changes that were needed in the original PR are mixed in
with all the changes from the child branches, meaning that it is more difficult
to retrospectively review that PR.

(new-release-process)=
### New release process

The release process adopted in August 2024 alleviates the "many features =
large PR" problem and makes it easier to multiple people to work on package
features simultaneously.

Now that we distribute packages outside of GitHub itself, builds can be pinned
to Releases on specific tags, resulting in a git graph that looks similar to
[the first graph](#previous-state), but it can also **enable developers to work in parallel**
on independent features, allowing users to intermittently test these features by
installing from the default branch in GitHub.

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "0.14.0"
    branch feature1
    branch feature2
    checkout main
    checkout feature1
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    checkout feature2
    commit id: "qrst"
    commit id: "uvwx"
    checkout main
    merge feature1 id: "gpne"
    merge feature2 id: "punx"
    branch release
    checkout release
    commit id: "2zy1"
    checkout main
    merge release id: "1u2n" tag: "0.14.1"
```

## Versioning

The hubverse is built using very basic semantic versioning using the
`X.Y.Z` pattern. Development versions are indicated as

- `X.Y.Z[.9000]` for R
- `X.Y.Z[.dev<n>]` for Python.

Here's an example for an R package. If we take
[the previous git graph](#new-release-process) and labelled the version number,
you can see how the first release in our graph was a minor release, followed by
a patch release. Everything that has [a `.9000` attached
is considered in-development](#dev). Read below for details and examples of
each of these semantic versions:

```{mermaid}
gitGraph
    commit id: "abcd (0.13.2.9000)"
    commit id: "efgh (0.14.0)" tag: "0.14.0"
    branch feature1
    branch feature2
    checkout main
    checkout feature1
    commit id: "ijkl (0.14.0.9000)"
    commit id: "mnop (0.14.0.9000)"
    checkout main
    checkout feature2
    commit id: "qrst (0.14.0.9000)"
    commit id: "uvwx (0.14.0.9000)"
    checkout main
    merge feature1 id: "gpne (0.14.0.9000)"
    merge feature2 id: "punx (0.14.0.9000)"
    branch release
    checkout release
    commit id: "2zy1 (0.14.1)"
    checkout main
    merge release id: "1u2n (1.14.1)" tag: "0.14.1"
```

<a id="major">`X`</a>
: **Major version number**: this version number will change if there are
  significant breaking changes to any of the user-facing workflows. That is, if
  a change requires users to modify their scripts, then it is a breaking change.
  **EXAMPLE**: There are no examples of hubverse packages undergoing a major
  version change, but [schemas v3.0.0](https://github.com/hubverse-org/schemas/releases/tag/v3.0.0)
  included the breaking change of switching `sample/output_type_id` (an array)
  to `sample/output_type_id_params` (an object). The breaking change meant that
  it was a non-trivial task to switch from a `v2.0.1` schema to `v3.0.0` and the
  users. This was reflected in the month-long timeline between [the
  announcement of the change on
  2024-05-13](https://github.com/orgs/hubverse-org/discussions/13) to the
  actual release on 2024-06-18.

<a id="minor">`Y`</a>
: **Minor version number**: this version number will change if there are new
  features or enhanced behaviors available to the users in a way that _does not
  affect how users who do not need the new features use the package_. This
  number grows the fastes in early stages of development.
  **EXAMPLE**: The [`{hubValidations}` package version 0.5.0](https://hubverse-org.github.io/hubValidations/news/index.html#hubvalidations-050)
  gives users the ability to reduce compute time by allowing them to sub-set
  the configuration by the new `output_type` argument to
  `expand_model_out_grid()`. Users who change nothing in their workflows or
  scripts will not see any change for the better or worse.

{#patch}
`Patch`
: **Patch version number**: this version number will change if something that
  was previously broken was fixed, but no new features have been added.
  **EXAMPLE**: the `{hubAdmin}` package needed an enhancement for schema version
  3.0.1, which removed the requirements for `CDF` outputs to have a specific
  pattern. [The actual fix was not something a user would interact
  with](https://github.com/hubverse-org/hubAdmin/pull/29/files#diff-c55622c612385015eaf6d6c2a48e72daae1caa20c58b9531493d74cbaf903f96),
  so [version 1.0.1](https://hubverse-org.github.io/hubAdmin/news/index.html#hubadmin-101)
  was a patch release.

(dev)=
<a id="dev">dev versioning</a>
: **Development version indicator**: this version number indicates that the
  package is in a development state and has the potential to change. When it's on
  the `main` branch, it indicates that the features or patches introduced have
  been reviewed and tested. This version is _appended after every successful
  release_. When this development version indicator exists, the documentation
  site will have an extra `dev/` directory that contains the upcoming changes
  so that we can continue to develop the hubverse without disrupting the
  regular documentation flow.

- For R packages, advice on incrementing the version number from
  [The R Packages Book (Wickham and Bryan, 2023)](https://r-pkgs.org/lifecycle.html#sec-lifecycle-version-number-tidyverse):

    > Increment the development version, e.g. from 9000 to 9001, if you’ve
    > added an important feature and you (or others) need to be able to
    > detect or require the presence of this feature. For example, this can
    > happen when two packages are developing in tandem. This is generally
    > the only reason that we bother to increment the development version.
    > This makes in-development versions special and, in some sense,
    > degenerate. Since we don’t increment the development component with
    > each Git commit, the same package version number is associated with
    > many different states of the package source, in between releases.

- For Python packages, we use [`setuptools-scm`](https://setuptools-scm.readthedocs.io/en/latest/)
  to calculate and apply versions automatically, including the version numbers
  for incremental development releases. When it's added to a Python package
  (via the `pyproject.toml` file), `setuptools-scm` inspects git tags and
  dynamically sets the version number as
  [described in its documentation](https://setuptools-scm.readthedocs.io/en/latest/usage/#default-versioning-scheme).

## Release Process

The sections below outline a general release process for both R and Python
packages. For language-specific checklists, refer to:

- [R release process](r.md)
- [Python release process](python.md)

### Non-urgent releases only

This release process assumes that we have accumulated bugfixes and/or features
in the `main` branch, which we are ready to release. If you have a bug that
needs to be patched _immediately_ and you have new features in the main branch
that are not yet ready to be released, then you should [create a
hotfix](hotfix.md) instead.

(hubverse-release-process-releases)=
### Releases

Releases are a concept that is specific for GitHub. Under the hood, releases are
created from commits or tags. When you use the GitHub web interface, you can
choose to have a tag automatically created from a release (though the tag will
not be annotated or signed, see below for creating stronger, signed tags). All
releases should contain a summary of the changes that happened between this
version and the previous version. A good example of this are [the hubverse
schema release notes](https://github.com/hubverse-org/schemas/releases), and
GitHub offers to automatically fill the release notes with titles and links to
the pull requests that populated the release, which is a good summary (assuming
people create good PR titles).

Once the release is created on GitHub, R packages will be available on the
R-Universe in about an hour or less. Python packages are released to PyPI via
a GitHub workflow that runs when a release tag is added to the repo.

#### Signed Tags

It is good practice to create a tag to release from so that we have a way to
track the releases even if we eventually move away from GitHub. Better practice
is to create _annotated_ tags with the `-a` flag, which adds metadata to the
tag, meaning that it cannot be moved. Even better practice is to create
_signed_ tags with the `-s` flag, which adds a cryptographic signature to the
annotated tag metadata that allows anyone to verify that it came from your
computer and not someone pretending to be you.

Zhian likes to create tags via the command line because he has set up his git
configuration to use [a gpg signature](https://gist.github.com/phortuin/cf24b1cca3258720c71ad42977e1ba57)
so the tags and the releases are both verified. Recently, Git and GitHub added
support for [creating signatures via an SSH key](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification#ssh-commit-signature-verification), which is _a lot_ more approchable than GPG.

Unfortunately, you cannot create a signed tag on the GitHub web interface and it
must be done locally.

```sh
git tag -s X.Y.Z -m 'summary of changes'
git push --tags
```

Once you have a signed tag created, you can then go to the Releases tab on
GitHub and create the release (or you can use the `gh` CLI utility and run
`gh release create X.Y.Z` to interactively create the release).

### R: Releasing to CRAN

R-Universe is not the official R package index—CRAN is. If you want to release
a package to CRAN, it's a relatively straightforward process that takes five
minutes on your part as the maintainer.

The time between sending your package to CRAN and the time it becomes available
to the public usually ranges anywhere from 30 minutes to two or three days,
depending on volume and feedback from CRAN maintainers. Because CRAN submissions
are often a back and forth process, you should not tag your release until you
have confirmed that CRAN has accepted the submission.

Some tips for CRAN submissions:

- Your first submission will likely take the longest (see [Chapter 22 of R Packages by Wickham and Bryan](https://r-pkgs.org/release.html#sec-release-initial))
- Don't use the webform; use [`devtools::release()`](https://devtools.r-lib.org/reference/release.html)
- Remove the `Remotes:` items in the DESCRIPTION with:

    ```sh
    sed -i '' -E -e '/(Remotes:|  hubverse-org)/d' DESCRIPTION
    ```

(you will restore this later with  `git restore DESCRIPTION`). [^uncommitted]

- Commit the `CRAN_SUBMISSION` file when it changes

:::{tip}
If you get an unhelpful or nasty review from a CRAN administrator, contact one of the other Hubverse maintainers who has experience submitting to CRAN (i.e. Zhian) for backup/strategy/comiseration. You can also see if you ran into a common issue by checking [The CRAN Cookbook](https://contributor.r-project.org/cran-cookbook/)
:::


[^uncommitted]: You will get a warning from devtools saying that all files should be tracked and committed before release.
  Double check that all that changed was removing the `Remotes:` field from the
  DESCRIPTION and proceed.

## Testing

Packages will exist in two states: released and stable development. Both of
these states need to pass checks (for example, `R CMD check`, tests, and
coverage), but the challenge with two versions becomes: how do you ensure both
versions work with both versions of the other packages?

The strategy is three-fold:

- All packages in development are tested against development packages. It is
important to remember that development versions must also not introduce
breaking changes. Testing breaking changes should be performed in a separate
branch.
- On a release/hotfix, pull request, all packages are tested against the
released packages to ensure no regressions.
- All packages (released and devel) are tested weekly. This helps to avoid
surprise reverse-dependency problems.

### R Testing

For R packages, testing against the development versions is achieved by setting
[the `Remotes:` section in your DESCRIPTION file](https://r-pkgs.org/dependencies-in-practice.html#sec-dependencies-nonstandard);
this ensures that when dependencies are installed for the GitHub workflow run,
the hubverse dependencies are installed from GitHub and not the R-universe.

During releases and hotfixes (detected by checking that the branch name
contains either `/release/` or  `/hotfix/`, the remote declarations of hubverse
packages are removed (before the dependencies are installed) with the command
`sed -i "" -E -e '/[ ][ ]hubverse-org/d' DESCRIPTION`.

[r-universe]: https://hubverse-org.r-universe.dev/

### Python Testing

At the time of this writing, the Hubverse does not have a documented process
for testing Python packages against development versions.

