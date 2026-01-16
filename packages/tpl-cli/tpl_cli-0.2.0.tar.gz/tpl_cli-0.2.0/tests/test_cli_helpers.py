from __future__ import annotations

import pathlib

import pytest
from tpl.cli import (
    parse_entry_pairs,
    parse_extra_context,
    resolve_requested_version,
    resolve_user_path,
    select_latest_version,
)
from tpl.errors import TPLError
from tpl.specs import RepoSpec


class DummyCache:
    def __init__(self, tags: list[str]):
        self._tags = tags

    def list_tags(self, spec: RepoSpec) -> list[str]:  # noqa: ARG002 - spec unused
        return self._tags


def test_parse_extra_context_builds_mapping() -> None:
    context = parse_extra_context(["name=tpl", "project_slug=demo"])

    assert context == {"name": "tpl", "project_slug": "demo"}


def test_parse_extra_context_validates_pairs() -> None:
    with pytest.raises(TPLError):
        parse_extra_context(["missingvalue"])


def test_parse_entry_pairs_success() -> None:
    pairs = parse_entry_pairs(["src/a.py=a.py", "docs/readme=README.md"])

    assert pairs == [("src/a.py", "a.py"), ("docs/readme", "README.md")]


def test_parse_entry_pairs_defaults_entry_when_missing() -> None:
    pairs = parse_entry_pairs(["src/settings.py"])

    assert pairs == [("src/settings.py", "settings.py")]


def test_parse_entry_pairs_error() -> None:
    with pytest.raises(TPLError):
        parse_entry_pairs(["="])


def test_select_latest_version_prefers_newer_tags() -> None:
    spec = RepoSpec.parse("gh:you/repo", require_version=False)
    cache = DummyCache(["v0.2.0", "v0.1.0"])

    next_version = select_latest_version(cache, spec, current_version="0.1.0")

    assert next_version == "v0.2.0"


def test_select_latest_version_returns_current_when_latest() -> None:
    spec = RepoSpec.parse("gh:you/repo", require_version=False)
    cache = DummyCache(["v1.0.0", "v0.9.0"])

    assert select_latest_version(cache, spec, current_version="1.0.0") == "1.0.0"


def test_resolve_requested_version_matches_variant_tags() -> None:
    spec = RepoSpec.parse("gh:you/repo", require_version=False)
    cache = DummyCache(["v1.0.0", "v0.9.0"])

    assert resolve_requested_version(cache, spec, requested="1.0.0") == "v1.0.0"


def test_resolve_requested_version_errors_for_missing_tag() -> None:
    spec = RepoSpec.parse("gh:you/repo", require_version=False)
    cache = DummyCache(["v0.5.0"])

    with pytest.raises(TPLError):
        resolve_requested_version(cache, spec, requested="1.0.0")


def test_resolve_user_path_returns_relative() -> None:
    root = pathlib.Path.cwd()
    relative, absolute = resolve_user_path("./foo/bar.txt", root)

    assert relative == "foo/bar.txt"
    assert absolute == (root / "foo/bar.txt").resolve()
