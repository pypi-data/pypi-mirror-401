from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .errors import TPLError

LOCKFILE_NAME = ".tpl-lock.toml"


@dataclass
class LockEntry:
    path: str
    source: str
    version: str
    entry: str
    sha256: str
    context: Optional[dict[str, str]] = None
    project: Optional[str] = None


@dataclass
class ProjectInfo:
    source: str
    version: str
    context: Optional[dict[str, str]] = None


class Lockfile:
    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = root or Path.cwd()
        self.path = self.root / LOCKFILE_NAME
        self._entries: dict[str, LockEntry] = {}
        self._project: Optional[ProjectInfo] = None
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return
        if not self.path.exists():
            self._entries = {}
            self._loaded = True
            return
        try:
            data = tomllib.loads(self.path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            raise TPLError(f"Failed to parse {LOCKFILE_NAME}: {exc}") from exc

        project_data = data.get("project", {}) if isinstance(data, dict) else {}
        if project_data:
            self._project = ProjectInfo(
                source=project_data["source"],
                version=project_data["version"],
                context=_ensure_context(project_data.get("context")),
            )
        else:
            self._project = None

        files = data.get("files", []) if isinstance(data, dict) else []
        for item in files:
            entry = LockEntry(
                path=item["path"],
                source=item["source"],
                version=item["version"],
                entry=item["entry"],
                sha256=item["sha256"],
                context=_ensure_context(item.get("context")),
                project=_read_project_source(item.get("project")),
            )
            self._entries[entry.path] = entry

        self._loaded = True

    def entries(self) -> list[LockEntry]:
        self.load()
        return list(self._entries.values())

    def find(self, path: str) -> Optional[LockEntry]:
        self.load()
        return self._entries.get(path)

    def upsert(self, entry: LockEntry) -> None:
        self.load()
        self._entries[entry.path] = entry
        self._write()

    def remove(self, path: str) -> None:
        self.load()
        if path in self._entries:
            del self._entries[path]
            self._write()

    def set_project(self, info: Optional[ProjectInfo]) -> None:
        self.load()
        self._project = info
        self._write()

    def project(self) -> Optional[ProjectInfo]:
        self.load()
        return self._project

    def _write(self) -> None:
        sorted_entries = [self._entries[key] for key in sorted(self._entries.keys())]
        lines: list[str] = []
        if self._project:
            lines.append("[project]")
            lines.append(f'source = "{self._project.source}"')
            lines.append(f'version = "{self._project.version}"')
            if self._project.context:
                lines.append("[project.context]")
                for key in sorted(self._project.context.keys()):
                    value = self._project.context[key]
                    lines.append(f'{key} = "{value}"')
            lines.append("")
        for entry in sorted_entries:
            lines.append("[[files]]")
            lines.append(f'path = "{entry.path}"')
            lines.append(f'source = "{entry.source}"')
            lines.append(f'version = "{entry.version}"')
            lines.append(f'entry = "{entry.entry}"')
            lines.append(f'sha256 = "{entry.sha256}"')
            if entry.context:
                lines.append("[files.context]")
                for key in sorted(entry.context.keys()):
                    value = entry.context[key]
                    lines.append(f'{key} = "{value}"')
            if entry.project:
                lines.append("[files.project]")
                lines.append(f'source = "{entry.project}"')
            lines.append("")
        content = "\n".join(lines).rstrip() + "\n"
        self.path.write_text(content, encoding="utf-8")


def _ensure_context(value: object) -> Optional[dict[str, str]]:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TPLError("Lockfile context must be a table")
    context: dict[str, str] = {}
    for key, raw_value in value.items():
        context[str(key)] = str(raw_value)
    return context


def _read_project_source(value: object) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, dict):
        return str(value.get("source")) if "source" in value else None
    if isinstance(value, str):
        return value
    raise TPLError("Lockfile project field must be a string or table with 'source'")
