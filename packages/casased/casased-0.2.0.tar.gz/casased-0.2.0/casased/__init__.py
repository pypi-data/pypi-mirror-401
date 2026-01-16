"""
casased - Casablanca Stock Exchange Data Retriever
==================================================

A Python library for retrieving stock market data from the Casablanca Stock Exchange.
"""

from .load import get_history, loadata, loadmany, get_intraday, getIntraday
from .notation import notation, notation_code, notation_value, list_assets, get_isin_by_name
from .tech import getPond

__version__ = "0.2.0"

__all__ = [
    # Data loading functions
    "get_history",
    "loadata",
    "loadmany",
    "get_intraday",
    "getIntraday",
    # Notation/asset functions
    "notation",
    "notation_code",
    "notation_value",
    "list_assets",
    "get_isin_by_name",
    # Technical data functions (working)
    "getPond",
]


# Deprecated functions - moved to roadmap due to website structure changes
def _deprecated_function(func_name: str, message: str = None):
    """Create a deprecated function wrapper."""
    def wrapper(*args, **kwargs):
        import warnings
        msg = message or f"{func_name} is temporarily unavailable due to website structure changes. See ROADMAP.md for planned restoration."
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        return {}
    wrapper.__name__ = func_name
    wrapper.__doc__ = f"DEPRECATED: {message or 'Temporarily unavailable due to website changes.'}"
    return wrapper


# These functions are deprecated until website scraping is updated
getCours = _deprecated_function("getCours", "getCours is temporarily unavailable - casablanca-bourse.com structure changed. See ROADMAP.md")
getKeyIndicators = _deprecated_function("getKeyIndicators", "getKeyIndicators is temporarily unavailable - casablanca-bourse.com structure changed. See ROADMAP.md")
getDividend = _deprecated_function("getDividend", "getDividend is temporarily unavailable - casablanca-bourse.com structure changed. See ROADMAP.md")
getIndex = _deprecated_function("getIndex", "getIndex is temporarily unavailable - casablanca-bourse.com structure changed. See ROADMAP.md")
getIndexRecap = _deprecated_function("getIndexRecap", "getIndexRecap is temporarily unavailable - casablanca-bourse.com structure changed. See ROADMAP.md")