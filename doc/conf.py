
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import sys
sys.path.append('.')
sys.path.append('..')

extensions = [
  'sphinx.ext.todo',
  'sphinx.ext.autodoc',
  ]

templates_path = ['_templates']
html_theme_path = ['_themes']
html_static_path = ['_static']
source_suffix = '.rst'
master_doc = 'index'
project = u'eca-auth-data'
copyright = u''
version = ''
release = ''
language = 'en'
html_title = 'eca-auth-data'
unused_docs = []
exclude_trees = []
pygments_style = 'colorful'
#html_theme = 'nature'
#html_theme = 'pyramid'
html_theme = 'default'
html_theme_options = {}
html_use_modindex = False
html_use_index = True
html_show_sourcelink = False
html_copy_source = False
html_file_suffix = '.html'
html_last_updated_fmt = '%b %d, %Y'
#html_use_smartypants = True
html_additional_pages = {
#  'index': 'index.html',
  }

