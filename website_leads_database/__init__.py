"""Python SDK for the hosted Shopify & Ecommerce Store Finder Apify Actor."""
from .client import WebsiteLeadsDatabaseClient
from .exceptions import WebsiteLeadsDatabaseError, AuthenticationError, ActorRunError, ActorTimeoutError

__version__ = "0.2.0"
__all__ = ["WebsiteLeadsDatabaseClient", "WebsiteLeadsDatabaseError", "AuthenticationError", "ActorRunError", "ActorTimeoutError"]
