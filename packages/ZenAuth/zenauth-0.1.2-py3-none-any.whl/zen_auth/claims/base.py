import datetime as DT
import json
from functools import lru_cache
from typing import Any, Callable, ClassVar, Iterable, Literal, TypeVar
from urllib.parse import urlencode

import requests
from fastapi import Depends, Header, status
from fastapi.requests import Request
from fastapi.responses import Response
from pydantic import BaseModel, PrivateAttr
from requests import exceptions as req_exc
from typing_extensions import Self

from ..config import ZENAUTH_CONFIG
from ..dto import UserDTO, VerifyTokenDTO
from ..errors import (
    ClaimError,
    ClaimSourceError,
    ClaimValidationError,
    ConfigError,
    InvalidCredentialsError,
    InvalidTokenError,
    MissingRequiredRolesError,
    MissingRequiredRolesOrScopesError,
    MissingRequiredScopesError,
    UserVerificationError,
)
from ..logger import AUDIT_LOGGER, LOGGER

TokenType = Literal["access"]

_RespT = TypeVar("_RespT", bound=Response)


# Define common error messages
ERROR_UNKNOWN = "An unknown error occurred."


def _as_dict(value: object, *, message: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ClaimSourceError(message, code="invalid_data")
    return value


def _extract_bool_field(data: dict[str, object], field: str, *, message: str) -> bool:
    value = data.get(field)
    if not isinstance(value, bool):
        raise ClaimSourceError(message, code="invalid_data")
    return value


def _build_role_or_scope_dep(
    cls: type["Claims"],
    guard: Callable[..., UserDTO],
    role_list: list[str],
    scope_list: list[str],
    *,
    role_url: str | None,
    scope_url: str | None,
    role_or_scope_url: str | None = None,
) -> Callable[..., UserDTO]:
    def dep(req: Request, user: UserDTO = Depends(guard)) -> UserDTO:
        return cls._role_or_scope_check(
            req,
            user,
            role_list=role_list,
            scope_list=scope_list,
            role_url=role_url,
            scope_url=scope_url,
            role_or_scope_url=role_or_scope_url,
        )

    return dep


def log_audit_success(
    msg: str,
    user_name: str,
    roles: Iterable[str] | None = None,
    required_context: object = None,
    request: Request | None = None,
) -> None:
    """Write a success entry to the audit logger.

    Args:
        msg: Human readable message.
        user_name: The username associated with the event.
        roles: The user's roles if available.
        required_context: Context for the operation (roles, scopes, etc).
        request: Optional Request object for additional context.
    """

    AUDIT_LOGGER.info(
        msg,
        extra={
            "user_name": user_name,
            "roles": roles,
            "result": "success",
            "required_context": required_context,
            "request": request,
        },
    )


def log_audit_fail(
    msg: str,
    user_name: str,
    roles: Iterable[str] | None = None,
    required_context: object = None,
    request: Request | None = None,
) -> None:
    """Write a failure entry to the audit logger.

    Args:
        msg: Human readable message.
        user_name: The username associated with the event.
        roles: The user's roles if available.
        required_context: Context for the operation (roles, scopes, etc).
        request: Optional Request object for additional context.
    """

    AUDIT_LOGGER.info(
        msg,
        extra={
            "user_name": user_name,
            "roles": roles,
            "result": "failure",
            "required_context": required_context,
            "request": request,
        },
    )


class Claims(BaseModel):
    """JWT claims model with helper utilities.

    This model also provides FastAPI dependencies (`guard`, `role`, `scope`) for
    validating tokens and enforcing authorization.
    """

    class TokenDTO(BaseModel):
        token: str

    class UserPassDTO(BaseModel):
        user_name: str
        password: str

    _GET: ClassVar[Callable[..., requests.Response]] = requests.get
    _POST: ClassVar[Callable[..., requests.Response]] = requests.post

    typ: TokenType
    sub: str
    policy_epoch: int
    iat: int
    exp: int

    _auth_user: UserDTO | None = PrivateAttr(default=None)

    @property
    def username(self) -> str:
        """Return the subject (username) from the claims."""
        return self.sub

    # NOTE: JWT encode/decode helpers are intentionally server-only.
    # WebApps should authenticate by calling the auth-server verification APIs.

    @classmethod
    def _gen_url(cls, path: str) -> str:
        # If an auth-server origin is configured, generate URLs against it.
        # This avoids assuming the auth server shares the same host as the
        # incoming request (common in microservice deployments).
        origin = ZENAUTH_CONFIG().auth_server_origin
        if origin is None or not origin.strip():
            raise ConfigError("ZENAUTH_AUTH_SERVER_ORIGIN must be set")

        origin = origin.rstrip("/")
        return f"{origin}/{path.lstrip('/')}"

    @classmethod
    def login_page_url(
        cls,
        req: Request,
        *,
        app_id: str | None = None,
        title: str | None = None,
    ) -> str:
        """Build the auth-server login page URL.

        This is a convenience helper for WebApps that want to redirect users to
        the ZenAuth login UI.

        The resulting URL points to the auth server's login page endpoint.

        For security (open redirect prevention), the login page does not accept
        a user-controlled return destination URL. Instead, pass `app_id` and
        let the auth server resolve the post-login destination.
        """

        base = cls._endpoint_url(req, "login_page")
        params: dict[str, str] = {}
        if app_id is not None:
            params["app_id"] = app_id
        if title is not None:
            params["title"] = title
        qs = urlencode(params)
        return f"{base}?{qs}" if qs else base

    @classmethod
    def _endpoints_discovery_url(cls) -> str:
        # Server-side discovery endpoint.
        # (Default path: `/zen_auth/v1/meta/endpoints`)
        return cls._gen_url("/zen_auth/v1/meta/endpoints")

    @staticmethod
    @lru_cache(maxsize=32)
    def _cached_discovered_endpoints_items(discovery_url: str) -> tuple[tuple[str, str], ...]:
        """Discover auth-server endpoints and memoize the result.

        Note:
            The returned value is immutable to prevent accidental mutation of
            the memoized cache.
        """

        try:
            res = Claims._GET(discovery_url, timeout=3.0)
        except req_exc.Timeout as e:
            raise ClaimSourceError("Auth server timeout", code="timeout") from e
        except req_exc.ConnectionError as e:
            raise ClaimSourceError("Auth server connection error", code="connection") from e
        except Exception as e:
            raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e

        if res.status_code != status.HTTP_200_OK:
            raise ClaimSourceError(
                "Auth server returned non-200 for endpoints discovery",
                code="invalid_data",
                info={"status_code": res.status_code, "url": discovery_url},
            )

        try:
            payload = res.json()
        except Exception as e:
            raise ClaimSourceError("Auth server returned invalid data", code="invalid_data") from e

        if not isinstance(payload, dict):
            raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")

        discovered: dict[str, str] = {}
        for k, v in data.items():
            if isinstance(k, str) and isinstance(v, str) and v.strip():
                discovered[k] = v

        required = {"verify_token", "verify_user", "verify_user_role", "verify_user_scope"}
        missing = sorted(required.difference(discovered.keys()))
        if missing:
            raise ClaimSourceError(
                "Auth server returned incomplete endpoints data",
                code="invalid_data",
                info={"missing": missing},
            )

        return tuple(sorted(discovered.items()))

    @classmethod
    def _get_cached_endpoints(cls) -> dict[str, str]:
        """Return cached endpoint URLs discovered from the auth server.

        The discovery call is memoized process-wide.
        """

        discovery_url = cls._endpoints_discovery_url()
        return dict(cls._cached_discovered_endpoints_items(discovery_url))

    @classmethod
    def _endpoint_url(cls, req: Request, key: str) -> str:
        endpoints = cls._get_cached_endpoints()
        url = endpoints.get(key)
        if url is None:
            raise ClaimSourceError(
                "Auth server discovery missing endpoint",
                code="invalid_data",
                info={"key": key},
            )
        return url

    @classmethod
    def _access_token_cookie_name(cls) -> str:
        meta_url = cls._gen_url("/zen_auth/v1/meta/access_token")
        cookie_name, _expire_min = cls._cached_access_token_cookie_meta(meta_url)
        return cookie_name

    @classmethod
    def _access_token_cookie_max_age(cls) -> int:
        meta_url = cls._gen_url("/zen_auth/v1/meta/access_token")
        _cookie_name, expire_min = cls._cached_access_token_cookie_meta(meta_url)
        return int(expire_min) * 60

    @staticmethod
    @lru_cache(maxsize=32)
    def _cached_access_token_cookie_meta(meta_url: str) -> tuple[str, int]:
        """Fetch and memoize access-token cookie metadata.

        The core library does not accept local overrides for these values.
        WebApps must be able to reach the auth server's public metadata endpoint.
        """

        try:
            res = Claims._GET(meta_url, timeout=1.0)
        except requests.Timeout as e:
            raise ClaimSourceError(
                "Auth server metadata request timed out",
                code="timeout",
                info={"url": meta_url},
            ) from e
        except requests.ConnectionError as e:
            raise ClaimSourceError(
                "Auth server metadata connection error",
                code="connection",
                info={"url": meta_url},
            ) from e
        except Exception as e:
            raise ClaimSourceError(
                "Auth server metadata request failed",
                code=ERROR_UNKNOWN,
                info={"url": meta_url},
            ) from e

        if res.status_code != status.HTTP_200_OK:
            raise ClaimSourceError(
                "Auth server metadata unavailable",
                code="unavailable",
                info={"url": meta_url, "status_code": res.status_code, "text": res.text},
            )

        res_dict = _as_dict(res.json(), message="Auth server returned invalid data")
        data = _as_dict(res_dict.get("data"), message="Auth server returned invalid data")
        name_val = data.get("access_token_cookie_name")
        expire_val = data.get("access_token_expire_min")

        cookie_name = name_val.strip() if isinstance(name_val, str) else ""
        expire_min = expire_val if isinstance(expire_val, int) else None

        if cookie_name and isinstance(expire_min, int) and expire_min > 0:
            return cookie_name, expire_min

        raise ClaimSourceError(
            "Auth server returned invalid data",
            code="invalid_data",
            info={
                "url": meta_url,
                "fields": ["access_token_cookie_name", "access_token_expire_min"],
            },
        )

    @classmethod
    def _get_token(cls, req: Request, authorization: str | None) -> str | None:
        return req.cookies.get(cls._access_token_cookie_name()) or _extract_bearer(authorization)

    @classmethod
    def _validate_claims(cls, claims: Self) -> None:
        if claims.typ != "access":
            raise ClaimValidationError("Wrong jwt type")

        checks = {"sub": str, "exp": int, "policy_epoch": int, "iat": int}

        for field, typ in checks.items():
            if not isinstance(getattr(claims, field), typ):
                raise ClaimValidationError(
                    f"Invalid jwt payload: {field} must be {typ.__name__}", field=field
                )

    @classmethod
    def clear_cookie(cls, resp: "_RespT") -> "_RespT":
        """Delete the auth cookie from the response and return it."""
        resp.delete_cookie(cls._access_token_cookie_name(), path="/")
        return resp

    @classmethod
    def set_cookie(cls, resp: "_RespT", token: str) -> "_RespT":
        """Set the auth cookie on the response and return it."""

        resp.set_cookie(
            key=cls._access_token_cookie_name(),
            value=token,
            httponly=True,
            secure=ZENAUTH_CONFIG().secure,
            samesite=ZENAUTH_CONFIG().samesite,
            max_age=cls._access_token_cookie_max_age(),
            path="/",
        )
        return resp

    @staticmethod
    def logout(response: Response) -> None:
        """Convenience alias for `clear_cookie`."""
        Claims.clear_cookie(response)

    @classmethod
    def role(
        cls,
        *required_roles: str,
        **kwargs: Any,
    ) -> Callable[..., UserDTO]:
        """FastAPI dependency that enforces required roles.

        The user must have at least one of the specified roles (OR).

        Optional kwargs:
            url: Override `/verify/token` endpoint URL.
            role_url / rbac_url: Override `/verify/user/role` endpoint URL.
        """
        token_url = kwargs.get("url", None)
        role_url = kwargs.get("role_url", None) or kwargs.get("rbac_url", None)
        guard = cls.guard(url=token_url)

        def _verify_roles(req: Request, user_name: str) -> bool:
            nonlocal role_url
            if role_url is None:
                role_url = cls._endpoint_url(
                    req,
                    "verify_user_role",
                )

            roles = [r for r in required_roles if r]
            res = cls._POST(
                role_url,
                timeout=3.0,
                json={"user_name": user_name, "required_roles": roles},
            )
            if res.status_code == status.HTTP_403_FORBIDDEN:
                return False
            if res.status_code != status.HTTP_200_OK:
                raise ClaimSourceError(
                    "Auth server returned non-200 for role verify",
                    code="invalid_data",
                    info={"status_code": res.status_code},
                )

            res_dict: dict[str, object] = res.json()
            data = res_dict.get("data")
            if not isinstance(data, dict):
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")
            has_role = data.get("has_role")
            if not isinstance(has_role, bool):
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")
            return has_role

        def dep(req: Request, user: UserDTO = Depends(guard)) -> UserDTO:
            roles = [r for r in required_roles if r]
            if not roles:
                log_audit_fail(
                    "Role check failed.", user.user_name, user.roles, required_context=roles, request=req
                )
                raise MissingRequiredRolesError(
                    f"Role check failed. (user: {user.user_name})",
                    user_name=user.user_name,
                    roles=set(user.roles),
                    required=roles,
                )

            try:
                if _verify_roles(req, user.user_name):
                    return user

                log_audit_fail(
                    "Role check failed.", user.user_name, user.roles, required_context=roles, request=req
                )
                raise MissingRequiredRolesError(
                    f"Role check failed. (user: {user.user_name})",
                    user_name=user.user_name,
                    roles=set(user.roles),
                    required=roles,
                )
            except ClaimError:
                raise
            except req_exc.Timeout as e:
                raise ClaimSourceError("Auth server timeout", code="timeout") from e
            except req_exc.ConnectionError as e:
                raise ClaimSourceError("Auth server connection error", code="connection") from e
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data") from e
            except Exception as e:
                LOGGER.error(ERROR_UNKNOWN, exc_info=e)
                raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e

        return dep

    @classmethod
    def scope(
        cls,
        *required_scopes: str,
        **kwargs: Any,
    ) -> Callable[..., UserDTO]:
        """FastAPI dependency that enforces required scopes.

        The user must have at least one of the specified scopes (OR).

        Optional kwargs:
            url: Override `/verify/token` endpoint URL.
            scope_url: Override `/verify/user/scope` endpoint URL.
        """
        token_url = kwargs.get("url", None)
        scope_url = kwargs.get("scope_url", None)
        guard = cls.guard(url=token_url)

        def _user_allowed_any_scope(req: Request, user_name: str) -> bool:
            nonlocal scope_url
            if scope_url is None:
                scope_url = cls._endpoint_url(
                    req,
                    "verify_user_scope",
                )

            scopes = [s for s in required_scopes if s]
            res = cls._POST(
                scope_url,
                timeout=3.0,
                json={"user_name": user_name, "required_scopes": scopes},
            )
            if res.status_code == status.HTTP_403_FORBIDDEN:
                return False
            if res.status_code != status.HTTP_200_OK:
                raise ClaimSourceError(
                    "Auth server returned non-200 for scope verify",
                    code="invalid_data",
                    info={"status_code": res.status_code},
                )

            res_dict: dict[str, object] = res.json()
            data = res_dict.get("data")
            if not isinstance(data, dict):
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")
            allowed = data.get("allowed")
            if not isinstance(allowed, bool):
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data")
            return allowed

        def dep(req: Request, user: UserDTO = Depends(guard)) -> UserDTO:
            scopes = [s for s in required_scopes if s]
            if not scopes:
                log_audit_fail(
                    "Scope check failed.", user.user_name, user.roles, required_context=scopes, request=req
                )
                raise MissingRequiredScopesError(
                    f"Scope check failed. (user: {user.user_name})",
                    user_name=user.user_name,
                    roles=set(user.roles),
                    required=scopes,
                )

            try:
                if _user_allowed_any_scope(req, user.user_name):
                    return user

                log_audit_fail(
                    "Scope check failed.", user.user_name, user.roles, required_context=scopes, request=req
                )
                raise MissingRequiredScopesError(
                    f"Scope check failed. (user: {user.user_name})",
                    user_name=user.user_name,
                    roles=set(user.roles),
                    required=scopes,
                )
            except ClaimError:
                raise
            except req_exc.Timeout as e:
                raise ClaimSourceError("Auth server timeout", code="timeout") from e
            except req_exc.ConnectionError as e:
                raise ClaimSourceError("Auth server connection error", code="connection") from e
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                raise ClaimSourceError("Auth server returned invalid data", code="invalid_data") from e
            except Exception as e:
                LOGGER.error(ERROR_UNKNOWN, exc_info=e)
                raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e

        return dep

    @classmethod
    def role_or_scope(
        cls,
        *,
        roles: Iterable[str] = (),
        scopes: Iterable[str] = (),
        **kwargs: Any,
    ) -> Callable[..., UserDTO]:
        """FastAPI dependency that allows access if either role OR scope matches.

        This is useful when you want a single dependency for endpoints that can
        be accessed by either privileged roles or specific scopes.

        Args:
            roles: Allowed roles (any-of).
            scopes: Allowed scopes (any-of).
        """

        role_list = [r for r in roles if r]
        scope_list = [s for s in scopes if s]

        token_url = kwargs.get("url", None)
        role_url = kwargs.get("role_url", None) or kwargs.get("rbac_url", None)
        scope_url = kwargs.get("scope_url", None)
        role_or_scope_url = kwargs.get("role_or_scope_url", None)
        guard = cls.guard(url=token_url)

        return _build_role_or_scope_dep(
            cls,
            guard,
            role_list,
            scope_list,
            role_url=role_url,
            scope_url=scope_url,
            role_or_scope_url=role_or_scope_url,
        )

    @classmethod
    def _verify_user_roles_any(
        cls,
        req: Request,
        user_name: str,
        role_list: list[str],
        *,
        role_url: str | None,
    ) -> bool:
        if not role_list:
            return False

        url = role_url or cls._endpoint_url(req, "verify_user_role")
        res = cls._POST(url, timeout=3.0, json={"user_name": user_name, "required_roles": role_list})
        if res.status_code == status.HTTP_403_FORBIDDEN:
            return False
        if res.status_code != status.HTTP_200_OK:
            raise ClaimSourceError(
                "Auth server returned non-200 for role verify",
                code="invalid_data",
                info={"status_code": res.status_code},
            )

        res_dict = _as_dict(res.json(), message="Auth server returned invalid data")
        data = _as_dict(res_dict.get("data"), message="Auth server returned invalid data")
        return _extract_bool_field(data, "has_role", message="Auth server returned invalid data")

    @classmethod
    def _verify_user_scopes_any(
        cls,
        req: Request,
        user_name: str,
        scope_list: list[str],
        *,
        scope_url: str | None,
    ) -> bool:
        if not scope_list:
            return False

        url = scope_url or cls._endpoint_url(req, "verify_user_scope")
        res = cls._POST(url, timeout=3.0, json={"user_name": user_name, "required_scopes": scope_list})
        if res.status_code == status.HTTP_403_FORBIDDEN:
            return False
        if res.status_code != status.HTTP_200_OK:
            raise ClaimSourceError(
                "Auth server returned non-200 for scope verify",
                code="invalid_data",
                info={"status_code": res.status_code},
            )

        res_dict = _as_dict(res.json(), message="Auth server returned invalid data")
        data = _as_dict(res_dict.get("data"), message="Auth server returned invalid data")
        return _extract_bool_field(data, "allowed", message="Auth server returned invalid data")

    @classmethod
    def _role_or_scope_check(
        cls,
        req: Request,
        user: UserDTO,
        *,
        role_list: list[str],
        scope_list: list[str],
        role_url: str | None,
        scope_url: str | None,
        role_or_scope_url: str | None,
    ) -> UserDTO:
        if not role_list and not scope_list:
            raise MissingRequiredRolesOrScopesError(
                f"Role/scope check failed. (user: {user.user_name})",
                user_name=user.user_name,
                roles=set(user.roles),
                required_roles=role_list,
                required_scopes=scope_list,
            )

        try:
            combined_url = role_or_scope_url
            if combined_url is None:
                endpoints = cls._get_cached_endpoints()
                combined_url = endpoints.get("verify_user_role_or_scope")

            if combined_url:
                res = cls._POST(
                    combined_url,
                    timeout=3.0,
                    json={
                        "user_name": user.user_name,
                        "required_roles": role_list,
                        "required_scopes": scope_list,
                    },
                )
                if res.status_code == status.HTTP_200_OK:
                    has_access = True
                elif res.status_code == status.HTTP_403_FORBIDDEN:
                    has_access = False
                else:
                    raise ClaimSourceError(
                        "Auth server returned unexpected status for role_or_scope verify",
                        code="invalid_data",
                        info={"status_code": res.status_code},
                    )
            else:
                has_access = cls._verify_user_roles_any(
                    req, user.user_name, role_list, role_url=role_url
                ) or cls._verify_user_scopes_any(req, user.user_name, scope_list, scope_url=scope_url)

            if has_access:
                log_audit_success(
                    "Role/scope check success.",
                    user.user_name,
                    user.roles,
                    required_context={"roles": role_list, "scopes": scope_list},
                    request=req,
                )
                return user

            log_audit_fail(
                "Role/scope check failed.",
                user.user_name,
                user.roles,
                required_context={"roles": role_list, "scopes": scope_list},
                request=req,
            )
            raise MissingRequiredRolesOrScopesError(
                f"Role/scope check failed. (user: {user.user_name})",
                user_name=user.user_name,
                roles=set(user.roles),
                required_roles=role_list,
                required_scopes=scope_list,
            )
        except ClaimError:
            raise
        except req_exc.Timeout as e:
            raise ClaimSourceError("Auth server timeout", code="timeout") from e
        except req_exc.ConnectionError as e:
            raise ClaimSourceError("Auth server connection error", code="connection") from e
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            raise ClaimSourceError("Auth server returned invalid data", code="invalid_data") from e
        except Exception as e:
            LOGGER.error(ERROR_UNKNOWN, exc_info=e)
            raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e

    @classmethod
    def guard(cls, **kwargs: Any) -> Callable[..., UserDTO]:
        """FastAPI dependency that authenticates a request.

        By default this calls the configured `/verify/token` endpoint, refreshes
        the cookie, and returns an authenticated `UserDTO`.

        Optional kwargs:
            url: Override the `/verify/token` endpoint URL.
        """
        url = kwargs.get("url", None)

        def dep(
            req: Request,
            resp: Response,
            authorization: str | None = Header(default=None),
        ) -> UserDTO:
            nonlocal url
            user_name: str = "--"
            try:
                if url is None:
                    url = cls._endpoint_url(
                        req,
                        "verify_token",
                    )

                token = cls._get_token(req, authorization)
                if not token:
                    raise InvalidTokenError("No token.", kind="no_token")

                # Remote verification: do not decode/verify the JWT locally.
                # This avoids requiring the signing key in WebApps.

                res = cls._POST(url, timeout=3.0, json={"token": token})
                if res.status_code != status.HTTP_200_OK:
                    raise InvalidTokenError(f"Invalid token. (user: {user_name})", user_name=user_name)

                res_dict: dict[str, object] = res.json()
                res_dto = VerifyTokenDTO.model_validate(res_dict["data"])

                cls.set_cookie(resp, res_dto.token)
                return res_dto.user
            except ClaimError:
                raise
            except req_exc.Timeout as e:
                raise ClaimSourceError("Auth server timeout", code="timeout") from e
            except req_exc.ConnectionError as e:
                raise ClaimSourceError("Auth server connection error", code="connection") from e
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                resp_text = None
                try:
                    resp_text = res.text
                except Exception:
                    resp_text = None
                raise ClaimSourceError(
                    "Auth server returned invalid data",
                    code="invalid_data",
                    info={"body": resp_text},
                ) from e
            except Exception as e:
                LOGGER.error(ERROR_UNKNOWN, exc_info=e)
                raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e

        return dep

    @classmethod
    def verify_user(
        cls,
        req: Request,
        resp: Response,
        user_name: str,
        password: str,
        **kwargs: Any,
        # url: str | None = None,
    ) -> Response:
        """Verify username/password via the `/verify/user` endpoint.

        On success, sets the auth cookie on `resp` and returns it.

        Optional kwargs:
            url: Override the `/verify/user` endpoint URL.
        """
        url = kwargs.get("url", None)
        try:
            if url is None:
                url = cls._endpoint_url(
                    req,
                    "verify_user",
                )

            res = cls._POST(url, timeout=3.0, json=dict(user_name=user_name, password=password))
            if res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                msg = f"Auth server internal error during user verification. (user: {user_name})"
                LOGGER.critical(msg)
                raise ClaimSourceError(msg, code="internal", info={"status_code": res.status_code})
            if res.status_code != status.HTTP_200_OK:
                raise InvalidCredentialsError(
                    f"Invalid user or password. (user: {user_name})",
                    user_name=user_name,
                    info={"user": user_name},
                )
            res_dict: dict[str, object] = res.json()
            res_dto = Claims.TokenDTO.model_validate(res_dict["data"])
            return cls.set_cookie(resp, res_dto.token)
        except UserVerificationError as e:
            raise InvalidCredentialsError(
                f"Invalid user or password. (user: {user_name})",
                user_name=user_name,
                info={"user": user_name},
            ) from e
        except req_exc.Timeout as e:
            raise ClaimSourceError("Auth server timeout", code="timeout") from e
        except req_exc.ConnectionError as e:
            raise ClaimSourceError("Auth server connection error", code="connection") from e
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            resp_text = None
            try:
                resp_text = res.text
            except Exception:
                resp_text = None
            raise ClaimSourceError(
                "Auth server returned invalid data",
                code="invalid_data",
                info={"body": resp_text},
            ) from e
        except Exception as e:
            LOGGER.error(ERROR_UNKNOWN, exc_info=e)
            raise ClaimSourceError(ERROR_UNKNOWN, code="internal") from e


def _utcnow() -> DT.datetime:
    return DT.datetime.now(DT.timezone.utc)


def _extract_bearer(v: str | None) -> str | None:
    if not v:
        return None
    try:
        scheme, token = v.strip().split(" ", 1)
    except ValueError:
        return None
    return token if scheme.lower() == "bearer" and token else None
