# Releasing Hotfixes

This document is adapted for The Hubverse from
[The Carpentries Developer’s Handbook](https://carpentries.github.io/workbench-dev/hotfixes.html)
(c) The Carpentries under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

## Introduction

A hotfix is a bug fix for a situation where a bug has been found, but the main
branch has new features that are not yet ready to be released.

A process for creating a hotfix release is similar to that of the standard
release with the following differences:

|        | standard | hotfix |
| ------ | -------- | ------ |
| parent branch | `main` | `<tag>` |
| tag and release | after merge | _before_ merge |
| merge conflicts | never | with `DESCRIPTION` and `NEWS.md` |

An example of a good candidate for a hotfix in the hubverse is
[hubValidations issue #123](https://github.com/hubverse-org/hubValidations/issues/123).
This bug was discovered in [hubValidations 0.6.2](https://github.com/hubverse-org/hubValidations/releases/tag/v0.6.2).
However, the discovery occurred after the `main` branch already
[had unreleased features](https://github.com/hubverse-org/hubValidations/commit/85d58251c7cbcbb4064a72f8126ad8846f351dbd).
While the new features were stable, the documentation was not fully polished[^unreleased].
A hotfix would give developers more time to document the new feature.

[^unreleased]: [the `create_custom_check()`
  function](https://github.com/hubverse-org/hubValidations/issues/121) was
  added in [pull request 122](https://github.com/hubverse-org/hubValidations/pull/122),
  but the vignette for creating the custom check functions was still in a draft
  state.

While this bug fix was released through the [standard release process](release-process.md),
It could have easily been a hotfix release. This document will be a walkthrough
of the hotfix process if it had been applied in
[hubValidations pull request 124](https://github.com/hubverse-org/hubValidations/pull/124).

## Conventions

This walkthrough will be presented as if our lead developer, Anna Krystalli
were fixing the bug (which she did in real life!) via this hotfix process. We
will diagram the process using the following conventions:

- Each step will be written in the second person perspective
- The commit IDs and branch names are simplified and will not directly match
  the real life names
- Each new commit is a unique sequence of letters
- Each merge commit is a combination of letters from the two previous commits
- Each non-main branch will be prefixed with `ak/`
- The command prompt will be displayed in the following format

   ```sh
   $ (<branch>) <COMMAND> # comment about <COMMAND>
   #| output of <COMMAND>
   ```

## The Scenario

- [hubValidations 0.6.2](https://github.com/hubverse-org/hubValidations/releases/tag/v0.6.2)
  was released on 2024-09-20.
- [the `create_custom_check()` function](https://github.com/hubverse-org/hubValidations/pull/122)
  was merged into hubValidations 0.6.2.9000 on 2024-10-01
  after it had been tested and validated.
- the vignette for creating custom validations was being drafted in a separate
  branch on 2024-10-01.
- [A bug was discovered in hubValidations 0.6.2 on 2024-10-02](https://github.com/hubverse-org/hubValidations/issues/123).

This is what the state of the project would look like on 2024-10-02 (simplified):

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "v0.6.2"
    branch ak/create-fun/121
    branch ak/document-fun/121
    checkout main
    checkout ak/create-fun/121
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge ak/create-fun/121 id: "gpne"
    checkout ak/document-fun/121
    commit id: "qrst"
    commit id: "uvwx"
```

The rest of the walkthrough will detail the four steps required to fix the bug.

## Step 1: Create a Fix and Pull Request

Normally, to fix bugs, you would check out a new bugfix branch from the `main`
branch. Here's the catch: if you check out from the main branch you will grab
`ak/create-fun/121` as well, which is not yet ready for production because you
intended `ak/document-fun/121` to be released along side. In this case, you
need to create a hotfix, and create the branch _from the last tag_ (which in
this case is `v0.6.2`).

**IMPORTANT**: When you create a hotfix, name the branch
`<author>/hotfix/<issue>`. By using `/hotfix/` in the branch name, the GitHub
workflows will know to test this package against the released versions from the
R-universe.

Python package workflows do not currently have behavior triggered by `/hotfix/`
in the branch name but should follow this naming convention regardless.

```sh
(main)$ git describe
#| v0.6.2-3-ggpne
(main)$ git switch --detach v0.6.2 # checkout the tag
#| HEAD is now at efgh Merge pull request #119 from hubverse-org/ak/release/v0.6.2
((v0.6.2))$ git switch -c ak/hotfix/123 # create a new branch
#| switched to new branch 'ak/hotfix/123'
(ak/hotfix/123)$ git push -u origin ak/hotfix/123 # push the branch to GitHub
```

Now you are ready to iterate and fix the bug on the hotfix branch, adding the
test and then adding the fix and any documentation to go with it.

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "v0.6.2"
    branch ak/create-fun/121
    branch ak/document-fun/121
    branch ak/hotfix/123
    checkout main
    checkout ak/create-fun/121
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge ak/create-fun/121 id: "gpne"
    checkout ak/document-fun/121
    commit id: "qrst"
    commit id: "uvwx"
    checkout ak/hotfix/123
    commit id: "yzAB"
```

When you have finished iterating on your own and are satisfied that it works,
the next step is to open a pull request and get a review.

## Step 2: Ensure checks pass, get a review, and create tag

You should check that the hotfix does not break any existing tests, which are
automatically run from the pull request. Once you have confirmed that
everything works as expected and have an approving review, the next step is to
bump the version and add a tag. This tag will allow you to release the patch
version.

```sh
(ak/hotfix/123)$ git add DESCRIPTION NEWS.md
(ak/hotfix/123)$ git commit -m 'bump version to v0.6.3'
(ak/hotfix/123)$ git tag -s v0.6.3 -m 'hotfix: validate tasks with optional output types'
(ak/hotfix/123)$ git push
(ak/hotfix/123)$ git push --tags
```

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "v0.6.2"
    branch ak/create-fun/121
    branch ak/document-fun/121
    branch ak/hotfix/123
    checkout main
    checkout ak/create-fun/121
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge ak/create-fun/121 id: "gpne"
    checkout ak/document-fun/121
    commit id: "qrst"
    commit id: "uvwx"
    checkout ak/hotfix/123
    commit id: "yzAB"
    commit id: "CDEF" tag: "v0.6.3"
```

**Note the v0.6.3 tag is on the `ak/hotfix/123` branch at the bottom.

At this point, the checks will not run on the pull request because there will be
a conflict in the DESCRIPTION and NEWS.md files. This is okay. All you did was
update the version numbers and add NEWS. **Do not merge at this point**. The
next step is to release the patch.

## Step 3: Release the Patch

You will release the patch using the same method as described in [the releases
chapter](release-process). You can either release on GitHub directly or via the GitHub
CLI. Importantly, when you create the release, you should _create the release
from the new tag_. This can be done via the GitHub interface or using GitHub's
CLI tool.

```sh
(ak/hotfix/123)$ gh release create v0.6.3
```

## Step 4: Resolve Conflicts and Merge

Now that you've created the release, you should resolve the conflicts in the
DESCRIPTION and NEWS files and then merge it back into `main` (note: this will
create two merge commits, but I'm only showing one in the diagram to make it
cleaner):

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "v0.6.2"
    branch ak/create-fun/121
    branch ak/document-fun/121
    branch ak/hotfix/123
    checkout main
    checkout ak/create-fun/121
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge ak/create-fun/121 id: "gpne"
    checkout ak/document-fun/121
    commit id: "qrst"
    commit id: "uvwx"
    checkout ak/hotfix/123
    commit id: "yzAB"
    commit id: "CDEF" tag: "v0.6.3"
    checkout main
    merge ak/hotfix/123 id: "DeFn"
```

Now you will have the patch in place for the released version _and_ the devel
version of this hubverse package, which means that you can continue to develop
as normal and merge the next feature when you are ready:

```{mermaid}
gitGraph
    commit id: "abcd"
    commit id: "efgh" tag: "v0.6.2"
    branch ak/create-fun/121
    branch ak/document-fun/121
    branch ak/hotfix/123
    checkout main
    checkout ak/create-fun/121
    commit id: "ijkl"
    commit id: "mnop"
    checkout main
    merge ak/create-fun/121 id: "gpne"
    checkout ak/document-fun/121
    commit id: "qrst"
    commit id: "uvwx"
    checkout ak/hotfix/123
    commit id: "yzAB"
    commit id: "CDEF" tag: "v0.6.3"
    checkout main
    merge ak/hotfix/123 id: "DeFn"
    checkout ak/document-fun/121
    commit id: "GHIJ"
    commit id: "KLMN"
    checkout main
    merge ak/document-fun/121 id: "FnNL"
```

