# NGram documentation build configuration file.

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']

# The suffix of source filenames.
source_suffix = '.rst'

# The human-readable project name
project = u'Python NGram'

# The short X.Y version.
version = '4.0'

# The full version, including alpha/beta/rc tags.
release = '4.0.1'

# Language the docs are written in.
language = 'en'

# Copyright byline.
copyright = 'Graham Poulter, Michel Albert 2008-2021'

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Name (excluding extension) of root document.
root_doc = 'index'