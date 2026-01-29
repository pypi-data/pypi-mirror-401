"""Android packaging helpers for JUSU (Capacitor wrapper).

Provides simple commands to scaffold a Capacitor project and run builds to
produce APK/AAB artifacts using Node/Capacitor/Gradle. The Python code acts as
a convenience wrapper and does not replace the native Android tooling which
must be installed by the user (Node.js, Java JDK, Android SDK/NDK).
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import typer

android_app = typer.Typer(help="Build Android APK/AAB using Capacitor")


@android_app.command("init")
def android_init(
    project_dir: Path = typer.Option(Path("android_app"), help="Directory to scaffold the Capacitor project"),
    app_id: str = typer.Option("com.example.jusu", help="Android application id"),
    app_name: str = typer.Option("JUSUApp", help="Application display name"),
    install: bool = typer.Option(False, help="Run `npm install` in the scaffolded project (requires npm)"),
    spec: Optional[Path] = typer.Option(None, help="Path to a `jusu.spec.toml` to read defaults from"),
) -> None:
    """Scaffold a minimal Capacitor project that can host the exported JUSU bundle.

    This command copies the bundled template from `scripts/android/capacitor-template`
    and fills in basic capacitor config. It does not modify your system (no SDK
    changes) and will only run `npm install` if explicitly requested.
    """
    # If a spec is provided, try to load values
    if spec is not None and isinstance(spec, (str, Path)):
        try:
            import tomllib
        except Exception:
            tomllib = None
        if tomllib is None:
            typer.echo("Unable to read spec file: tomllib not available on this Python version.")
            raise typer.Exit(code=2)
        spec_path = Path(spec)
        if not spec_path.exists():
            typer.echo(f"Spec file {spec} not found.")
            raise typer.Exit(code=2)
        data = tomllib.loads(spec_path.read_text(encoding="utf-8"))
        app_id = data.get("android", {}).get("package", app_id)
        app_name = data.get("app", {}).get("name", app_name)
    """Scaffold a minimal Capacitor project that can host the exported JUSU bundle.

    This command copies the bundled template from `scripts/android/capacitor-template`
    and fills in basic capacitor config. It does not modify your system (no SDK
    changes) and will only run `npm install` if explicitly requested.
    """
    here = Path(__file__).resolve().parent
    template = here.parent / "scripts" / "android" / "capacitor-template"
    if not template.exists():
        typer.echo("Capacitor template not found in repository (scripts/android/capacitor-template)")
        raise typer.Exit(code=2)

    project_dir = project_dir.resolve()
    if project_dir.exists():
        typer.confirm(f"Directory {project_dir} already exists. Overwrite?", abort=True)
        shutil.rmtree(project_dir)

    shutil.copytree(template, project_dir)
    # Fill basic config (package.json and capacitor.config.json)
    pkg = project_dir / "package.json"
    if pkg.exists():
        text = pkg.read_text(encoding="utf-8")
        text = text.replace("__APP_ID__", app_id).replace("__APP_NAME__", app_name)
        pkg.write_text(text, encoding="utf-8")

    cap = project_dir / "capacitor.config.json"
    if cap.exists():
        text = cap.read_text(encoding="utf-8")
        text = text.replace("__APP_ID__", app_id).replace("__APP_NAME__", app_name)
        cap.write_text(text, encoding="utf-8")

    typer.echo(f"Scaffolded Capacitor project at: {project_dir}")

    if install:
        typer.echo("Running `npm install` (this may take a while)...")
        res = subprocess.run(["npm", "install"], cwd=str(project_dir))
        if res.returncode != 0:
            typer.echo("`npm install` failed. Please run it manually and ensure Node.js is installed.")
            raise typer.Exit(code=3)
        typer.echo("Dependencies installed.")


@android_app.command("build")
def android_build(
    project_dir: Path = typer.Option(Path("android_app"), help="Capacitor project directory (created by `jusu android init`)"),
    bundle_dir: Optional[Path] = typer.Option(None, help="Directory containing HTML/CSS bundle to copy into the Capacitor 'www' folder (defaults to 'dist' or project 'www')"),
    build_type: str = typer.Option("debug", help="Build type: debug or release"),
    run_sync: bool = typer.Option(True, help="Run `npx cap sync` before building to copy assets"),
    spec: Optional[Path] = typer.Option(None, help="Path to `jusu.spec.toml` to load build defaults from (auto-detected if omitted)"),
) -> None:
    """Build the Android app (APK/AAB) using Capacitor + Gradle.

    This function copies the web bundle into the Capacitor `www` folder, runs
    `npx cap sync` to sync, and then runs the Gradle build (`npx cap build android`).
    The environment must have Node.js and Android build tools installed.
    """
    project_dir = project_dir.resolve()
    if not project_dir.exists():
        typer.echo(f"Capacitor project not found at {project_dir}. Run `jusu android init` first.")
        raise typer.Exit(code=2)

    www_dir = project_dir / "www"
    www_dir.mkdir(parents=True, exist_ok=True)

    # If a spec is provided or present in cwd, try to load values (auto-detect)
    spec_path = None
    if spec is not None and isinstance(spec, (str, Path)):
        spec_path = Path(spec)
    else:
        # prefer project-local spec, then workspace cwd
        p1 = project_dir / "jusu.spec.toml"
        p2 = Path.cwd() / "jusu.spec.toml"
        spec_path = p1 if p1.exists() else (p2 if p2.exists() else None)

    if spec_path is not None:
        try:
            import tomllib
            data = tomllib.loads(spec_path.read_text(encoding="utf-8"))
            pkg = data.get("android", {}).get("package")
            if pkg:
                typer.echo(f"Using android package from spec: {pkg}")
        except Exception:
            # ignore parsing errors - not fatal
            typer.echo(f"Warning: failed to read spec file: {spec_path}")

    # Normalize bundle_dir in case Typer passed an OptionInfo object when called in tests
    if bundle_dir is not None and not isinstance(bundle_dir, (str, Path)):
        bundle_dir = None

    # Determine bundle source
    if bundle_dir is None:
        candidate = Path("dist")
        bundle_dir = candidate if candidate.exists() else None
    if bundle_dir is not None and (not Path(bundle_dir).exists()):
        typer.echo(f"Bundle directory {bundle_dir} does not exist.")
        raise typer.Exit(code=3)

    if bundle_dir:
        # copy bundle contents into www
        typer.echo(f"Copying bundle from {bundle_dir} into {www_dir}...")
        # remove existing contents
        for child in www_dir.iterdir():
            if child.is_file():
                child.unlink()
            else:
                shutil.rmtree(child)
        for src in Path(bundle_dir).iterdir():
            dest = www_dir / src.name
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)

    if run_sync:
        typer.echo("Running `npx cap sync android`...")
        res = subprocess.run(["npx", "cap", "sync", "android"], cwd=str(project_dir))
        if res.returncode != 0:
            typer.echo("`npx cap sync android` failed. Ensure Node + Capacitor are installed.")
            raise typer.Exit(code=4)

    # Now build
    typer.echo("Running `npx cap build android` (this invokes Gradle and may take several minutes)...")
    res = subprocess.run(["npx", "cap", "build", "android"], cwd=str(project_dir))
    if res.returncode != 0:
        typer.echo("Android build failed. Check Android SDK/Gradle configuration and try again.")
        raise typer.Exit(code=5)

    typer.echo("Android build completed. Check the Android project in the Capacitor project for APK/AAB outputs (android/app/build/outputs).")


@android_app.command("embed-worker")
def embed_worker(
    worker_src: Path = typer.Option(Path("./worker"), help="Directory containing Python worker sources"),
    chaquopy_project: Path = typer.Option(Path("./android_example"), help="Android project root where the worker should be embedded (Chaquopy)"),
):
    """Package a Python worker directory and embed it into an Android project prepared for Chaquopy.

    This command zips the worker sources (via `JUSU.embedded_worker.package_worker`),
    and extracts them into `app/src/main/python/` within the target Android project.
    """
    from . import embedded_worker

    worker_src = Path(worker_src)
    chaquopy_project = Path(chaquopy_project)

    if not worker_src.exists():
        typer.echo(f"Worker source directory not found: {worker_src}")
        raise typer.Exit(code=2)
    if not chaquopy_project.exists():
        typer.echo(f"Chaquopy Android project not found at: {chaquopy_project}")
        raise typer.Exit(code=2)

    out_zip = chaquopy_project / "build" / "jusu_worker.zip"
    out_zip.parent.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Packaging worker sources from {worker_src} -> {out_zip}...")
    embedded_worker.package_worker(worker_src, out_zip)

    # Extract into app/src/main/python/
    dest = chaquopy_project / "app" / "src" / "main" / "python"
    if dest.exists():
        # remove previous contents
        for child in dest.iterdir():
            if child.is_file():
                child.unlink()
            else:
                shutil.rmtree(child)
    else:
        dest.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Extracting worker into {dest}...")
    with __import__("zipfile").ZipFile(out_zip, "r") as z:
        z.extractall(dest)

    typer.echo("Worker embedded successfully into Chaquopy Android project.")
