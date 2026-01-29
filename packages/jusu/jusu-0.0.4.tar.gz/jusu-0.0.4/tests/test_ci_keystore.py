from pathlib import Path
import os
import base64

from JUSU import ci_keystore


def test_setup_keystore(tmp_path, monkeypatch):
    # Create a fake keystore binary
    keystore_bin = b"fake-keystore-bytes"
    b64 = base64.b64encode(keystore_bin).decode("ascii")
    monkeypatch.setenv("ANDROID_KEYSTORE_BASE64", b64)
    monkeypatch.setenv("ANDROID_KEYSTORE_PASSWORD", "storepass")
    monkeypatch.setenv("ANDROID_KEY_ALIAS", "myalias")
    monkeypatch.setenv("ANDROID_KEY_PASSWORD", "keypass")

    target_dir = tmp_path / "android"
    keystore_path = tmp_path / "android" / "app" / "keystore.jks"

    ci_keystore.setup_keystore(target_dir, keystore_path)

    assert keystore_path.exists()
    assert (target_dir / "key.properties").exists()
    content = (target_dir / "key.properties").read_text(encoding="utf-8")
    assert "storePassword=storepass" in content
    assert "keyAlias=myalias" in content
    # verify keystore bytes written
    assert keystore_path.read_bytes() == keystore_bin


def test_skip_when_no_env(tmp_path, monkeypatch):
    # Ensure nothing is created if no env var provided
    monkeypatch.delenv("ANDROID_KEYSTORE_BASE64", raising=False)
    target_dir = tmp_path / "android"
    keystore_path = tmp_path / "android" / "app" / "keystore.jks"
    ci_keystore.setup_keystore(target_dir, keystore_path)
    assert not keystore_path.exists()
    assert not (target_dir / "key.properties").exists()
