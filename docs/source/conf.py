# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Modeling Hub Documentation'
copyright = '2023, Consortium of Infectious Disease Modeling Hubs'
author = 'Consortium of Infectious Disease Modeling Hubs'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser', # markdown (NOTE: this is NOT mystmd)
    'sphinx_design', # tab panels and boxes 
    'sphinxcontrib.mermaid', # compose diagrams in code
]

# -- Options for mermaid
mermaid_d3_zoom = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# These folders are copied to the documentation's HTML output
html_static_path = ['../_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

# from https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "amsmath",
    "deflist",
    "dollarmath",
    "fieldlist",
    "substitution",
    "tasklist",
    "colon_fence",
    "attrs_inline"
]

# -- Options for HTML output

html_theme = 'sphinx_book_theme'
html_logo = 'images/LOGO-hubverse-withtext.png'
html_favicon = 'images/hubverse-favicon.png'
html_title = 'Hubverse'
html_theme_options = {
    "home_page_in_toc": False,
    #"github_url": "https://github.com/hubverse-org/hubDocs",
    "repository_url": "https://github.com/hubverse-org/hubDocs",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    #"use_edit_page_button": True,
    "use_issues_button": True,
    "use_sidenotes": True,
    #"navbar_persistent": ["theme-switcher", "navbar-icon-links"],
}

html_js_files = [
    'js/custom.js',
]

# -- Options for EPUB output
epub_show_urls = 'footnote'

schema_version = "v3.0.1"
# Use schema_branch variable to specify a branch in the schemas repository from which config schema will be source, especially for docson widgets.
# Useful if the schema being documented hasn't been released to the `main` branch in the schemas repo yet. If version has been released already, set this to "main".
schema_branch = "br-"+schema_version

# The following statements override any custom branch assigned to schema branch if the build is being run on READTHEDOCS and is either a build for a new tag or on a branch
# (in contrast to being run in a pull request or locally). This ensures that any production versions of the docs published on the hubDocs `main` branch always 
# point to schema on the `main` branch of the `schemas` repository. It also allows for previewing docson widgets and links to schema in branches other than the
# main branch in the schemas repos when developing locally or in pull requests
import os
build_type = os.environ.get("READTHEDOCS_VERSION_TYPE")
if build_type is None:
    build_type = "unknown"

if build_type in ("tag", "branch"):
    schema_branch = "main"

myst_substitutions = {
    'schema_version': schema_version,
    'schema_branch': schema_branch
}
