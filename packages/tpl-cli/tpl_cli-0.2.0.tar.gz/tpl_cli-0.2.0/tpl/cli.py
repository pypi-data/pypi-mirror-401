from __future__ import annotations

import argparse
import difflib
import importlib.metadata
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence

from .cache import RepoCache
from .errors import GitError, TemplateError, TPLError
from .lockfile import LockEntry, Lockfile, ProjectInfo
from .project import (
    DEFAULT_LOCAL_PROJECT_FILE,
    ProjectPlan,
    build_local_project_plan,
    build_project_plan,
)
from .specs import RepoSpec, SpecParseError
from .template import compute_sha256, render_template, render_template_tree

EXAMPLES = """Examples:
  tpl pull gh:you/tpl-logging@v0.3.0 --file infra/logging.yaml=logging.yaml
    --set project_slug=my-app
  tpl compose gh:you/python-service@v1.2.0 --set project_name=my-app
  tpl apply --config tpl.toml --force
  tpl status
  tpl upgrade infra/logging.yaml --to v0.4.0 --merge
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tpl",
        description="Template pulling CLI",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"tpl {_get_version()}",
        help="Show version and exit",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pull = subparsers.add_parser(
        "pull",
        help="Pull a template into the project",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    pull.add_argument(
        "repo_spec",
        help="Template repo spec (Cookiecutter repo), e.g., gh:user/logging@v0.1.0",
    )
    pull.add_argument(
        "--as",
        dest="target",
        help="Destination path for the file (legacy single-file syntax)",
    )
    pull.add_argument(
        "--file",
        action="append",
        default=[],
        metavar="DEST[=ENTRY]",
        help="Copy DEST from template entry ENTRY (repeatable); omit for full template",
    )
    pull.add_argument(
        "--multi",
        action="append",
        default=[],
        metavar="PATH=ENTRY",
        help="Add another destination=entry pair (repeatable)",
    )
    pull.add_argument("--force", action="store_true", help="Overwrite existing files")
    pull.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override cookiecutter context values (repeatable)",
    )

    compose = subparsers.add_parser(
        "compose",
        help="Apply a remote project template",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    compose.add_argument("project_spec", help="Project repo spec, e.g., gh:user/template@v0.1.0")
    compose.add_argument("--force", action="store_true", help="Overwrite existing files")
    compose.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override project context values (repeatable)",
    )

    apply = subparsers.add_parser(
        "apply",
        help="Apply a local project configuration",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    apply.add_argument(
        "--config",
        default=DEFAULT_LOCAL_PROJECT_FILE,
        help="Path to the local project file (default tpl.toml)",
    )
    apply.add_argument("--force", action="store_true", help="Overwrite existing files")
    apply.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override project context values (repeatable)",
    )

    init = subparsers.add_parser(
        "init",
        help="Create a starter tpl.toml in this project",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    init.add_argument(
        "--path",
        default=DEFAULT_LOCAL_PROJECT_FILE,
        help="Destination path for tpl.toml (default tpl.toml)",
    )
    init.add_argument("--force", action="store_true", help="Overwrite existing files")

    subparsers.add_parser(
        "status",
        help="Show managed file status",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )

    upgrade = subparsers.add_parser(
        "upgrade",
        help="Upgrade a file or entire project",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EXAMPLES,
    )
    upgrade.add_argument(
        "path",
        nargs="?",
        help="Managed file path (omit to upgrade a composed project)",
    )
    upgrade.add_argument("--to", dest="version", help="Target version tag")
    upgrade.add_argument(
        "--no-merge",
        action="store_true",
        help="Skip automatic three-way merges when conflicts occur",
    )
    upgrade.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting pre-existing files when new blocks are added",
    )

    return parser


def _get_version() -> str:
    try:
        return importlib.metadata.version("tpl-cli")
    except importlib.metadata.PackageNotFoundError:
        return "0+unknown"


def _use_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _style(text: str, code: str) -> str:
    if _use_color():
        return f"\x1b[{code}m{text}\x1b[0m"
    return text


def _print_ok(message: str) -> None:
    print(_style(message, "32"))


def _print_info(message: str) -> None:
    print(_style(message, "36"))


def _print_table(rows: Sequence[Sequence[str]]) -> None:
    if not rows:
        return
    widths = [0] * len(rows[0])
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))
    for row_index, row in enumerate(rows):
        padded = [value.ljust(widths[idx]) for idx, value in enumerate(row)]
        print("  ".join(padded))
        if row_index == 0:
            separators = ["-" * width for width in widths]
            print("  ".join(separators))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cache = RepoCache()
    lockfile = Lockfile()

    try:
        if args.command == "pull":
            handle_pull(args, cache, lockfile)
        elif args.command == "compose":
            handle_compose(args, cache, lockfile)
        elif args.command == "apply":
            handle_apply(args, cache, lockfile)
        elif args.command == "init":
            handle_init(args, lockfile)
        elif args.command == "status":
            handle_status(lockfile)
        elif args.command == "upgrade":
            handle_upgrade(args, cache, lockfile)
    except (SpecParseError, GitError, TemplateError, TPLError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    return 0


def handle_pull(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    spec = RepoSpec.parse(args.repo_spec, require_version=False)
    if spec.version is None:
        if spec.local_path:
            spec = spec.with_version("local")
        else:
            raise SpecParseError("Repo spec must include a version (use @<tag>)")
    repo_path = cache.ensure_version(spec)
    context = parse_extra_context(args.set)
    if args.file or args.target:
        targets = parse_pull_targets(args, lockfile)
        entries = [target.entry for target in targets]
        rendered = render_template(repo_path, entries, context)

        for target in targets:
            file_bytes = rendered[target.entry]
            install_rendered_file(
                target.destination,
                relative_path=target.relative,
                spec=spec,
                metadata_version=spec.require_version(),
                metadata_entry=target.entry,
                file_bytes=file_bytes,
                lockfile=lockfile,
                context=context,
                force=args.force,
                project_source=None,
            )
            _print_ok(f"Wrote {target.relative} from {spec.display()}")
        _print_info(f"Done: {len(targets)} file(s) written")
        return

    rendered = render_template_tree(repo_path, context)
    if not rendered:
        raise TPLError("Template rendered no files")

    for entry in sorted(rendered):
        file_bytes = rendered[entry]
        relative_path, destination = resolve_user_path(entry, lockfile.root)
        install_rendered_file(
            destination,
            relative_path=relative_path,
            spec=spec,
            metadata_version=spec.require_version(),
            metadata_entry=entry,
            file_bytes=file_bytes,
            lockfile=lockfile,
            context=context,
            force=args.force,
            project_source=None,
        )
        _print_ok(f"Wrote {relative_path} from {spec.display()}")
    _print_info(f"Done: {len(rendered)} file(s) written")


def handle_compose(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    spec = RepoSpec.parse(args.project_spec, require_version=False)
    if spec.version is None:
        if spec.local_path:
            spec = spec.with_version("local")
        else:
            raise SpecParseError("Repo spec must include a version (use @<tag>)")
    overrides = parse_extra_context(args.set)
    plan = build_project_plan(spec, cache, overrides)
    apply_project_plan(plan, cache, lockfile, force=args.force)
    _print_ok(f"Applied project template {spec.display()} ({len(plan.blocks)} file(s) written)")


def handle_apply(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = (lockfile.root / config_path).resolve()
    relative_config = os.path.relpath(config_path, lockfile.root)
    overrides = parse_extra_context(args.set)
    plan = build_local_project_plan(
        config_path,
        cache,
        overrides,
        source_label=f"local:{relative_config}",
    )
    apply_project_plan(plan, cache, lockfile, force=args.force)
    _print_ok(
        f"Applied local project config {relative_config} ({len(plan.blocks)} file(s) written)"
    )


def handle_init(args: argparse.Namespace, lockfile: Lockfile) -> None:
    path = Path(args.path)
    if not path.is_absolute():
        path = (lockfile.root / path).resolve()
    if path.exists() and not args.force:
        raise TPLError(f"File {path} already exists (use --force to overwrite)")
    project_name = lockfile.root.name or "project"
    path.write_text(_starter_tpl_config(project_name), encoding="utf-8")
    relative_path = os.path.relpath(path, lockfile.root)
    _print_ok(f"Wrote {relative_path}")


def handle_status(lockfile: Lockfile) -> None:
    entries = lockfile.entries()
    project = lockfile.project()
    if project:
        _print_info(f"Project: {project.source}@{project.version}")
    if not entries:
        _print_info("No managed files yet. Use 'tpl pull' or 'tpl compose' to add one.")
        return

    rows = [("PATH", "STATUS", "SOURCE", "VERSION", "PROJECT")]
    status_counts = {"OK": 0, "MODIFIED": 0, "MISSING": 0}
    for entry in entries:
        path = (lockfile.root / entry.path).resolve()
        if not path.exists():
            status = "MISSING"
        else:
            status = "OK" if compute_sha256(path.read_bytes()) == entry.sha256 else "MODIFIED"
        status_counts[status] += 1
        rows.append(
            (
                entry.path,
                status,
                entry.source,
                entry.version,
                entry.project or "-",
            )
        )

    _print_table(rows)
    _print_info(
        "Summary: "
        f"{status_counts['OK']} OK, "
        f"{status_counts['MODIFIED']} MODIFIED, "
        f"{status_counts['MISSING']} MISSING"
    )


def handle_upgrade(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    if args.path:
        handle_upgrade_file(args, cache, lockfile)
    else:
        handle_upgrade_project(args, cache, lockfile)


def handle_upgrade_file(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    relative_path, destination = resolve_user_path(args.path, lockfile.root)
    entry = lockfile.find(relative_path)
    if not entry:
        raise TPLError(f"File {args.path} is not managed by tpl. Run `tpl status` first.")

    spec = RepoSpec.parse(entry.source, require_version=False)
    current_version = entry.version
    desired_version = (
        resolve_requested_version(cache, spec, args.version)
        if args.version
        else select_latest_version(cache, spec, current_version)
    )
    if desired_version == current_version:
        _print_info(f"{entry.path} already at latest version {current_version}")
        return

    updated_spec = spec.with_version(desired_version)
    repo_path = cache.ensure_version(updated_spec)
    rendered = render_template(repo_path, [entry.entry], entry.context or {})
    new_bytes = rendered[entry.entry]
    apply_upgrade_to_path(
        destination,
        entry,
        new_bytes,
        updated_spec.require_version(),
        entry.entry,
        lockfile,
        cache,
        merge=not args.no_merge,
        context=entry.context,
    )
    _print_ok(f"Upgraded {entry.path} to {updated_spec.require_version()}")


def handle_upgrade_project(args: argparse.Namespace, cache: RepoCache, lockfile: Lockfile) -> None:
    project = lockfile.project()
    if not project:
        raise TPLError("No project template recorded; run 'tpl compose' or 'tpl apply' first")

    source = project.source
    stored_context = project.context or {}

    if source.startswith("local:"):
        relative_target = source.split(":", 1)[1]
        config_path = Path(relative_target)
        if not config_path.is_absolute():
            config_path = (lockfile.root / config_path).resolve()
        if config_path.is_file():
            if not config_path.exists():
                raise TPLError(f"Local project config '{relative_target}' not found")
            plan = build_local_project_plan(
                config_path,
                cache,
                stored_context,
                source_label=source,
            )
            upgrade_project_plan(
                plan, cache, lockfile, merge=not args.no_merge, allow_new=args.force
            )
            _print_ok(f"Reapplied local project config {relative_target} (version {plan.version})")
            return

    spec = RepoSpec.parse(source, require_version=False)
    current_version = project.version
    desired_version = (
        resolve_requested_version(cache, spec, args.version)
        if args.version
        else select_latest_version(cache, spec, current_version)
    )
    if desired_version == current_version:
        _print_info(f"Project already at latest version {current_version}")
        return

    target_spec = spec.with_version(desired_version)
    plan = build_project_plan(target_spec, cache, stored_context)
    upgrade_project_plan(plan, cache, lockfile, merge=not args.no_merge, allow_new=args.force)
    _print_ok(f"Upgraded project to {plan.version}")


def parse_extra_context(values: Iterable[str]) -> dict[str, str]:
    context: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise TPLError(f"Invalid --set value '{item}', expected KEY=VALUE")
        key, value = item.split("=", 1)
        if not key:
            raise TPLError("Context key cannot be empty")
        context[key] = value
    return context


@dataclass
class PullTarget:
    relative: str
    destination: Path
    entry: str


def parse_pull_targets(args: argparse.Namespace, lockfile: Lockfile) -> list[PullTarget]:
    targets: list[PullTarget] = []
    if args.file:
        for dest_string, entry_name in parse_entry_pairs(args.file):
            relative_path, destination_path = resolve_user_path(dest_string, lockfile.root)
            targets.append(
                PullTarget(relative=relative_path, destination=destination_path, entry=entry_name)
            )
        return targets

    if not args.target:
        raise TPLError("Provide --file DEST[=ENTRY] or legacy --as. See `tpl pull --help`.")

    relative, destination = resolve_user_path(args.target, lockfile.root)
    entry_name = Path(args.target).name
    targets.append(PullTarget(relative=relative, destination=destination, entry=entry_name))
    return targets


def select_latest_version(cache: RepoCache, base_spec: RepoSpec, current_version: str) -> str:
    tags = cache.list_tags(base_spec)
    if not tags:
        raise TPLError("No tags found for repository; cannot upgrade")

    newest = tags[0]
    if _normalize_version(newest) == _normalize_version(current_version):
        return current_version
    return newest


def resolve_requested_version(cache: RepoCache, base_spec: RepoSpec, requested: str) -> str:
    tags = cache.list_tags(base_spec)
    normalized_request = _normalize_version(requested)
    for tag in tags:
        if _normalize_version(tag) == normalized_request:
            return tag
    raise TPLError(f"Version {requested} not found for {base_spec.without_version()}")


def resolve_user_path(value: str, root: Path) -> tuple[str, Path]:
    candidate = Path(value)
    absolute = candidate if candidate.is_absolute() else (root / candidate)
    absolute = absolute.resolve()
    relative = os.path.relpath(absolute, root)
    return relative, absolute


def _normalize_version(tag: str) -> str:
    return tag.lstrip("vV")


def parse_entry_pairs(values: Iterable[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in values:
        if "=" in item:
            destination, entry = item.split("=", 1)
            destination = destination.strip()
            entry = entry.strip()
            if not destination:
                raise TPLError("--file entries must include a destination path")
            entry_name = entry or Path(destination).name
        else:
            destination = item.strip()
            if not destination:
                raise TPLError("--file entries must include a destination path")
            entry_name = Path(destination).name
        if not entry_name:
            raise TPLError("Unable to infer entry name for --file option")
        pairs.append((destination, entry_name))
    return pairs


def _is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def _starter_tpl_config(project_name: str) -> str:
    return (
        f'name = "{project_name}"\n'
        'version = "0.1.0"\n'
        "\n"
        "[context]\n"
        f'# project_name = "{project_name}"\n'
        "\n"
        "# [[blocks]]\n"
        '# source = "gh:you/template@v0.1.0"\n'
        "#\n"
        "# [[blocks.files]]\n"
        '# path = "path/to/file"\n'
        '# entry = "template-file.ext"\n'
    )


def install_rendered_file(
    destination: Path,
    *,
    relative_path: str,
    spec: RepoSpec,
    metadata_version: str,
    metadata_entry: str,
    file_bytes: bytes,
    lockfile: Lockfile,
    context: Optional[dict[str, str]],
    force: bool,
    project_source: Optional[str],
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        raise TPLError(f"File {destination} already exists (use --force to overwrite)")
    destination.write_bytes(file_bytes)
    lockfile.upsert(
        LockEntry(
            path=relative_path,
            source=spec.without_version(),
            version=metadata_version,
            entry=metadata_entry,
            sha256=compute_sha256(file_bytes),
            context=context.copy() if context else None,
            project=project_source,
        )
    )


def apply_project_plan(
    plan: ProjectPlan,
    cache: RepoCache,
    lockfile: Lockfile,
    *,
    force: bool,
) -> None:
    for task in plan.blocks:
        repo_path = cache.ensure_version(task.spec)
        if task.full_tree:
            rendered = render_template_tree(repo_path, task.context)
            for entry_name in sorted(rendered):
                file_bytes = rendered[entry_name]
                relative_path, destination = resolve_user_path(entry_name, lockfile.root)
                install_rendered_file(
                    destination,
                    relative_path=relative_path,
                    spec=task.spec,
                    metadata_version=task.spec.require_version(),
                    metadata_entry=entry_name,
                    file_bytes=file_bytes,
                    lockfile=lockfile,
                    context=task.context,
                    force=force,
                    project_source=plan.source,
                )
        else:
            if task.entry is None or task.path is None:
                raise TPLError("Project block entries must define a path and entry")
            rendered = render_template(repo_path, [task.entry], task.context)
            file_bytes = rendered[task.entry]
            relative_path, destination = resolve_user_path(task.path, lockfile.root)
            install_rendered_file(
                destination,
                relative_path=relative_path,
                spec=task.spec,
                metadata_version=task.spec.require_version(),
                metadata_entry=task.entry,
                file_bytes=file_bytes,
                lockfile=lockfile,
                context=task.context,
                force=force,
                project_source=plan.source,
            )

    lockfile.set_project(
        ProjectInfo(source=plan.source, version=plan.version, context=plan.context or None)
    )


def upgrade_project_plan(
    plan: ProjectPlan,
    cache: RepoCache,
    lockfile: Lockfile,
    *,
    merge: bool,
    allow_new: bool,
) -> None:
    managed_paths: set[str] = set()
    for task in plan.blocks:
        repo_path = cache.ensure_version(task.spec)
        if task.full_tree:
            rendered = render_template_tree(repo_path, task.context)
            for entry_name in sorted(rendered):
                relative_path, destination = resolve_user_path(entry_name, lockfile.root)
                managed_paths.add(relative_path)
                entry = lockfile.find(relative_path)
                new_bytes = rendered[entry_name]
                if entry is None:
                    if destination.exists() and not allow_new:
                        raise TPLError(
                            f"File {relative_path} exists but is unmanaged; rerun with --force "
                            "to overwrite"
                        )
                    install_rendered_file(
                        destination,
                        relative_path=relative_path,
                        spec=task.spec,
                        metadata_version=task.spec.require_version(),
                        metadata_entry=entry_name,
                        file_bytes=new_bytes,
                        lockfile=lockfile,
                        context=task.context,
                        force=True,
                        project_source=plan.source,
                    )
                    continue

                apply_upgrade_to_path(
                    destination,
                    entry,
                    new_bytes,
                    task.spec.require_version(),
                    entry_name,
                    lockfile,
                    cache,
                    merge=merge,
                    project_source=plan.source,
                    context=task.context,
                )
        else:
            if task.entry is None or task.path is None:
                raise TPLError("Project block entries must define a path and entry")
            relative_path, destination = resolve_user_path(task.path, lockfile.root)
            managed_paths.add(relative_path)
            entry = lockfile.find(relative_path)
            rendered = render_template(repo_path, [task.entry], task.context)
            new_bytes = rendered[task.entry]
            if entry is None:
                if destination.exists() and not allow_new:
                    raise TPLError(
                        f"File {relative_path} exists but is unmanaged; rerun with --force "
                        "to overwrite"
                    )
                install_rendered_file(
                    destination,
                    relative_path=relative_path,
                    spec=task.spec,
                    metadata_version=task.spec.require_version(),
                    metadata_entry=task.entry,
                    file_bytes=new_bytes,
                    lockfile=lockfile,
                    context=task.context,
                    force=True,
                    project_source=plan.source,
                )
                continue

            apply_upgrade_to_path(
                destination,
                entry,
                new_bytes,
                task.spec.require_version(),
                task.entry,
                lockfile,
                cache,
                merge=merge,
                project_source=plan.source,
                context=task.context,
            )

    for entry in list(lockfile.entries()):
        if entry.project == plan.source and entry.path not in managed_paths:
            lockfile.remove(entry.path)

    lockfile.set_project(
        ProjectInfo(source=plan.source, version=plan.version, context=plan.context or None)
    )


def apply_upgrade_to_path(
    path_obj: Path,
    entry: LockEntry,
    new_bytes: bytes,
    new_version: str,
    metadata_entry: str,
    lockfile: Lockfile,
    cache: RepoCache,
    *,
    merge: bool,
    project_source: Optional[str] = None,
    context: Optional[dict[str, str]] = None,
) -> None:
    if not path_obj.exists():
        raise TPLError(f"Managed file {entry.path} is missing; run tpl compose/pull again")

    current_bytes = path_obj.read_bytes()
    existing_hash = compute_sha256(current_bytes)
    if existing_hash != entry.sha256:
        if merge:
            merged = attempt_three_way_merge(entry, current_bytes, new_bytes, cache)
            if merged is not None:
                path_obj.write_bytes(merged)
                lockfile.upsert(
                    LockEntry(
                        path=entry.path,
                        source=entry.source,
                        version=new_version,
                        entry=metadata_entry,
                        sha256=compute_sha256(merged),
                        context=_copy_context(context, entry.context),
                        project=project_source or entry.project,
                    )
                )
                return
        write_conflict_artifacts(path_obj, current_bytes, new_bytes)
        raise TPLError(
            f"{entry.path} has local changes; review *.tpl-new/*.tpl.diff artifacts for details"
        )

    path_obj.write_bytes(new_bytes)
    lockfile.upsert(
        LockEntry(
            path=entry.path,
            source=entry.source,
            version=new_version,
            entry=metadata_entry,
            sha256=compute_sha256(new_bytes),
            context=_copy_context(context, entry.context),
            project=project_source or entry.project,
        )
    )


def attempt_three_way_merge(
    entry: LockEntry,
    local_bytes: bytes,
    new_bytes: bytes,
    cache: RepoCache,
) -> Optional[bytes]:
    try:
        base_bytes = render_lock_entry(entry, cache)
    except Exception:
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir) / "base"
        local = Path(tmpdir) / "local"
        new = Path(tmpdir) / "new"
        base.write_bytes(base_bytes)
        local.write_bytes(local_bytes)
        new.write_bytes(new_bytes)

        result = subprocess.run(
            ["git", "merge-file", "-p", str(local), str(base), str(new)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode == 0:
            return result.stdout
    return None


def render_lock_entry(entry: LockEntry, cache: RepoCache) -> bytes:
    spec = RepoSpec.parse(f"{entry.source}@{entry.version}")
    repo_path = cache.ensure_version(spec)
    rendered = render_template(repo_path, [entry.entry], entry.context or {})
    return rendered[entry.entry]


def write_conflict_artifacts(path_obj: Path, local_bytes: bytes, new_bytes: bytes) -> None:
    temp_path = path_obj.with_suffix(path_obj.suffix + ".tpl-new")
    temp_path.write_bytes(new_bytes)
    diff_path = path_obj.with_suffix(path_obj.suffix + ".tpl.diff")
    local_text = local_bytes.decode("utf-8", errors="ignore")
    new_text = new_bytes.decode("utf-8", errors="ignore")
    diff = difflib.unified_diff(
        local_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=str(path_obj),
        tofile=str(temp_path),
    )
    diff_path.write_text("".join(diff), encoding="utf-8")


def _copy_context(
    new_context: Optional[dict[str, str]], fallback: Optional[dict[str, str]]
) -> Optional[dict[str, str]]:
    if new_context:
        return new_context.copy()
    if fallback:
        return fallback.copy()
    return None
