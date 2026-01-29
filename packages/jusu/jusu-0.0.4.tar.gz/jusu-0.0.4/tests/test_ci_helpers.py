from pathlib import Path
import os
import base64

from JUSU import ci_helpers


def test_setup_keystore(tmp_path, monkeypatch):
    # Create a fake keystore bytes
    fake_keystore = b"FAKE-KEYSTORE-BYTES"
    os.environ["ANDROID_KEYSTORE_BASE64"] = base64.b64encode(fake_keystore).decode("ascii")
    os.environ["ANDROID_KEYSTORE_PASSWORD"] = "storepass"
    os.environ["ANDROID_KEY_ALIAS"] = "alias"
    os.environ["ANDROID_KEY_PASSWORD"] = "keypass"

    keystore_path = ci_helpers.setup_keystore(tmp_path, keystore_name="k.jks")
    assert keystore_path.exists()
    props = (tmp_path / "keystore.properties").read_text(encoding="utf-8")
    assert "storeFile=k.jks" in props
    assert "storePassword=storepass" in props
    assert "keyAlias=alias" in props
    assert "keyPassword=keypass" in props

    # Clean up env
    del os.environ["ANDROID_KEYSTORE_BASE64"]
    del os.environ["ANDROID_KEYSTORE_PASSWORD"]
    del os.environ["ANDROID_KEY_ALIAS"]
    del os.environ["ANDROID_KEY_PASSWORD"]
