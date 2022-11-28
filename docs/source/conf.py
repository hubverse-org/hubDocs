# Configuration file for the Sphinx documentation builder.
from os import path
from shutil import copytree, rmtree
#from os import mkdir, walk
import os
from sphinx.util.fileutil import copy_asset_file

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



def copy_custom_files(app, exc):
    if app.builder.format == 'html' and not exc:
        staticdir = os.path.join(app.builder.outdir, '_static/docson/')
        print(staticdir)
        rmtree(staticdir)
        root =  os.path.join(app.builder.srcdir, '../_static/docson/')
        print(root)
        #os.makedirs(staticdir, exist_ok=True)
        copytree(root, staticdir, dirs_exist_ok=True)
        #filenames = [os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]
        #print(filenames)
        for path, subdirs, files in os.walk(staticdir):
            for name in files:
                #print(path)
                #print(name)
                #copy_asset_file(os.path.join(path, name), staticdir)
                print(os.path.join(path, name))
        #copy_asset_file('_static/docson/docson.js', staticdir)

def setup(app):
    app.connect('build-finished', copy_custom_files)
