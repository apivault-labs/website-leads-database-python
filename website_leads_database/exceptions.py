"""Public exception hierarchy for the Shopify & Ecommerce Store Finder SDK."""

class WebsiteLeadsDatabaseError(Exception):
    """Base SDK error."""

class AuthenticationError(WebsiteLeadsDatabaseError):
    """The Apify token is missing or rejected."""

class ActorRunError(WebsiteLeadsDatabaseError):
    """The Actor run or Dataset request failed."""

class ActorTimeoutError(WebsiteLeadsDatabaseError):
    """The client stopped waiting before the Actor completed."""
