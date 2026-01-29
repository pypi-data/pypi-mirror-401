from __future__ import annotations

import os
from pathlib import Path


def setup_keystore(target_dir: Path, keystore_name: str = "keystore.jks") -> Path:
    """Decode keystore from env var ANDROID_KEYSTORE_BASE64 and write a keystore
    and `keystore.properties` file into `target_dir`.

    Returns the path to the keystore file created.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    b64 = os.environ.get("ANDROID_KEYSTORE_BASE64")
    if not b64:
        raise RuntimeError("ANDROID_KEYSTORE_BASE64 not set")

    keystore_path = target_dir / keystore_name
    props_path = target_dir / "keystore.properties"

    # Decode base64
    data = b64.encode("utf-8")
    import base64

    with keystore_path.open("wb") as f:
        f.write(base64.b64decode(data))

    storepass = os.environ.get("ANDROID_KEYSTORE_PASSWORD", "")
    alias = os.environ.get("ANDROID_KEY_ALIAS", "")
    keypass = os.environ.get("ANDROID_KEY_PASSWORD", "")

    with props_path.open("w", encoding="utf-8") as f:
        f.write(f"storeFile={keystore_name}\n")
        f.write(f"storePassword={storepass}\n")
        f.write(f"keyAlias={alias}\n")
        f.write(f"keyPassword={keypass}\n")

    return keystore_path


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("target_dir")
    p.add_argument("--keystore", default="keystore.jks")
    args = p.parse_args()
    print("Setting up keystore in", args.target_dir)
    print(setup_keystore(Path(args.target_dir), keystore_name=args.keystore))
