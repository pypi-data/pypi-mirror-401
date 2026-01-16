from __future__ import annotations

from pathlib import Path

import pytest
from tpl.errors import TemplateError
from tpl.project import ProjectPlan, build_local_project_plan, build_project_plan
from tpl.specs import RepoSpec


class DummyCache:
    def __init__(self, mapping: dict[str, Path]):
        self._mapping = mapping

    def ensure_version(self, spec: RepoSpec) -> Path:  # pragma: no cover - signature only
        return self._mapping[spec.display()]


def test_project_plan_expands_blocks_and_nested_projects(tmp_path) -> None:
    root_repo = tmp_path / "root"
    child_repo = tmp_path / "child"
    root_repo.mkdir()
    child_repo.mkdir()

    (child_repo / "tpl.toml").write_text(
        """
name = "child"
version = "0.2.0"

[context]
runtime = "py"

[[blocks]]
source = "gh:me/block-b@v1.0.0"

[[blocks.files]]
path = "src/app.py"
entry = "src/app.py"
""".strip(),
        encoding="utf-8",
    )

    (root_repo / "tpl.toml").write_text(
        """
name = "root"
version = "0.1.0"

[context]
project_name = "demo"

[[blocks]]
source = "gh:me/block-a@v0.1.0"

[[blocks.files]]
path = "README.md"
entry = "README.md"

[[blocks.files]]
path = "docs/README.md"
entry = "docs/README.md"

[[blocks]]
kind = "project"
source = "gh:me/child@0.2.0"
""".strip(),
        encoding="utf-8",
    )

    cache = DummyCache(
        {
            "gh:me/root@0.1.0": root_repo,
            "gh:me/child@0.2.0": child_repo,
        }
    )

    plan = build_project_plan(RepoSpec.parse("gh:me/root@0.1.0"), cache, overrides={"owner": "me"})

    assert isinstance(plan, ProjectPlan)
    assert plan.version == "0.1.0"
    assert plan.context["project_name"] == "demo"
    assert plan.context["owner"] == "me"
    assert len(plan.blocks) == 3
    first, second, third = plan.blocks
    assert first.path == "README.md"
    assert first.entry == "README.md"
    assert first.context["project_name"] == "demo"
    assert first.context["owner"] == "me"

    assert second.path == "docs/README.md"
    assert second.entry == "docs/README.md"
    assert second.context["project_name"] == "demo"
    assert second.context["owner"] == "me"

    assert third.path == "src/app.py"
    assert third.entry == "src/app.py"
    assert third.context["runtime"] == "py"
    assert third.context["project_name"] == "demo"


def test_project_plan_detects_recursion(tmp_path) -> None:
    repo_path = tmp_path / "loop"
    repo_path.mkdir()
    (repo_path / "tpl.toml").write_text(
        """
name = "loop"
version = "0.1.0"

[[blocks]]
kind = "project"
source = "gh:me/loop@0.1.0"
""".strip(),
        encoding="utf-8",
    )

    cache = DummyCache({"gh:me/loop@0.1.0": repo_path})

    with pytest.raises(TemplateError):
        build_project_plan(RepoSpec.parse("gh:me/loop@0.1.0"), cache)


def test_local_project_plan_builds_from_config(tmp_path) -> None:
    config = tmp_path / "tpl.toml"
    config.write_text(
        """
name = "local"
version = "0.3.0"

[context]
owner = "init"

[[blocks]]
source = "gh:you/block@v1.0.0"

[[blocks.files]]
path = "README.md"
entry = "README.md"
""".strip(),
        encoding="utf-8",
    )

    cache = DummyCache({})
    plan = build_local_project_plan(
        config,
        cache,
        overrides={"owner": "override"},
        source_label="local:tpl.toml",
    )

    assert plan.source == "local:tpl.toml"
    assert plan.version == "0.3.0"
    assert plan.context["owner"] == "override"
    assert len(plan.blocks) == 1
    assert plan.blocks[0].path == "README.md"
    assert plan.blocks[0].entry == "README.md"
