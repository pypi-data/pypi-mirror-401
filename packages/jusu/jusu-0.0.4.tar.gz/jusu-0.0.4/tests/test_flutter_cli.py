import subprocess
from pathlib import Path
import shutil

import pytest

from JUSU import flutter_cli


def test_init_creates_project(tmp_path):
    project = tmp_path / "my_flutter_app"
    # Ensure template exists in repository scripts/flutter-template
    template = Path(__file__).parent.parent / "scripts" / "flutter-template"
    assert template.exists(), "Template missing"

    flutter_cli.init(project_dir=project, install=False)

    assert project.exists()
    assert (project / "pubspec.yaml").exists()
    assert (project / "lib" / "main.dart").exists()
    assert (project / "assets" / "www" / "index.html").exists()


def test_build_copies_bundle_and_invokes_flutter(tmp_path, monkeypatch):
    # Copy template to simulate an existing project
    template = Path(__file__).parent.parent / "scripts" / "flutter-template"
    project = tmp_path / "proj"
    shutil.copytree(template, project)

    # Create a fake bundle dir
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "index.html").write_text("<h1>bundle</h1>")

    calls = []

    def fake_run(cmd, check=True, cwd=None):
        calls.append((cmd, cwd))
        return None

    monkeypatch.setattr(subprocess, "run", fake_run)

    # Run build with run_sync -> should copy files and call flutter build
    flutter_cli.build(project_dir=project, build_mode="apk", bundle_dir=bundle, run_sync=True)

    assert (project / "assets" / "www" / "index.html").exists()
    assert any(cmd[0] == "flutter" and "build" in cmd for cmd, _ in calls)
