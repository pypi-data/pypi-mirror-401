"""
Generic OIDC/OAuth proxy provider for FastMCP.

This provider is configured via environment variables to enable
authentication for any MCP server (Elastic, Snowflake, etc.)
without code changes.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.server.auth.oidc_proxy import OIDCConfiguration
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.settings import ENV_FILE
from fastmcp.utilities.auth import parse_scopes
from fastmcp.utilities.types import NotSet, NotSetT


def _parse_list(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, tuple):
        return [str(v) for v in value]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except json.JSONDecodeError:
            pass
        return [v.strip() for v in text.split(",") if v.strip()]
    return None


def _parse_dict(value: Any) -> Optional[Dict[str, str]]:
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items()}
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return {str(k): str(v) for k, v in parsed.items()}
        except json.JSONDecodeError:
            pass
    return None


def _stringify_dict(value: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    if value is None:
        return None
    return {str(k): str(v) for k, v in value.items()}


class OIDCProxyProviderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FASTMCP_SERVER_AUTH_OIDC_",
        env_file=ENV_FILE,
        extra="ignore",
    )

    # OIDC discovery (optional)
    config_url: Optional[str] = None
    strict: Optional[bool] = None
    timeout_seconds: Optional[int] = None

    # Explicit endpoints (required if config_url not set)
    authorization_endpoint: Optional[str] = None
    token_endpoint: Optional[str] = None
    revocation_endpoint: Optional[str] = None
    jwks_uri: Optional[str] = None
    issuer: Optional[str] = None

    # OAuth client configuration (required)
    client_id: Optional[str] = None
    client_secret: Optional[SecretStr] = None
    base_url: Optional[str] = None
    issuer_url: Optional[str] = None
    redirect_path: Optional[str] = None
    token_endpoint_auth_method: Optional[str] = None
    forward_pkce: bool = True

    # JWT verification
    jwt_public_key: Optional[SecretStr] = None
    jwt_algorithm: Optional[str] = None
    audience: Optional[str] = None
    required_scopes: Optional[List[str]] = None

    # OAuth proxy behavior
    valid_scopes: Optional[List[str]] = None
    allowed_client_redirect_uris: Optional[List[str]] = None
    require_authorization_consent: bool = True
    jwt_signing_key: Optional[SecretStr] = None
    fallback_access_token_expiry_seconds: Optional[int] = None

    # Extra parameters for upstream requests
    extra_authorize_params: Optional[Dict[str, str]] = None
    extra_token_params: Optional[Dict[str, str]] = None

    @field_validator("required_scopes", "valid_scopes", mode="before")
    @classmethod
    def _parse_scopes(cls, v: Any):
        return parse_scopes(v)

    @field_validator("allowed_client_redirect_uris", mode="before")
    @classmethod
    def _parse_allowed_redirects(cls, v: Any):
        return _parse_list(v)

    @field_validator("extra_authorize_params", "extra_token_params", mode="before")
    @classmethod
    def _parse_extra_params(cls, v: Any):
        return _parse_dict(v)


class OIDCProxyProvider(OAuthProxy):
    """
    Generic OAuth/OIDC proxy provider configured via environment variables.

    Set:
      FASTMCP_SERVER_AUTH=smf.auth.providers.oidc.OIDCProxyProvider
    """

    def __init__(
        self,
        *,
        config_url: str | NotSetT | None = NotSet,
        strict: bool | NotSetT | None = NotSet,
        timeout_seconds: int | NotSetT | None = NotSet,
        authorization_endpoint: str | NotSetT | None = NotSet,
        token_endpoint: str | NotSetT | None = NotSet,
        revocation_endpoint: str | NotSetT | None = NotSet,
        jwks_uri: str | NotSetT | None = NotSet,
        issuer: str | NotSetT | None = NotSet,
        client_id: str | NotSetT | None = NotSet,
        client_secret: str | NotSetT | None = NotSet,
        base_url: str | NotSetT | None = NotSet,
        issuer_url: str | NotSetT | None = NotSet,
        redirect_path: str | NotSetT | None = NotSet,
        token_endpoint_auth_method: str | NotSetT | None = NotSet,
        forward_pkce: bool | NotSetT = NotSet,
        jwt_public_key: str | NotSetT | None = NotSet,
        jwt_algorithm: str | NotSetT | None = NotSet,
        audience: str | NotSetT | None = NotSet,
        required_scopes: List[str] | NotSetT | None = NotSet,
        valid_scopes: List[str] | NotSetT | None = NotSet,
        allowed_client_redirect_uris: List[str] | NotSetT | None = NotSet,
        require_authorization_consent: bool | NotSetT = NotSet,
        jwt_signing_key: str | NotSetT | None = NotSet,
        fallback_access_token_expiry_seconds: int | NotSetT | None = NotSet,
        extra_authorize_params: Dict[str, str] | NotSetT | None = NotSet,
        extra_token_params: Dict[str, str] | NotSetT | None = NotSet,
    ) -> None:
        settings = OIDCProxyProviderSettings.model_validate(
            {
                k: v
                for k, v in {
                    "config_url": config_url,
                    "strict": strict,
                    "timeout_seconds": timeout_seconds,
                    "authorization_endpoint": authorization_endpoint,
                    "token_endpoint": token_endpoint,
                    "revocation_endpoint": revocation_endpoint,
                    "jwks_uri": jwks_uri,
                    "issuer": issuer,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "base_url": base_url,
                    "issuer_url": issuer_url,
                    "redirect_path": redirect_path,
                    "token_endpoint_auth_method": token_endpoint_auth_method,
                    "forward_pkce": forward_pkce,
                    "jwt_public_key": jwt_public_key,
                    "jwt_algorithm": jwt_algorithm,
                    "audience": audience,
                    "required_scopes": required_scopes,
                    "valid_scopes": valid_scopes,
                    "allowed_client_redirect_uris": allowed_client_redirect_uris,
                    "require_authorization_consent": require_authorization_consent,
                    "jwt_signing_key": jwt_signing_key,
                    "fallback_access_token_expiry_seconds": fallback_access_token_expiry_seconds,
                    "extra_authorize_params": extra_authorize_params,
                    "extra_token_params": extra_token_params,
                }.items()
                if v is not NotSet
            }
        )

        config = None
        if settings.config_url:
            config = OIDCConfiguration.get_oidc_configuration(
                AnyHttpUrl(settings.config_url),
                strict=settings.strict,
                timeout_seconds=settings.timeout_seconds,
            )

        authorization_endpoint_value = (
            settings.authorization_endpoint
            or (str(config.authorization_endpoint) if config and config.authorization_endpoint else None)
        )
        token_endpoint_value = (
            settings.token_endpoint
            or (str(config.token_endpoint) if config and config.token_endpoint else None)
        )
        revocation_endpoint_value = (
            settings.revocation_endpoint
            or (str(config.revocation_endpoint) if config and config.revocation_endpoint else None)
        )
        jwks_uri_value = (
            settings.jwks_uri
            or (str(config.jwks_uri) if config and config.jwks_uri else None)
        )
        issuer_value = (
            settings.issuer
            or (str(config.issuer) if config and config.issuer else None)
        )

        missing = []
        if not authorization_endpoint_value:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_AUTHORIZATION_ENDPOINT")
        if not token_endpoint_value:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_TOKEN_ENDPOINT")
        if not jwks_uri_value and not settings.jwt_public_key:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_JWKS_URI or FASTMCP_SERVER_AUTH_OIDC_JWT_PUBLIC_KEY")
        if not issuer_value:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_ISSUER")
        if not settings.client_id:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_CLIENT_ID")
        if not settings.client_secret:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_CLIENT_SECRET")
        if not settings.base_url:
            missing.append("FASTMCP_SERVER_AUTH_OIDC_BASE_URL")

        if missing:
            raise ValueError(
                "Missing required OIDC proxy configuration: "
                + ", ".join(missing)
            )

        if settings.jwt_public_key:
            jwt_key = settings.jwt_public_key.get_secret_value()
            token_verifier = JWTVerifier(
                public_key=jwt_key,
                algorithm=settings.jwt_algorithm,
                issuer=issuer_value,
                audience=settings.audience,
                required_scopes=settings.required_scopes,
            )
        else:
            token_verifier = JWTVerifier(
                jwks_uri=jwks_uri_value,
                algorithm=settings.jwt_algorithm,
                issuer=issuer_value,
                audience=settings.audience,
                required_scopes=settings.required_scopes,
            )

        jwt_signing_key_value = (
            settings.jwt_signing_key.get_secret_value()
            if settings.jwt_signing_key
            else None
        )

        valid_scopes_value = settings.valid_scopes
        if valid_scopes_value is None and config and config.scopes_supported:
            valid_scopes_value = [str(s) for s in config.scopes_supported]

        super().__init__(
            upstream_authorization_endpoint=authorization_endpoint_value,
            upstream_token_endpoint=token_endpoint_value,
            upstream_client_id=settings.client_id,
            upstream_client_secret=settings.client_secret.get_secret_value(),
            upstream_revocation_endpoint=revocation_endpoint_value,
            token_verifier=token_verifier,
            base_url=settings.base_url,
            redirect_path=settings.redirect_path,
            issuer_url=settings.issuer_url or settings.base_url,
            allowed_client_redirect_uris=settings.allowed_client_redirect_uris,
            valid_scopes=valid_scopes_value,
            forward_pkce=settings.forward_pkce,
            token_endpoint_auth_method=settings.token_endpoint_auth_method,
            extra_authorize_params=_stringify_dict(settings.extra_authorize_params),
            extra_token_params=_stringify_dict(settings.extra_token_params),
            jwt_signing_key=jwt_signing_key_value,
            require_authorization_consent=settings.require_authorization_consent,
            fallback_access_token_expiry_seconds=settings.fallback_access_token_expiry_seconds,
        )
