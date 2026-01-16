from __future__ import annotations

import pytest
from tpl.errors import TPLError
from tpl.lockfile import LOCKFILE_NAME, LockEntry, Lockfile, ProjectInfo


def test_lockfile_round_trip(tmp_path) -> None:
    lock = Lockfile(root=tmp_path)
    entry = LockEntry(
        path="configs/logging.yaml",
        source="gh:you/template",
        version="0.1.0",
        entry="logging.yaml",
        sha256="abc123",
        context={"project_slug": "demo"},
    )

    lock.set_project(
        ProjectInfo(source="gh:you/project", version="0.2.0", context={"name": "demo"})
    )
    lock.upsert(entry)

    persisted = (tmp_path / LOCKFILE_NAME).read_text(encoding="utf-8")
    assert "[[files]]" in persisted
    assert 'path = "configs/logging.yaml"' in persisted

    reloaded = Lockfile(root=tmp_path)
    loaded_entry = reloaded.find("configs/logging.yaml")
    project_info = reloaded.project()

    assert loaded_entry == entry
    assert project_info == ProjectInfo(
        source="gh:you/project", version="0.2.0", context={"name": "demo"}
    )


def test_lockfile_reads_project_sources_from_string_and_table(tmp_path) -> None:
    lock_path = tmp_path / LOCKFILE_NAME
    lock_path.write_text(
        """
[[files]]
path = "README.md"
source = "gh:you/template"
version = "v1.0.0"
entry = "README.md"
sha256 = "abc123"
project = "local:tpl.toml"

[[files]]
path = "docs/guide.md"
source = "gh:you/template"
version = "v1.0.0"
entry = "docs/guide.md"
sha256 = "def456"
project = { source = "gh:you/project" }
""".strip()
        + "\n",
        encoding="utf-8",
    )

    lock = Lockfile(root=tmp_path)
    readme = lock.find("README.md")
    docs = lock.find("docs/guide.md")

    assert readme is not None
    assert readme.project == "local:tpl.toml"
    assert docs is not None
    assert docs.project == "gh:you/project"


def test_lockfile_rejects_non_table_context(tmp_path) -> None:
    lock_path = tmp_path / LOCKFILE_NAME
    lock_path.write_text(
        """
[project]
source = "gh:you/project"
version = "0.1.0"
context = "bad"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    lock = Lockfile(root=tmp_path)
    with pytest.raises(TPLError):
        lock.load()
