# Security Policies


## Background

The repositories in The Hubverse organization host code that is responsible for
the infrastructure behind each and every individual hub. To help prevent
[supply-chain attacks](https://en.wikipedia.org/wiki/Supply_chain_attack) on
hubs which may contain sensitive information, it is imperative that our
repositories have standard security policies. In early 2025, an official
decision was made to implement standard security practices for the GitHub
Actions workflows used by repositories in The Hubverse (see
[2025-02-13-rfc-github-action-security](https://github.com/reichlab/decisions/blob/main/decisions/2025-02-13-rfc-github-action-security.md#decision)
for details).

This document helps to summarize the decision and provide a guide to how it
is implemented in The Hubverse. The practical reference for action pinning
in workflow templates is maintained in the
[hubverse-developer-actions README](https://github.com/hubverse-org/hubverse-developer-actions#action-pinning-policy).

(security-github-settings)=
## Automatic Settings for GitHub

GitHub has a set of [recommended security settings](https://docs.github.com/en/code-security/securing-your-organization/enabling-security-features-in-your-organization/applying-the-github-recommended-security-configuration-in-your-organization) that
are now enabled by default for all repositories in the hubverse-org GitHub
organization.

These settings include:

 - automated [code scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql)
 - [dependabot alerts](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security#what-is-dependabot)
 - protection against accidental leaking of secrets through [push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns#supported-secrets)

These will add notices to the "security" tab in GitHub, where you can see a list
of areas of the code that have vulnerabilities

```{figure} ../images/code-scanning.png
---
figclass: margin-caption
alt: screenshot of a github repo code scanning page showing 30 alerts, with the first three being "Workflow does not contain permissions" with Medium severity
name: code-scanning-fig
---
Code scanning reveals a list of vulnerabilities for this repository. Clicking on
each entry will highlight the location in the code and provide a brief summary
of how to fix the vulnerability.
```

Beyond these automatic settings, there are additional settings that each
repository must have enabled individually.

(security-codeql)=
### CodeQL settings

The default code scanning will detect important vulnerabilities such as
[not setting default permissions](https://github.com/github/codeql/blob/main/actions/ql/src/Security/CWE-275/MissingActionsPermissions.md),
however, the default will not detect
[un-pinned third-party actions](https://github.com/github/codeql/blob/main/actions/ql/src/Security/CWE-829/UnpinnedActionsTag.md).
**If you have administrative access, you need to set the CodeQL settings to use
"extended security" rules (details below).**

:::{important}

When you use a GitHub action in a workflow, there is always an `@` that specifies
either a branch (e.g. `@main`), a tag (e.g. `@v2`), or a Git SHA (e.g. `@14a7e741c1cb130261263aa1593718ba42cf443b`).

GitHub recommends to [pin third-party actions to the full
SHA](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
because the source code behind a branch or tag could change at any time, but
the SHA cannot be changed.

**Using SHA tags for actions can help prevent supply chain attacks similar to
the [tj-actions/changed-files supply-chain attack](https://arstechnica.com/information-technology/2025/03/supply-chain-attack-exposing-credentials-affects-23k-users-of-tj-actions/).**

:::

(security-action-pinning)=
### Action pinning policy

Rather than treating all third-party actions the same, we use a tiered approach
that balances supply-chain security with maintenance burden:

**Tier 1 — GitHub-official actions** (`actions/*`, `github/*`)
: Pin to **major version tag** (e.g., `@v6`). Maintained by GitHub, verified
  publisher, extremely low supply-chain risk.

**Tier 2 — Trusted ecosystem actions**
: Pin to **major version tag** (e.g., `@v2`) or **latest exact version tag** if
  the project doesn't maintain rolling major tags. These are actions from major,
  trusted organisations that are de facto standards in their ecosystem — for
  example, `r-lib/actions` (Posit/tidyverse), `astral-sh/setup-uv` (Astral),
  and `pypa/gh-action-pypi-publish` (Python Packaging Authority). Not all
  trusted projects maintain rolling major version tags — for those that don't, we
  pin to the latest exact version tag and rely on dependabot for minor and major
  update PRs. The authoritative list of Tier 2 action owners is maintained in the
  [CodeQL trusted owners model pack](https://github.com/hubverse-org/hubverse-developer-actions/blob/main/codeql-model-pack/models/trusted-actions-owners.yml).

**Tier 3 — Other third-party actions**
: Pin to **full SHA** with a version comment (e.g., `@9d877eea...  #v4.7.6`).
  These come from individual maintainers or smaller organisations where a
  compromised tag is a real risk.

For the current pinning reference for all actions used in hubverse workflow
templates, see the
[hubverse-developer-actions README](https://github.com/hubverse-org/hubverse-developer-actions#action-pinning-policy).

First, you should go to **Settings** and then in the
left-hand navigation bar, scroll down and click on **Code security**. Scroll down
until you see **Code Scanning**. From there you will see a section called "Tools"
followed by a box that says "CodeQL analysis". In that box, you can select the
expandable menu and select "View CodeQL configuration".

```{figure} ../images/codeql-config-view.png
---
figclass: margin-caption
alt: GitHub screenshot showing the code scanning section described above with a box that says "CodeQL analysis" and a expanded menu item showing the selected item as "View CodeQL configuration"
name: codeql-config-view-fig
---
CodeQL configuration settings can be edited by clicking on the three dots to the right of "CodeQL analysis" and selecting "View CodeQL configuration"
```

When you click on the configuration, you will see a summary of the current
configuration with a button at the bottom that will allow you to edit the
configuration.

```{figure} ../images/codeql-config-edit.png
---
width: 50%
figclass: margin-caption
alt: GitHub screenshot showing the CodeQL configuration having the default setup
name: codeql-config-edit-fig
---
```

When you click that button, you can select the recommended extended security suite


```{figure} ../images/codeql-config-extend.png
---
figclass: margin-caption
alt: GitHub screenshot showing the CodeQL configuration having the default setup
name: codeql-config-extend-fig
---
```

Once you set this, you will get additional alerts for third-party actions that
do not pin actions to SHA. This is important because it allows you to configure
dependabot to automatically open pull requests to update actions that have
security vulnerabilities.

(security-codeql-trusted-owners)=
#### CodeQL trusted owners model pack

Because the [tiered pinning policy](#security-action-pinning) allows Tier 2
actions to use version tags instead of SHAs, the `security-extended` suite would
flag them as unpinned. To prevent these false positives, we maintain a
[CodeQL model pack](https://github.com/hubverse-org/hubverse-developer-actions/tree/main/codeql-model-pack)
that extends the `trustedActionsOwnerDataModel` with our Tier 2 action owners.

The pack is published to GitHub Container Registry as `hubverse-org/trusted-actions`
and is referenced in the hubverse-org org-level CodeQL configuration
(Settings > Advanced Security > Global settings > Code scanning), so it applies
to all repos automatically.

When a new action owner is promoted to Tier 2, add it to
[`trusted-actions-owners.yml`](https://github.com/hubverse-org/hubverse-developer-actions/blob/main/codeql-model-pack/models/trusted-actions-owners.yml)
— the pack is automatically republished on merge.

(security-dependabot)=
### Dependabot Setup

Dependabot's default behavior is to flag potential security vulnerabilities introduced by a project's dependencies. You can also be more proactive by configuring Dependabot to submit pull requests as new versions of project dependencies become available. Regular dependency updates reduces the likelihood of actual vulnerabilities.  You can set this
up by adding a `.github/dependabot.yml` file to your repository.

You should set up dependabot for any [ecosystem](https://docs.github.com/en/enterprise-cloud@latest/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories#supported-ecosystems-and-repositories) you use (e.g. Python and JavaScript),
but the most important one to use is the github actions ecoystem. GitHub has a
[detailed writeup of setting up dependabot to update github actions](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot) and this is a template YAML file that you can use:

```{code-block} yaml
# instruct GitHub dependabot to scan github actions for updates

version: 2
updates:
  - package-ecosystem: "github-actions"
    # dependabot automatically checks .github/workflows/ and .github/actions/
    directory: "/"
    schedule:
      interval: "weekly"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-patch"]
    groups:
      all-updates:
        applies-to: version-updates
        update-types:
          - minor
          - major
```

This configuration:
- **Ignores patch updates** for all actions, reducing PR noise for SHA-pinned and
  exact-version-pinned actions.
- **Groups all minor and major updates** into a single PR instead of one per action.
- **Does not affect security alerts** — dependabot security alerts are a separate
  system and will still fire for known CVEs regardless of version update settings.

For more customization information, refer to [GitHub's documentation for the `dependabot.yml` file](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference).

(security-adding-actions)=
### Adding a new third-party action

When introducing a new third-party GitHub Action to a hubverse workflow, follow
these steps to determine the appropriate trust tier and pinning method:

1. **Check the org-level actions allowlist.** The hubverse-org organisation
   restricts which actions are allowed to run. If the action is not already
   permitted, an org admin will need to add it (Settings > Actions > General >
   Actions permissions).

2. **Assess the trust tier.** Consider:
   - Is it maintained by a major, well-funded organisation?
   - Is it a de facto standard in its ecosystem?
   - Is the publisher verified on GitHub Marketplace?
   - Does the broader community use version tags rather than SHA pins?

   If the answer to all of these is yes, it may qualify as Tier 2. Otherwise,
   default to Tier 3.

3. **Pin the action** according to its tier (see
   [action pinning policy](#security-action-pinning)).

4. **If Tier 2**, add the action owner to the
   [CodeQL trusted owners model pack](https://github.com/hubverse-org/hubverse-developer-actions/blob/main/codeql-model-pack/models/trusted-actions-owners.yml)
   so it doesn't trigger false positive unpinned-action alerts.

5. **Update the workflow templates** in
   [hubverse-developer-actions](https://github.com/hubverse-org/hubverse-developer-actions)
   if the action will be used across multiple repos.

(security-codeowners)=
## Code Owners

[The `.github/CODEOWNERS` file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
is a way to tell GitHub who is responsible for specific sections of a repository.

All repositories that use GitHub actions must specify at least the following
codeowners file:

```
# require core team member review for updates to GitHub workflows
/.github/CODEOWNERS @hubverse-org/hubverse-developers
/.github/actions/ @hubverse-org/hubverse-developers
/.github/shared/ @hubverse-org/hubverse-developers
/.github/workflows/ @hubverse-org/hubverse-developers
```

The hubverse-org GitHub organization now has a specific team for the core
hubverse developers called `hubverse-org/hubverse-developers` who all have
"maintain" access to the hubverse repositories and approval from at least one
member of this team is required to make changes to any GitHub workflow files.

## Branch protections and rulesets

The `main` branch for all repositories must be protected. Any new commits to
`main` must be part of an approved pull request.

Read more [about branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

