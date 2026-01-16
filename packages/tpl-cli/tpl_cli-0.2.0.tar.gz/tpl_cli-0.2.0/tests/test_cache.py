from __future__ import annotations

from pathlib import Path

from tpl.auth import RepoAuth
from tpl.cache import _cleanup_askpass, _git_env, _parse_numeric_version, _version_key


def test_parse_numeric_version_handles_numeric_and_empty() -> None:
    assert _parse_numeric_version("1.2.3") == (1, 2, 3)
    assert _parse_numeric_version("") == ()


def test_parse_numeric_version_rejects_non_numeric() -> None:
    assert _parse_numeric_version("1.2.x") is None


def test_version_key_prefers_numeric_and_orders_by_value() -> None:
    assert _version_key("v1.2.3") > _version_key("alpha")
    assert _version_key("v10.0.0") > _version_key("v2.5.0")


def test_git_env_with_auth_creates_askpass_script() -> None:
    auth = RepoAuth(username="user", password="secret")
    env, askpass_script = _git_env(auth)

    assert env["GIT_ASKPASS"] == str(askpass_script)
    assert env["TPL_ASKPASS_USERNAME"] == "user"
    assert env["TPL_ASKPASS_PASSWORD"] == "secret"
    assert askpass_script is not None
    assert Path(askpass_script).exists()

    _cleanup_askpass(askpass_script)
    assert not Path(askpass_script).exists()
