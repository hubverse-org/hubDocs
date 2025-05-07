# Generating the Dashboard Website

The [dashboard website
builder](https://github.com/hubverse-org/hub-dash-site-builder) is a [docker
image](#dashboard-tool-docker) which is thin wrapper around [the quarto
publishing system](#dashboard-tool-yq) and [yq](#dashboard-tool-yq). This tool
was designed under the following motivations:

1. Maintenance of this dashboard should be independent from hub maintenance.
2. Anyone should be able to deploy a dashboard as long as they have a hub with
   target data that they can access.
3. The only knowledge anyone should need is of Markdown, YAML, and basic
   operation of GitHub workflows. Knowledge of any particular [website
   generator](https://jamstack.org/generators/) is not required and the user
   should not need to handle any templating that cannot be easily automated.
4. We should not have to maintain a server to deploy these sites.

## References

Here are links to some concepts that are used in the website builder.

- [Building a website using quarto](https://quarto.org/docs/websites/)
- [BASH scripting cheat sheet](https://devhints.io/bash)
- `yq` [tips and tricks](https://mikefarah.gitbook.io/yq/usage/tips-and-tricks)
  and [recipes](https://mikefarah.gitbook.io/yq/recipes). Specific operators
  can be found in the comments of the
  [`modify-quarto-yml.sh`](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/modify-quarto-yml.sh)
  file in the hub-dash-site-builder repository.
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

## Installation

You can install the latest version of this tool with docker:

```bash
docker pull ghcr.io/hubverse-org/hub-dash-site-builder:latest
```

(dashboard-site-source)=
## How the website is built (a tale of two sources)

The website that is built is a fully static site that can be viewed locally. It
is the result of a combination of two sources:

1. [dashboard website builder `static/` directory](https://github.com/hubverse-org/hub-dash-site-builder/tree/main/static) and,
2. [the dashboard repository](https://github.com/hubverse-org/hub-dashboard-template/)

For example, the [source for the hub-dashboard-template website](https://github.com/hubverse-org/hub-dashboard-template/tree/gh-pages), shows the following files and folders.

| site component | from site builder | from user |
| :-------- | :---------------- | :-------- |
| Menu Items | `static/_quarto.yml` | `site-config.yml` |
| Theme      | `static/_quarto.yml` | `site-config.yml` |
| `index.html` | --- | `pages/index.qmd` |
| `about.html` | --- | `pages/about.md` |
| `data.html` | --- | `pages/data.qmd` |
| `img/` | --- | `pages/img` |
| `eval.html` | `static/eval.qmd` | --- |
| `forecast.html` | `static/eval.qmd` | --- |
| `resources/` | `static/resources/` | --- |
| `site_libs` | `static/_quarto.yml` | --- |

On its own, the `static/` directory of the dashboard website contains an
incomplete quarto website. The incomplete parts are:

1. `index.qmd` is missing
2. The JavaScript in `resources/` is incomplete. There is a single line that
   defines the root folder for resource access, with a placeholder called
   `{ROOT}`, which needs to be replaced by a local folder or URL for the
   resource:
   ```js
   const root = "{ROOT}";
   ```

The site builder image effectively performs four steps to complete and render
the site:

1. Combine the contents of `pages/` and `/static/` into a temporary directory, `/tmp/`.
2. Update the JavaScript files to point to the correct resources.
3. Use `yq` to merge `site-config.yml` into `/tmp/_quarto.yml`.
4. Run `quarto render /tmp/` and copy the output to the output directory (`out/`).

```{mermaid}
:config: {"theme": "base", "themeVariables": {"primaryColor": "#dbeefb", "primaryBorderColor": "#3c88be"}}
flowchart TD
  subgraph dashboard
    pages/contents["pages/[contents]"]
    site-config.yml
    out/
  end
  subgraph docker
    subgraph /static/
        /static/contents["/static/[contents]"]
        /static/_quarto.yml["/static/_quarto.yml"]
    end
    yq{{"yq"}}
    subgraph /tmp/
        _quarto.yml["/tmp/_quarto.yml"]
        contents["/tmp/[contents]"]
        _site/["/tmp/_site/"]
        quarto{{"quarto"}}
    end
  end
  pages/contents --> contents
  /static/contents --> contents
  site-config.yml --- yq
  /static/_quarto.yml --- yq
  yq -->|yq -i '...' _quarto.yml | _quarto.yml
  _quarto.yml --> quarto
  contents --> quarto
  quarto -->|quarto render /tmp/| _site/ --> out/

```


