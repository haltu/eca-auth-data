
from roledb.settings import *

DEBUG = False

try:
  from roledb.local_settings import *
except ImportError:
  pass

