from __future__ import annotations

import os

import pytest
from tpl.auth import get_auth_for_host


def test_get_auth_for_github_prefers_tpl_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TPL_GITHUB_TOKEN", "secret")
    if "GITHUB_TOKEN" in os.environ:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    auth = get_auth_for_host("github")

    assert auth is not None
    assert auth.username == "x-access-token"
    assert auth.password == "secret"


def test_get_auth_for_bitbucket_requires_username_and_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TPL_BITBUCKET_USERNAME", "user")
    monkeypatch.setenv("TPL_BITBUCKET_APP_PASSWORD", "pass123")

    auth = get_auth_for_host("bitbucket")

    assert auth is not None
    assert auth.username == "user"
    assert auth.password == "pass123"


def test_get_auth_for_missing_env_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TPL_GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    assert get_auth_for_host("github") is None
