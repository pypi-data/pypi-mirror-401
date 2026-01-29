from __future__ import annotations

import base64
import os
from pathlib import Path
import argparse


def setup_keystore(target_dir: Path, keystore_path: Path) -> None:
    """Decode keystore from environment variables and write key.properties.

    Expects these environment variables to be set:
      ANDROID_KEYSTORE_BASE64 (base64-encoded keystore file)
      ANDROID_KEYSTORE_PASSWORD
      ANDROID_KEY_ALIAS
      ANDROID_KEY_PASSWORD

    If `ANDROID_KEYSTORE_BASE64` is not set, the function does nothing and
    returns gracefully.
    """
    target_dir = Path(target_dir)
    keystore_path = Path(keystore_path)

    b64 = os.environ.get("ANDROID_KEYSTORE_BASE64")
    if not b64:
        print("ANDROID_KEYSTORE_BASE64 not set; skipping keystore setup")
        return

    store_password = os.environ.get("ANDROID_KEYSTORE_PASSWORD", "")
    key_alias = os.environ.get("ANDROID_KEY_ALIAS", "")
    key_password = os.environ.get("ANDROID_KEY_PASSWORD", "")

    keystore_path.parent.mkdir(parents=True, exist_ok=True)
    with open(keystore_path, "wb") as f:
        f.write(base64.b64decode(b64))

    # Write key.properties in target_dir
    key_props = target_dir / "key.properties"
    key_props.write_text(
        f"storePassword={store_password}\nkeyPassword={key_password}\nkeyAlias={key_alias}\nstoreFile={keystore_path}\n",
        encoding="utf-8",
    )
    print(f"Wrote keystore to: {keystore_path}")
    print(f"Wrote key.properties to: {key_props}")


def main():
    p = argparse.ArgumentParser(prog="jusu-ci-keystore")
    p.add_argument("--target-dir", type=Path, required=True, help="Directory to write key.properties into")
    p.add_argument("--keystore-path", type=Path, required=True, help="Where to write the keystore (.jks) file")
    args = p.parse_args()
    setup_keystore(args.target_dir, args.keystore_path)


if __name__ == "__main__":
    main()
