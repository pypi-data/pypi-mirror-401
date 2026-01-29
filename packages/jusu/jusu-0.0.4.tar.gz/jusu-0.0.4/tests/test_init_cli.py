from pathlib import Path

from JUSU import cli


def test_init_writes_spec(tmp_path, monkeypatch):
    spec_path = tmp_path / "jusu.spec.toml"
    # run non-interactive to use defaults
    cli.init(spec_file=spec_path, interactive=False)
    assert spec_path.exists()
    text = spec_path.read_text(encoding="utf-8")
    assert 'Francis Jusu' in text
    assert 'package = "com.example.jusu"' in text
    assert 'package_type = "aab"' in text
