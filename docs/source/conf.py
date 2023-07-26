import os
import sys
from re import template

sys.path.insert(0, os.path.abspath("../../src"))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ColaWaterToolbox"
copyright = "2023, Columbia Water"
author = "Columbia Water"
release = "2.3.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

napoleon_numpy_docstring = False

autoapi_dirs = ["../../src"]
autoapi_root = "api-reference"
autoapi_template_dir = f"{templates_path[0]}/_autoapi_templates"

rst_epilog = ".. include:: /include/links.rst"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

project_tagline = "ArcGIS geoprocessing tools for Columbia Water"
html_title = f"{project} {release} <br><small>{project_tagline}</small>"


html_theme_options = {
    "navigation_with_keys": True,
    "top_of_page_button": None,
    "globaltoc_maxdepth": -1,
    "globaltoc_collapse": True,
}
