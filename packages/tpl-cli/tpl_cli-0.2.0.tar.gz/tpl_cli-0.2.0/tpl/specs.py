from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from .errors import TPLError


class SpecParseError(TPLError):
    """Raised when repo specifications are invalid."""


@dataclass(frozen=True)
class HostInfo:
    alias: str
    domain: Optional[str]
    auth_key: Optional[str]
    kind: str


HOSTS: dict[str, HostInfo] = {
    "gh": HostInfo(alias="gh", domain="github.com", auth_key="github", kind="remote"),
    "bb": HostInfo(alias="bb", domain="bitbucket.org", auth_key="bitbucket", kind="remote"),
    "local": HostInfo(alias="local", domain=None, auth_key=None, kind="local"),
}

HOST_ALIASES: dict[str, str] = {
    "gh": "gh",
    "github": "gh",
    "bb": "bb",
    "bitbucket": "bb",
    "local": "local",
    "file": "local",
    "path": "local",
}


@dataclass(frozen=True)
class RepoSpec:
    host: str
    owner: Optional[str]
    repo: Optional[str]
    version: Optional[str] = None
    local_path: Optional[str] = None

    @classmethod
    def parse(
        cls,
        text: str,
        *,
        default_version: Optional[str] = None,
        require_version: bool = True,
    ) -> "RepoSpec":
        """Parse a repo-spec of the form host:owner/name@version.

        Supports `gh:`, `bb:`, and `local:` prefixes. Local specs resolve to an
        absolute path, and can omit the version when `require_version` is False.
        """

        if ":" not in text:
            raise SpecParseError("Repo spec must include host prefix, e.g., gh:user/repo@v1.0.0")

        host, remainder = text.split(":", 1)
        host_info = _resolve_host(host)

        if host_info.kind == "local":
            path_segment, specified_version = cls._split_repo_version(remainder)
            if not path_segment:
                raise SpecParseError(
                    "Local repo spec must include a path, e.g., local:../tpl@v1.0.0"
                )
            resolved = str(Path(path_segment).expanduser().resolve())
            version = specified_version or default_version
            if require_version and not version:
                raise SpecParseError("Repo spec must include a version (use @<tag>)")
            return cls(
                host=host_info.alias,
                owner=None,
                repo=None,
                version=version,
                local_path=resolved,
            )

        if "/" not in remainder:
            raise SpecParseError("Repo spec must include owner and repo, e.g., gh:user/repo@v1.0.0")

        owner, repo_segment = remainder.split("/", 1)

        repo_name, specified_version = cls._split_repo_version(repo_segment)
        version = specified_version or default_version

        if require_version and not version:
            raise SpecParseError("Repo spec must include a version (use @<tag>)")

        return cls(host=host_info.alias, owner=owner, repo=repo_name, version=version)

    @staticmethod
    def _split_repo_version(repo_segment: str) -> Tuple[str, Optional[str]]:
        if "@" not in repo_segment:
            return repo_segment, None
        repo_name, version = repo_segment.split("@", 1)
        return repo_name, version

    def require_version(self) -> str:
        """Return the version string or raise if missing."""
        if not self.version:
            raise SpecParseError("A version is required for this operation")
        return self.version

    def without_version(self) -> str:
        if self.local_path:
            return f"{self.host}:{self.local_path}"
        return f"{self.host}:{self.owner}/{self.repo}"

    def with_version(self, version: str) -> "RepoSpec":
        return RepoSpec(
            host=self.host,
            owner=self.owner,
            repo=self.repo,
            version=version,
            local_path=self.local_path,
        )

    def git_url(self) -> str:
        """Return a git URL or local path that can be passed to git."""
        if self.local_path:
            return self.local_path
        info = self._host_info()
        if not info.domain:
            raise SpecParseError(f"Host '{self.host}' does not support remote URLs")
        return f"https://{info.domain}/{self.owner}/{self.repo}.git"

    def auth_key(self) -> Optional[str]:
        return self._host_info().auth_key

    def cache_key(self) -> str:
        """Return a filesystem-safe cache key for the repo/version tuple."""
        version = self.require_version()
        safe_host = self.host.replace(":", "_")
        if self.local_path:
            safe_path = self.local_path.replace(os.sep, "_").replace(":", "")
            return f"{safe_host}_{safe_path}_{version}"
        return f"{safe_host}_{self.owner}_{self.repo}_{version}"

    def display(self) -> str:
        """Return a user-facing spec string, with version when present."""
        if self.version:
            return f"{self.without_version()}@{self.version}"
        return self.without_version()

    def _host_info(self) -> HostInfo:
        if self.host in HOSTS:
            return HOSTS[self.host]
        return _resolve_host(self.host)


def _resolve_host(label: str) -> HostInfo:
    key = HOST_ALIASES.get(label.lower())
    if not key or key not in HOSTS:
        raise SpecParseError(
            f"Unsupported repo host '{label}'. Use gh:owner/repo, bb:owner/repo, or local:/path."
        )
    return HOSTS[key]
