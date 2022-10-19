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

To build and preview the site locally, you the following steps 
(assuming you already have python installed) are adapted from the 
[ReadTheDocs site](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html):

1. Install sphinx: `pip install sphinx`.
2. We are using [MyST to enable Markdown](https://github.com/executablebooks/MyST-Parser/edit/master/docs/syntax/syntax.md), 
so you need to install myst-parser: `pip install myst-parser`.
3. Install the theme we are using: `pip install sphinx-book-theme`. Documentation on theme-specific elements can be found [here](https://sphinx-book-theme.readthedocs.io/en/stable/index.html).
4. In the `docs` folder, run `make html` to build the site locally to inspect changes.

## Contribution guidelines
In general, contributions should be made via pull requests to the `main` branch. 
Note that PRs should trigger preview builds of the site, so you should be able
to double-check that your changes look as expected.
