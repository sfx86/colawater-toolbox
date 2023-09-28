import os
import sys

# make sure sphinx has right source path
sys.path.insert(0, os.path.abspath("../../src"))

# project info
project = "colawater-toolbox"
copyright = "2023, Columbia Water"
author = "Columbia Water"
release = "3.6.0"

# general config
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
]
templates_path = ["_templates"]
exclude_patterns = []
# napoleon
napoleon_numpy_docstring = False
# autoapi
autoapi_dirs = ["../../src"]
autoapi_root = "api-reference"
autoapi_template_dir = f"{templates_path[0]}/_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",  # removing makes the API reference empty for some reason
    # "private-members",
    "show-inheritance",
    "show-module-summary",
    # "special-members",
    "imported-members",
]
# include shared links at the end of every file
rst_epilog = ".. include:: /include/links.rst"

# theme
html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_favicon = "_static/logo.ico"

project_tagline = "ArcGIS geoprocessing tools for Columbia Water"
html_title = f"{project} {release} <br><small>{project_tagline}</small>"

html_theme_options = {
    "navigation_with_keys": True,
    "top_of_page_button": None,
    "globaltoc_maxdepth": -1,
    "globaltoc_collapse": True,
}
