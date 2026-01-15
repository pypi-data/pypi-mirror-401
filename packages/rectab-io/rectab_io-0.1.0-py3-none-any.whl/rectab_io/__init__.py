from .analytics import recommenders_analytics
from .auth import validate_auth

# Validate authentication when package is imported
validate_auth()

__version__ = "0.1.0"
__author__ = "Louati Mahdi"

__all__ = ["recommenders_analytics"]