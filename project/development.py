# -*- encoding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Haltu Oy, http://haltu.fi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import sys
from project.settings import *

DEBUG = True
TEMPLATE_DEBUG = True

if 'test' in sys.argv:
  DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
  TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
  BROKER_BACKEND = 'memory'
  CELERY_ALWAYS_EAGER = True

  PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
  )

  EMAIL_BACKEND = 'django.core.mail.backend.locmem.EmailBackend'

  NOSE_ARGS = [
      '--verbosity=2',
      '--with-tissue',
      '--tissue-statistics',
      '--tissue-color',
      '--tissue-ignore=E111,E501,E128,E114,E121,W391',
      '--with-coverage',
      '--cover-package=authdata',
      '--cover-package=external_ldap',
      '--detailed-errors',
      '--nocapture',
  ]

# try:
#   from local_settings import *
# except ImportError:
#   pass

