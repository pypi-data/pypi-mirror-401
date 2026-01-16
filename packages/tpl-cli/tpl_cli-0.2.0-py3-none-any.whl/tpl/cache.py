from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple, Union

from .auth import RepoAuth, get_auth_for_host
from .errors import GitError
from .specs import RepoSpec


class RepoCache:
    """Manage cached template repositories on disk."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir or Path.home() / ".tpl-cache"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def ensure_version(self, spec: RepoSpec) -> Path:
        """Ensure the requested version is cloned locally and return its path.

        Local specs return the source directory directly (when present). Remote
        specs are shallow-cloned at the requested tag into the cache directory.
        """

        if spec.local_path:
            local_path = Path(spec.local_path)
            if local_path.exists() and (spec.version == "local" or not _is_git_repo(local_path)):
                return local_path

        version = spec.require_version()
        repo_path = self.base_dir / spec.cache_key()
        if repo_path.exists():
            return repo_path

        url = spec.git_url()
        auth = get_auth_for_host(spec.auth_key())
        env, askpass_script = _git_env(auth)
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--branch",
                    version,
                    url,
                    str(repo_path),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
        except subprocess.CalledProcessError as exc:
            raise GitError(
                f"Failed to clone {spec.display()}: {exc.stderr.decode().strip()}"
            ) from exc
        finally:
            _cleanup_askpass(askpass_script)

        return repo_path

    def list_tags(self, spec: RepoSpec) -> list[str]:
        """Return all tags available for the repo (ignores cache)."""

        if spec.local_path:
            local_path = Path(spec.local_path)
            if local_path.exists() and not _is_git_repo(local_path):
                return []

        url = spec.git_url()
        auth = get_auth_for_host(spec.auth_key())
        env, askpass_script = _git_env(auth)
        try:
            result = subprocess.run(
                ["git", "ls-remote", "--tags", url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
        except subprocess.CalledProcessError as exc:
            raise GitError(
                f"Failed to list tags for {spec.display()}: {exc.stderr.strip()}"
            ) from exc
        finally:
            _cleanup_askpass(askpass_script)

        tags: set[str] = set()
        for line in result.stdout.splitlines():
            if "refs/tags/" not in line:
                continue
            _, ref = line.split("\t", 1)
            tag = ref.split("refs/tags/", 1)[1]
            if tag.endswith("^{}"):
                tag = tag[:-3]
            tags.add(tag)

        return sorted(tags, key=_version_key, reverse=True)


def _version_key(tag: str) -> Tuple[int, Union[Tuple[int, ...], Tuple[()]], str]:
    normalized = tag.lstrip("vV")
    numeric = _parse_numeric_version(normalized)
    if numeric is not None:
        return (1, numeric, normalized)
    return (0, (), normalized)


def _parse_numeric_version(value: str) -> Optional[Tuple[int, ...]]:
    parts = value.split(".") if value else []
    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return None


def _is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def _git_env(auth: Optional[RepoAuth]) -> Tuple[dict[str, str], Optional[Path]]:
    """Build an env dict for git, optionally wiring a temp GIT_ASKPASS script."""
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    if auth is None:
        return env, None

    temp_dir = Path(tempfile.mkdtemp(prefix="tpl-askpass-"))
    script_path = temp_dir / "askpass.sh"
    script_path.write_text(
        """#!/bin/sh
case "$1" in
    *Username* ) printf '%s' "$TPL_ASKPASS_USERNAME" ;;
    *Password* ) printf '%s' "$TPL_ASKPASS_PASSWORD" ;;
    * ) printf '%s' "$TPL_ASKPASS_PASSWORD" ;;
esac
""",
        encoding="utf-8",
    )
    os.chmod(script_path, 0o700)
    env["GIT_ASKPASS"] = str(script_path)
    env["TPL_ASKPASS_USERNAME"] = auth.username
    env["TPL_ASKPASS_PASSWORD"] = auth.password
    return env, script_path


def _cleanup_askpass(script_path: Optional[Path]) -> None:
    if not script_path:
        return
    try:
        script_path.unlink()
    finally:
        try:
            script_path.parent.rmdir()
        except OSError:
            pass
