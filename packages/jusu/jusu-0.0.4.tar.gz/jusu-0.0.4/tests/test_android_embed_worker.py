from pathlib import Path
import shutil

import pytest

from JUSU import android_cli
from JUSU import embedded_worker


def test_embed_worker_commands(tmp_path, monkeypatch):
    # Create a fake worker source
    worker_src = tmp_path / "worker_src"
    worker_src.mkdir()
    (worker_src / "worker.py").write_text("def do_work(x):\n    return x.upper()\n")

    # Create a fake chaquopy android project layout
    project = tmp_path / "android_example"
    (project / "app" / "src" / "main" / "python").mkdir(parents=True)

    # Run embed_worker
    android_cli.embed_worker(worker_src=worker_src, chaquopy_project=project)

    # After embedding, worker.py should exist in the project's python dir
    assert (project / "app" / "src" / "main" / "python" / "worker.py").exists()
