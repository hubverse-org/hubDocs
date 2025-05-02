# Dashboard Tools

:::{admonition} Assumptions

This guide assumes that you are familiar and comfortable with the following

- the command line interface including pipes, file redirection, and standard
  utilities like `sed` and `grep`
- Git
- [the concept of a modelling hub](https://hubverse.io/quickstart/)
- [YAML syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
- markdown authoring
- the basics of how HTML, CSS, and JavaScript interact to create a web page.

:::

(dashboard-general)=
## General tools

We use a wide range of tools to build the
[dashboards](/user-guide/dashboards.md). Ultimately, the only tools you will
need to build a dashboard are git, [python](#dashboard-tool-python), and
[docker](#dashboard-tool-docker). Everything else is encapsulated within docker
images.

[Python]{#dashboard-tool-python}
: Python is the backbone of hub-dashboard-predtimechart and is used in the
  control room to get a list of repositories that have the app installed.

[docker]{#dashboard-tool-docker}
: We use docker to containerize the tools needed to build the website and the
  data for the evaluations.

[BASH]{#dashboard-tool-bash}
: We use BASH to orchestrate building of the dashboard website and within the
  GitHub workflows. In particular, we make use of [conditional
  expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions)
  and [parameter
  expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion)
  (e.g. `${HUB%/}` takes the variable `$HUB` and removes any trailing slash).

[R]{#dashboard-tool-r}
: R is the backbone of hubPredEvalsData, which generates the evaluations dashboard

[JavaScript]{#dashboard-tool-javascript}
: Both of the visualizations are built as JavaScript modules. In turn, these
  modules are called from scripts that are loaded in a page of the dashboard,
  which replaces a specific `<div>` element of the webpage with the content.

(dashboard-website)=
## Website

The website is orchestrated with the docker image
[hub-dash-site-builder](https://github.com/hubverse-org/hub-dash-site-builder).
The image bundles [BASH](#dashboard-tool-bash) and [yq](#dashboard-tool-yq) to
join the user data with the template and [quarto](#dashboard-tool-quarto) to
render the markdown to HTML.

[[quarto](https://quarto.org)]{#dashboard-tool-quarto}
: This is the website engine. It is responsible for converting markdown to HTML
   and applying styling.

[[yq](https://github.com/mikefarah/yq/#install)]{#dashboard-tool-yq}
: YAML Query. This tool is similar to the command line JSON processor,
  [jq](https://jqlang.org), except it works with YAML. It is responsible for
  joining the dashboard's `site-config.yml` to
  [`static/_quarto.yml`](https://github.com/hubverse-org/hub-dash-site-builder/blob/main/static/_quarto.yml).
  The rationale behind this is that a user does not have to learn how to use
  quarto in order to generate a site.

(dashboard-forecast)=
## Forecast visualization

The forecasts visualization is built with [PredTimeChart](https://github.com/reichlab/predtimechart), a JavaScript module that displays forecast visualizations.

The data for PredTimeChart is converted from hub format with
[hub-dashboard-predtimechart](https://github.com/hubverse-org/hub-dashboard-predtimechart),
a command-line Python app, which uses the [polars](#dashboard-tool-polars) to
read and convert the data to JSON format.

[[polars](https://pola.rs)]{#dashboard-tool-polars}
: A data manipulation library that provides lazy data frame utilities in Python.
  It gives our tool the ability to read and slice hub data. Eventually, this
  will be subserseded by the hub-data package.

(dashboard-evals)=
## Evaluations visualization

The evaluations visualization is built with
[PredEvals](https://github.com/hubverse-org/predevals), a JavaScript module
that displays the evaluation visualization. Its code is heavily based off of
predtimechart.

The evaluations visualization data are built with the
[hubPredEvalsData-docker](https://github.com/hubverse-org/hubPredEvalsData-docker)
docker image. This bundles the R package
[hubPredEvalsData](#dashboard-tool-hubPredEvalsData), which uses
[hubEvals](#dashboard-tool-hubEvals) and
[scoringutils](#dashboard-tool-scoringutils) to evaluate model performance if
the hub has oracle output available.

[hubPredEvalsData]{#dashboard-tool-hubPredEvalsData}
: generates nested folders of scores disaggregated by task ID

[hubEvals]{#dashboard-tool-hubEvals}
: scores model output

[scoringutils]{#dashboard-tool-scoringutils}
: does some other scoring, IDK

(dashboard-orchestration)=
## Orchestration

The orchestration of all the tools above is performed with GitHub Actions though
a series of workflows in the
[hub-dashboard-control-room](https://github.com/hubverse-org/hub-dashboard-control-room)
repository.

The entirety of the orchestration happens on the `ubuntu-latest` runner of
GitHub Actions. This is a virtual machine that has a bunch of useful software
installed (you can find [**a list of the available tools for the Ubuntu
Runner**](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md)
in the actions/runner-images repository). For our purposes, it has
[docker](#dashboard-tool-docker),
[BASH](#dashboard-tool-bash), [yq](#dashboard-tool-yq),
[jq](#dashboard-tool-jq), [gh](#dashboard-tool-gh), and
[curl](#dashboard-tool-curl) pre-installed.

### Important references

Broadly important references (e.g. you will be reaching back to these often):

- [**Choosing how to run a workflow**](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs). For example, we use a few scenarios: `schedule`, `push`, `workflow_dispatch` (human triggered) and `workflow_call` (workflows triggered from a separate repository).
- [**Workflow syntax**](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#about-yaml-syntax-for-workflows)
- [**Workflow commands**](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions) allows you to use values between job steps
- [**Evaluating expressions**](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions). You will see things like `${{ fromJSON(steps.status.outputs.forecast-ok) || fromJSON(steps.status.outputs.eval-ok) }}`. This guide tells you what they mean and how to evaluate them.


### Broad table of tasks and tools used for each

| task/component | tools |github workflow documentation|
|----------------|-------|-----------------------------|
| Fetching dashboard repository | Git | [actions/checkout](https://github.com/actions/checkout#readme) |
| Determining what to build | [BASH](#dashboard-tool-bash), [yq](#dashboard-tool-yq) | [Setting an output parameter](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#setting-an-output-parameter), [Passing information between jobs](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/passing-information-between-jobs) |
| Checking for resources | BASH, [gh](#dashboard-tool-gh), [curl](#dashboard-tool-curl), [jq](#dashboard-tool-jq) | [branches API endpoint](https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28) |
| Fetching hub repository | Git | actions/checkout (linked above) |
| [Website](#dashboard-website) | [docker](#dashboard-tool-docker) | [Running jobs in a container](https://docs.github.com/en/actions/writing-workflows/choosing-where-your-workflow-runs/running-jobs-in-a-container) |
| [Evaluation visualization](#dashboard-evals) | docker | Running jobs in a container (linked above) |
| [Forecast visualization](#dashboard-forecast) | [python](#dashboard-tool-python) | [actions/setup-python](https://github.com/actions/setup-python#readme) |
| Passing data between Jobs | actions/upload-artifact | [actions/upload-artifact](https://github.com/actions/upload-artifact#readme) |
| Pushing content to GitHub | actions/download-artifact, BASH, Git | [actions/download-artifact](https://github.com/actions/upload-artifact#readme) |

[[gh](https://cli.github.com)]{#dashboard-tool-gh}
: GitHub's CLI interface is useful for performing operations that involve the
  GitHub API as well as operations like creating pull requests. This comes
  pre-installed on all GitHub Actions runners.

[[curl](https://curl.se)]{#dashboard-tool-curl}
: Command line tool for interacting with URLs. This comes standard with macOS
  and on GitHub Actions runners. It is particularly useful to check if a URL is
  valid (e.g. for checking if a resource is available):
  ```
  curl -o /dev/null --silent -Iw '%{http_code}' "https://hubverse.io"
  # 200
  ```

[[jq](https://jqlang.org)]{#dashboard-tool-jq}
: Command line tool that allows you to manipulate JSON from the command line.
  This is _very_ useful for parsing queries to the GitHub API. It's also really
  useful for parsing the `tasks.json` file of a hub. For example, here's a quick
  way to get all of the known output types across rounds and model tasks:
  ```
  jq '[.rounds[].model_tasks[].output_type | keys] | flatten' < hub-config/tasks.json
  ```
