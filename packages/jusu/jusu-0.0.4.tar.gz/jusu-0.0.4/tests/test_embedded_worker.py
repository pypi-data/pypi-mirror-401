from pathlib import Path
import shutil
import zipfile

from JUSU import embedded_worker


def test_package_worker(tmp_path):
    src = tmp_path / "worker_src"
    src.mkdir()
    (src / "worker.py").write_text("def do_work(x):\n    return x[::-1]\n")
    out = tmp_path / "out" / "worker.zip"

    path = embedded_worker.package_worker(src, out)
    assert path.exists()
    # verify zip contains worker.py
    with zipfile.ZipFile(path, "r") as z:
        assert "worker.py" in z.namelist()
