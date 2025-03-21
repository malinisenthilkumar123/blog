# Import all settings from miniblog
import os
import sys

# Add the miniblog directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'miniblog')))

# Import settings from miniblog
from miniblog.settings import * # type: ignore

# Override any settings if needed
# For example:
# DEBUG = True 