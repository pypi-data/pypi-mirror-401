from __future__ import annotations

import pytest
from tpl.specs import RepoSpec, SpecParseError


def test_repo_spec_parse_success() -> None:
    spec = RepoSpec.parse("gh:you/tpl-example@v1.2.3")

    assert spec.host == "gh"
    assert spec.owner == "you"
    assert spec.repo == "tpl-example"
    assert spec.version == "v1.2.3"
    assert spec.git_url() == "https://github.com/you/tpl-example.git"


def test_repo_spec_missing_version_errors() -> None:
    with pytest.raises(SpecParseError):
        RepoSpec.parse("gh:you/tpl-example")


def test_repo_spec_without_version_round_trip() -> None:
    spec = RepoSpec.parse("gh:you/tpl-example@v0.1.0")

    assert spec.without_version() == "gh:you/tpl-example"
    assert spec.cache_key() == "gh_you_tpl-example_v0.1.0"


def test_repo_spec_supports_full_github_host() -> None:
    spec = RepoSpec.parse("github:team/proj@1")

    assert spec.host == "gh"
    assert spec.git_url() == "https://github.com/team/proj.git"


def test_repo_spec_supports_bitbucket_aliases() -> None:
    spec = RepoSpec.parse("bitbucket:team/proj@1.0.0")

    assert spec.host == "bb"
    assert spec.git_url() == "https://bitbucket.org/team/proj.git"


def test_repo_spec_requires_known_hosts() -> None:
    with pytest.raises(SpecParseError):
        RepoSpec.parse("gitlab:team/repo@v1.0.0")


def test_repo_spec_local_path(tmp_path) -> None:
    repo_dir = tmp_path / "tpl"
    spec = RepoSpec.parse(f"local:{repo_dir}@v0.1.0")

    assert spec.host == "local"
    assert spec.local_path == str(repo_dir.resolve())
    assert spec.git_url() == str(repo_dir.resolve())


def test_repo_spec_local_path_alias(tmp_path) -> None:
    repo_dir = tmp_path / "tpl"
    spec = RepoSpec.parse(f"file:{repo_dir}@v0.1.0")

    assert spec.host == "local"
