# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Modeling Hub Documentation'
copyright = '2022, Consortium of Infectious Disease Modeling Hubs'
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
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# These folders are copied to the documentation's HTML output
html_static_path = ['../_static']

# from https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "amsmath",
    "deflist",
    "dollarmath",
    "fieldlist",
]

# -- Options for HTML output

html_theme = 'sphinx_book_theme'
#html_logo = "_static/LOGO-CovidForecastHub_VIRUS-blue.png"
html_favicon = "forecast-hub-favicon.png"
html_title = "hubDocs"
html_theme_options = {
    "home_page_in_toc": False,
    "github_url": "https://github.com/Infectious-Disease-Modeling-Hubs/hubDocs",
    "repository_url": "https://github.com/Infectious-Disease-Modeling-Hubs/hubDocs",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_sidenotes": True,

}

# -- Options for EPUB output
epub_show_urls = 'footnote'
