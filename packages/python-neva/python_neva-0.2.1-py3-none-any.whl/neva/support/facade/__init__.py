"""Built-in facades for static access to the framework components."""

from neva.support.facade.app import App
from neva.support.facade.config import Config
from neva.support.facade.log import Log

__all__ = [
    "App",
    "Config",
    "Log",
]
