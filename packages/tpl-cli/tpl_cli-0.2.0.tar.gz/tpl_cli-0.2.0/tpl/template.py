from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

from cookiecutter.exceptions import NonTemplatedInputDirException
from cookiecutter.main import cookiecutter

from .errors import TemplateError


def render_template(
    repo_path: Path,
    entries: list[str],
    extra_context: dict[str, str],
) -> dict[str, bytes]:
    if not entries:
        return {}

    unique_entries: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            unique_entries.append(entry)

    config_path, replay_dir = ensure_cookiecutter_state()

    with TemporaryDirectory() as tmpdir:
        try:
            rendered_path = Path(
                cookiecutter(
                    template=str(repo_path),
                    no_input=True,
                    extra_context=extra_context or None,
                    output_dir=tmpdir,
                    config_file=str(config_path),
                    default_config=False,
                )
            )
        except NonTemplatedInputDirException:
            return _read_raw_entries(repo_path, entries)
        result: dict[str, bytes] = {}
        for entry_path in unique_entries:
            target = rendered_path / entry_path
            if not target.exists():
                raise TemplateError(f"Rendered template missing entry file '{entry_path}'")
            result[entry_path] = target.read_bytes()

    return {entry: result[entry] for entry in entries}


def render_template_tree(
    repo_path: Path,
    extra_context: dict[str, str],
) -> dict[str, bytes]:
    config_path, _ = ensure_cookiecutter_state()

    with TemporaryDirectory() as tmpdir:
        try:
            rendered_path = Path(
                cookiecutter(
                    template=str(repo_path),
                    no_input=True,
                    extra_context=extra_context or None,
                    output_dir=tmpdir,
                    config_file=str(config_path),
                    default_config=False,
                )
            )
        except NonTemplatedInputDirException:
            return _read_raw_tree(repo_path)

        result: dict[str, bytes] = {}
        for path in sorted(rendered_path.rglob("*")):
            if not path.is_file():
                continue
            entry = path.relative_to(rendered_path).as_posix()
            result[entry] = path.read_bytes()

    return result


def _read_raw_entries(repo_path: Path, entries: list[str]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for entry_path in entries:
        target = repo_path / entry_path
        if not target.exists():
            raise TemplateError(f"Template missing entry file '{entry_path}'")
        if target.is_dir():
            raise TemplateError(f"Template entry '{entry_path}' is a directory")
        result[entry_path] = target.read_bytes()
    return result


def _read_raw_tree(repo_path: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in sorted(repo_path.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.name == "cookiecutter.json":
            continue
        entry = path.relative_to(repo_path).as_posix()
        result[entry] = path.read_bytes()
    return result


def compute_sha256(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def ensure_cookiecutter_state() -> tuple[Path, Path]:
    base_dir = os.environ.get("TPL_COOKIECUTTER_STATE_DIR")
    if base_dir:
        state_root = Path(base_dir)
    else:
        home_dir = os.environ.get("HOME")
        if home_dir:
            state_root = Path(home_dir) / ".tpl-state"
        else:
            state_root = Path(tempfile.gettempdir()) / "tpl-state"

    replay_dir = state_root / "cookiecutter-replay"
    config_path = state_root / "cookiecutter.yaml"
    replay_dir.mkdir(parents=True, exist_ok=True)
    state_root.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        config_path.write_text(_cookiecutter_config(replay_dir), encoding="utf-8")

    os.environ["COOKIECUTTER_CONFIG"] = str(config_path)
    os.environ["COOKIECUTTER_REPLAY_DIR"] = str(replay_dir)
    return config_path, replay_dir


def _cookiecutter_config(replay_dir: Path) -> str:
    return f"default_context: {{}}\nreplay_dir: {replay_dir.as_posix()}\n"
