import os
import subprocess
from pathlib import Path

import pytest

from JUSU import android_cli


def test_init_creates_template(tmp_path, monkeypatch):
    # Prepare a fake template directory inside the repo
    repo = Path(__file__).resolve().parents[1]
    template = repo / "scripts" / "android" / "capacitor-template"
    assert template.exists()

    out = tmp_path / "myapp"
    # Run init (do not run npm install)
    android_cli.android_init(project_dir=out, app_id="com.example.test", app_name="TestApp", install=False)
    assert (out / "package.json").exists()
    assert (out / "capacitor.config.json").exists()
    content = (out / "package.json").read_text()
    assert "com.example.test" in content


def test_build_fails_when_no_project(tmp_path):
    import typer as _typer
    with pytest.raises(_typer.Exit):
        android_cli.android_build(project_dir=tmp_path / "does-not-exist")


def test_build_copies_bundle_and_invokes_npx(tmp_path, monkeypatch):
    # Create fake capacitor project
    project = tmp_path / "android_app"
    (project / "www").mkdir(parents=True)
    (project / "package.json").write_text('{}')
    # create a fake dist bundle
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html></html>")

    calls = []

    def fake_run(cmd, cwd=None, **kwargs):
        calls.append((cmd, cwd))
        class R:
            returncode = 0
        return R()

    monkeypatch.setattr(subprocess, "run", fake_run)

    android_cli.android_build(project_dir=project, bundle_dir=dist, run_sync=True)
    # check that npx cap sync and npx cap build were called
    assert any("cap" in c[0] for c in calls)
    # check that index.html made it into the www folder
    assert (project / "www" / "index.html").exists()
