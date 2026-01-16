"""Application configuration loaded from environment variables."""

import logging
from functools import lru_cache
from typing import ClassVar, Literal

from pydantic_settings import BaseSettings

LogLevels = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LOGGER = logging.getLogger("zen_auth")


class ZenAuthConfig(BaseSettings):
    """ZenAuth settings.

    Values are loaded from env vars prefixed with `ZENAUTH_` and an optional `.env` file.

    Note: In container environments, configuration is typically provided via
    environment variables / injected secrets, so `.env` is usually unnecessary.
    """

    _ENV_PREFIX: ClassVar[str] = "ZENAUTH_"

    model_config = dict(env_prefix=_ENV_PREFIX, env_file=".env", extra="allow")
    samesite: Literal["lax", "none", "strict"] = "lax"
    secure: bool = False

    auth_server_origin: str = ""

    def safe_dict(self) -> dict[str, object]:
        """Return a redacted representation safe for logs/diagnostics."""

        data: dict[str, object] = self.model_dump()
        for key in ("secret_key",):
            if data.get(key) is not None:
                data[key] = "***REDACTED***"
        return data

    def model_post_init(self, context: object) -> None:
        # NOTE:
        # The core library is used both by WebApps and by the ZenAuth server.
        # WebApps may rely on remote token verification and therefore do not
        # need access to the JWT signing key.
        #
        # The ZenAuth server must still ensure ZENAUTH_SERVER_SECRET_KEY is set.
        # (See server-side config validation.)

        # Avoid logging secrets. Use safe_dict() if needed.
        LOGGER.debug("ZenAuthConfig loaded (redacted): %s", self.safe_dict())


@lru_cache
def ZENAUTH_CONFIG() -> ZenAuthConfig:
    return ZenAuthConfig()
