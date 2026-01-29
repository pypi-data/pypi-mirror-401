from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import typer
import tomllib

flutter_app = typer.Typer(help="Flutter scaffold & build commands for JUSU")


def _read_spec(spec_path: Path) -> dict:
    if not spec_path.exists():
        return {}
    with spec_path.open("rb") as f:
        return tomllib.load(f)


@flutter_app.command()
def init(
    project_dir: Path = typer.Option(Path("./jusu_flutter_app"), help="Directory to create the Flutter project in"),
    app_id: str = typer.Option("com.example.jusu", help="Android package id"),
    app_name: str = typer.Option("JUSUApp", help="Application display name"),
    install: bool = typer.Option(False, help="Run `flutter pub get` after creating the project"),
    spec: Path | None = typer.Option(None, help="Optional path to a spec file to apply"),
):
    """Create a minimal Flutter project scaffold for JUSU.

    The template is a thin Flutter app that loads a web bundle from
    `assets/www/index.html` and communicates with a JUSU worker over HTTP.
    """
    project_dir = Path(project_dir)
    if project_dir.exists():
        if not typer.confirm(f"{project_dir} already exists — overwrite?", abort=False):
            typer.echo("Aborting: project not created.")
            raise typer.Exit()
        shutil.rmtree(project_dir)

    template_dir = Path(__file__).parent.parent / "scripts" / "flutter-template"
    if not template_dir.exists():
        typer.echo("Error: Flutter template missing in scripts/flutter-template")
        raise typer.Exit(code=2)

    shutil.copytree(template_dir, project_dir)

    # Apply spec values if provided
    # Typer Option defaults can expose OptionInfo when the function is called directly; normalize.
    if getattr(spec, "help", None) is not None:
        spec = None
    if spec is None:
        spec_path = Path("jusu.spec.toml")
        if spec_path.exists():
            spec = spec_path
    if spec:
        data = _read_spec(Path(spec))
        app_section = data.get("app", {})
        flutter_section = data.get("flutter", {})
        # Replace simple tokens in android manifest / pubspec if present
        # For PoC we only update pubspec name and the app name in main.dart
        pubspec = project_dir / "pubspec.yaml"
        if pubspec.exists():
            text = pubspec.read_text(encoding="utf-8")
            if "name:" in text and app_section.get("name"):
                text = text.replace("name: jusu_app_template", f"name: {app_section.get('name').lower().replace(' ', '_')}")
            pubspec.write_text(text, encoding="utf-8")
        main = project_dir / "lib" / "main.dart"
        if main.exists() and app_section.get("name"):
            text = main.read_text(encoding="utf-8")
            text = text.replace("JUSU App", app_section.get("name"))
            main.write_text(text, encoding="utf-8")

    typer.echo(f"Created Flutter project at {project_dir}")

    if install:
        typer.echo("Running flutter pub get...")
        subprocess.run(["flutter", "pub", "get"], check=True, cwd=str(project_dir))


@flutter_app.command()
def build(
    project_dir: Path = typer.Option(Path("./jusu_flutter_app"), help="Flutter project directory"),
    build_mode: str = typer.Option("apk", help="Build type: apk | appbundle"),
    bundle_dir: Path | None = typer.Option(None, help="Path to the web bundle directory (optional)"),
    run_sync: bool = typer.Option(False, help="If True, copy bundle assets before building"),
    spec: Path | None = typer.Option(None, help="Optional path to jusu.spec.toml"),
):
    """Build the Flutter project (Android)."""
    project_dir = Path(project_dir)
    if not project_dir.exists():
        typer.echo("Error: Flutter project directory does not exist. Run `jusu flutter init` first.")
        raise typer.Exit(code=2)

    # Normalize `spec` if it was supplied as an OptionInfo by Typer when called directly
    if getattr(spec, "help", None) is not None:
        spec = None
    if spec is None:
        spec_path = Path("jusu.spec.toml")
        if spec_path.exists():
            spec = spec_path

    # If a bundle_dir is provided, copy into assets/www
    if bundle_dir and run_sync:
        src = Path(bundle_dir)
        dst = project_dir / "assets" / "www"
        dst.mkdir(parents=True, exist_ok=True)
        # copy files
        for item in src.iterdir():
            if item.is_file():
                shutil.copy2(item, dst / item.name)
        typer.echo(f"Copied bundle files from {src} to {dst}")

    # Determine build command
    if build_mode == "apk":
        cmd = ["flutter", "build", "apk", "--release"]
    elif build_mode in ("aab", "appbundle"):
        cmd = ["flutter", "build", "appbundle", "--release"]
    else:
        typer.echo("Unknown build mode. Use 'apk' or 'appbundle'.")
        raise typer.Exit(code=2)

    typer.echo(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=str(project_dir))
    typer.echo("Build finished. Check build/outputs in the Flutter project.")
