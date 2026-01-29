from pathlib import Path

import subprocess

from JUSU import android_cli


def test_build_reads_spec_and_copies(tmp_path, monkeypatch):
    # Set up project and dist
    project = tmp_path / "android_app"
    (project / "www").mkdir(parents=True)
    (project / "package.json").write_text('{}')
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html></html>")

    # create a spec in cwd
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    spec = cwd / "jusu.spec.toml"
    spec.write_text('[app]\nname = "SpecApp"\n[android]\npackage = "com.example.spec"\npackage_type = "aab"\n')

    calls = []

    def fake_run(cmd, cwd=None, **kwargs):
        calls.append((cmd, cwd))
        class R:
            returncode = 0
        return R()

    import os
    monkeypatch.setenv('PYTEST_CWD', str(cwd))
    monkeypatch.chdir(cwd)
    import subprocess as sp
    monkeypatch.setattr(sp, 'run', fake_run)

    android_cli.android_build(project_dir=project, bundle_dir=dist, run_sync=False)

    # check that copy happened
    assert (project / "www" / "index.html").exists()
    # and that npx was called (sync false but build will still call cap build)
    assert any('cap' in c[0] for c in calls)
    # Spec file should have been detected and a message printed earlier (not asserted here)
