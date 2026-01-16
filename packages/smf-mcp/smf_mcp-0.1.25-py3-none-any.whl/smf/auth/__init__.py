"""
SMF authentication helpers and providers.
"""

from smf.auth.policy import require_any_scope, require_scopes
from smf.auth.providers.oidc import OIDCProxyProvider

__all__ = [
    "OIDCProxyProvider",
    "require_scopes",
    "require_any_scope",
]
