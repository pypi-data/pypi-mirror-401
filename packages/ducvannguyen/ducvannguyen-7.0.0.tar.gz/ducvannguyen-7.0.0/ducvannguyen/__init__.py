"""
Duc Van Nguyen Package v7.0.0
Professional Python toolkit with advanced utilities and DucVanNguyen class.

Multiple import options available:
- from ducvannguyen import DucVanNguyen
- from ducvannguyen import ducvannguyen
- from ducvannguyen.core import DucVanNguyen
- import ducvannguyen
"""

__version__ = "7.0.0"
__author__ = "Duc Van Nguyen"

# Import the main class and utilities
from .core import DucVanNguyen, ducvannguyen

# Import all utility functions for backward compatibility
from .core import (
    hello, get_info, string_utils, math_utils, list_utils, 
    file_utils, datetime_utils, web_utils, random_utils, 
    validate_utils, all_utils
)

# Define what gets imported with "from ducvannguyen import *"
__all__ = [
    'DucVanNguyen',           # Main class
    'ducvannguyen',           # Default instance
    'hello',                  # Function
    'get_info',              # Function
    'string_utils',          # Function
    'math_utils',            # Function
    'list_utils',            # Function
    'file_utils',            # Function
    'datetime_utils',        # Function
    'web_utils',             # Function
    'random_utils',          # Function
    'validate_utils',        # Function
    'all_utils'              # Function
]
