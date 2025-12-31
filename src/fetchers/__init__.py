# Icon fetchers package

from .azure import AzureFetcher
from .base import BaseFetcher, IconCategory
from .dynamics365 import Dynamics365Fetcher
from .microsoft365 import Microsoft365Fetcher

__all__ = [
    "BaseFetcher",
    "IconCategory",
    "AzureFetcher",
    "Microsoft365Fetcher",
    "Dynamics365Fetcher",
]
