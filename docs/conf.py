"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Project information -----------------------------------------------------
# import your own package here
import vodftools

project = "vodftools"
copyright = "CTAO"
author = "CTAO Computing Department"
version = vodftools.__version__
# The full version, including alpha/beta/rc tags.
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.autodoc_pydantic",
    "sphinxcontrib.programoutput",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# have all links automatically associated with the right domain.
default_role = "py:obj"


# intersphinx allows referencing other packages sphinx docs
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_theme_options = dict(
    navigation_with_keys=False,
    logo=dict(
        image_light="_static/vodf-logo.svg",
        image_dark="_static/vodf-logo.svg",
        alt_text="ctao-logo",
    ),
    # setup for displaying multiple versions, also see setup in .gitlab-ci.yml
    switcher=dict(
        json_url="http://xxx/versions.json",  # noqa: E501
        version_match="latest" if ".dev" in version else f"v{version}",
    ),
    navbar_start=["navbar-logo", "version-switcher"],
)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

python_use_unqualified_type_names = True
add_module_names = False
autodoc_pydantic_model_erdantic_figure = True
autodoc_pydantic_model_erdantic_figure_collapsed = False


nitpick_ignore = [
    ("py:class", "pydantic.main.BaseModel"),
]
