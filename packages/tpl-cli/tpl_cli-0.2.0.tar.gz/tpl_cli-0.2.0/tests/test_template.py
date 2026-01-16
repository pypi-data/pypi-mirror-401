from __future__ import annotations

import os

from tpl.template import ensure_cookiecutter_state


def test_ensure_cookiecutter_state_uses_env_dir(tmp_path, monkeypatch) -> None:
    state_root = tmp_path / "state"
    monkeypatch.setenv("TPL_COOKIECUTTER_STATE_DIR", str(state_root))
    monkeypatch.delenv("HOME", raising=False)

    config_path, replay_dir = ensure_cookiecutter_state()

    assert config_path == state_root / "cookiecutter.yaml"
    assert replay_dir == state_root / "cookiecutter-replay"
    assert config_path.exists()
    assert replay_dir.exists()
    assert os.environ["COOKIECUTTER_CONFIG"] == str(config_path)
    assert os.environ["COOKIECUTTER_REPLAY_DIR"] == str(replay_dir)

    config_text = config_path.read_text(encoding="utf-8")
    assert "default_context: {}" in config_text
    assert f"replay_dir: {replay_dir.as_posix()}" in config_text
