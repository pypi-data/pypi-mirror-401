from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .cache import RepoCache
from .errors import TemplateError
from .specs import RepoSpec

PROJECT_FILE = "tpl.toml"
DEFAULT_LOCAL_PROJECT_FILE = "tpl.toml"


@dataclass
class BlockTarget:
    path: Optional[str]
    entry: Optional[str]


@dataclass
class ProjectBlock:
    kind: str
    source: str
    targets: list[BlockTarget]
    context: dict[str, str]


@dataclass
class ProjectTemplate:
    name: str
    version: str
    context: dict[str, str]
    blocks: list[ProjectBlock]


@dataclass
class BlockTask:
    spec: RepoSpec
    path: Optional[str]
    entry: Optional[str]
    context: dict[str, str]
    full_tree: bool = False


@dataclass
class ProjectPlan:
    source: str
    version: str
    context: dict[str, str]
    blocks: list[BlockTask]
    spec: Optional[RepoSpec] = None


def load_project_template(repo_path: Path) -> ProjectTemplate:
    return load_project_template_from_path(repo_path / PROJECT_FILE)


def load_project_template_from_path(path: Path) -> ProjectTemplate:
    if not path.exists():
        raise TemplateError(f"Project template missing {path.name}")

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise TemplateError(f"Failed to parse {path.name}: {exc}") from exc

    try:
        name = data["name"]
        version = data["version"]
    except KeyError as exc:
        raise TemplateError(f"Missing required project metadata field: {exc.args[0]}") from exc

    context = _parse_context(data.get("context", {}))
    blocks = [_parse_block(entry) for entry in data.get("blocks", [])]

    return ProjectTemplate(name=name, version=version, context=context, blocks=blocks)


def build_project_plan(
    spec: RepoSpec,
    cache: RepoCache,
    overrides: Optional[dict[str, str]] = None,
    *,
    _visited: Optional[set[str]] = None,
) -> ProjectPlan:
    version = spec.require_version()
    visited = _visited or set()
    cache_key = f"{spec.without_version()}@{version}"
    if cache_key in visited:
        raise TemplateError(f"Detected recursive project template include for {cache_key}")

    repo_path = cache.ensure_version(spec)
    template = load_project_template(repo_path)
    if template.version != version:
        raise TemplateError(
            f"Project template version mismatch: metadata {template.version} != requested {version}"
        )

    effective_context: dict[str, str] = dict(template.context)
    if overrides:
        effective_context.update(overrides)

    visited.add(cache_key)
    blocks = _expand_blocks(template.blocks, effective_context, cache, visited)
    visited.remove(cache_key)

    return ProjectPlan(
        source=spec.without_version(),
        version=version,
        context=effective_context,
        blocks=blocks,
        spec=spec.with_version(version),
    )


def build_local_project_plan(
    config_path: Path,
    cache: RepoCache,
    overrides: Optional[dict[str, str]] = None,
    *,
    source_label: Optional[str] = None,
    _visited: Optional[set[str]] = None,
) -> ProjectPlan:
    config_path = config_path.resolve()
    template = load_project_template_from_path(config_path)

    effective_context: dict[str, str] = dict(template.context)
    if overrides:
        effective_context.update(overrides)

    label = source_label or f"local:{config_path}"
    visited = _visited or set()
    if label in visited:
        raise TemplateError(f"Detected recursive project template include for {label}")

    visited.add(label)
    blocks = _expand_blocks(template.blocks, effective_context, cache, visited)
    visited.remove(label)

    return ProjectPlan(
        source=label,
        version=template.version,
        context=effective_context,
        blocks=blocks,
        spec=None,
    )


def _expand_blocks(
    blocks: list[ProjectBlock],
    base_context: dict[str, str],
    cache: RepoCache,
    visited: set[str],
) -> list[BlockTask]:
    tasks: list[BlockTask] = []
    for block in blocks:
        block_context = dict(base_context)
        block_context.update(block.context)
        if block.kind == "project":
            child_spec = RepoSpec.parse(block.source, require_version=False)
            if child_spec.version is None:
                if child_spec.local_path:
                    child_spec = child_spec.with_version("local")
                else:
                    raise TemplateError("Repo spec must include a version (use @<tag>)")
            child_plan = build_project_plan(child_spec, cache, block_context, _visited=visited)
            tasks.extend(child_plan.blocks)
            continue

        block_spec = RepoSpec.parse(block.source, require_version=False)
        if block_spec.version is None:
            if block_spec.local_path:
                block_spec = block_spec.with_version("local")
            else:
                raise TemplateError("Repo spec must include a version (use @<tag>)")
        if not block.targets:
            tasks.append(
                BlockTask(
                    spec=block_spec,
                    path=None,
                    entry=None,
                    context=block_context,
                    full_tree=True,
                )
            )
        else:
            for target in block.targets:
                if target.path is None:
                    raise TemplateError("Block entries must define a 'path'")
                entry = target.entry or Path(target.path).name
                tasks.append(
                    BlockTask(
                        spec=block_spec,
                        path=target.path,
                        entry=entry,
                        context=block_context,
                    )
                )
    return tasks


def _parse_block(entry: dict[str, object]) -> ProjectBlock:
    kind = str(entry.get("kind", "block")).lower()
    source = entry.get("source")
    if not isinstance(source, str):
        raise TemplateError("Each block must define a 'source'")

    targets: list[BlockTarget] = []
    files_value = entry.get("files")
    if files_value is not None:
        if not isinstance(files_value, list):
            raise TemplateError("Block 'files' must be an array of tables")
        for _idx, file_entry in enumerate(files_value):
            if not isinstance(file_entry, dict):
                raise TemplateError("Each block.files entry must be a table")
            path_value = file_entry.get("path")
            if not isinstance(path_value, str):
                raise TemplateError("Each block.files entry requires a string 'path'")
            entry_value = file_entry.get("entry")
            if entry_value is not None and not isinstance(entry_value, str):
                raise TemplateError("Each block.files entry must use a string 'entry'")
            targets.append(BlockTarget(path=path_value, entry=entry_value))
    else:
        target = entry.get("path")
        if target is not None and not isinstance(target, str):
            raise TemplateError("Block 'path' must be a string")
        entry_file = entry.get("entry")
        if entry_file is not None and not isinstance(entry_file, str):
            raise TemplateError("Block 'entry' must be a string")
        if kind == "block" and target is not None:
            targets.append(BlockTarget(path=target, entry=entry_file))

    context = _parse_context(entry.get("context", {}))

    return ProjectBlock(kind=kind, source=source, targets=targets, context=context)


def _parse_context(value: object) -> dict[str, str]:
    if not value:
        return {}
    if not isinstance(value, dict):
        raise TemplateError("Context must be a table")
    context: dict[str, str] = {}
    for key, raw in value.items():
        context[str(key)] = str(raw)
    return context
