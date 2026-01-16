from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RepoAuth:
    username: str
    password: str


def get_auth_for_host(host_key: Optional[str]) -> Optional[RepoAuth]:
    """Return credentials for the given git host if configured.

    Reads environment variables per host:
    - GitHub: `TPL_GITHUB_TOKEN` or `GITHUB_TOKEN` (token-only auth).
    - Bitbucket: `TPL_BITBUCKET_USERNAME` + `TPL_BITBUCKET_APP_PASSWORD`.
    """

    if host_key == "github":
        token = os.getenv("TPL_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN")
        if token:
            return RepoAuth(username="x-access-token", password=token)

    if host_key == "bitbucket":
        username = os.getenv("TPL_BITBUCKET_USERNAME")
        password = os.getenv("TPL_BITBUCKET_APP_PASSWORD")
        if username and password:
            return RepoAuth(username=username, password=password)

    return None
