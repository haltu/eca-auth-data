
from roledb.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

try:
  from settings_local import *
except ImportError:
  pass

