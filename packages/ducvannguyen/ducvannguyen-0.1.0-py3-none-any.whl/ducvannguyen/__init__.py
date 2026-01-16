"""
Duc Van Nguyen Package
A Python package for demonstration purposes.
"""

__version__ = "0.1.0"
__author__ = "Duc Van Nguyen"

def hello():
    """Return a greeting message."""
    return "Hello from ducvannguyen package!"

def get_info():
    """Return package information."""
    return {
        "name": "ducvannguyen",
        "version": __version__,
        "author": __author__
    }
