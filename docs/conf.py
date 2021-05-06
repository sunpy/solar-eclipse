# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os

# -- Project information -----------------------------------------------------

project = 'solar-eclipse'
copyright = '2021, The SunPy Developers'
author = 'The SunPy Developers'

# The full version, including alpha/beta/rc tags
from eclipse import __version__
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx_automodapi.automodapi',
    'sphinx_automodapi.smart_resolver',
    'sphinx_gallery.gen_gallery'
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

import sphinx_gallery
extensions += ["sphinx_gallery.gen_gallery"]

sphinx_gallery_conf = {
	'backreferences_dir':
	'generated{}modules'.format(os.sep),  # path to store the module using example template
	'filename_pattern':
	'^((?!skip_).)*$',  # execute all examples except those that start with "skip_"
	'examples_dirs': os.path.join('..', 'examples'),  # path to the examples scripts
	'gallery_dirs': os.path.join('generated',
									'gallery'),  # path to save gallery generated examples
	'default_thumb_file': os.path.join('.', 'logo', 'sunpy_icon_128x128.png'),
	'reference_url': {
		'eclipse': None,
		'sunpy': 'http://docs.sunpy.org/en/stable',
		'astropy': 'http://docs.astropy.org/en/stable/',
		'matplotlib': 'http://matplotlib.org/',
		'numpy': 'http://docs.scipy.org/doc/numpy/',
	},
	'abort_on_example_error': True,
	'plot_gallery': True
}
