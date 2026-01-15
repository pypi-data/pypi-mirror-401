"""UAIP CLI."""
import shutil
from pathlib import Path
import click

TEMPLATE_NAME = "mini_store"


def _copy_template(dest: Path) -> None:
    src_root = Path(__file__).parent / "templates" / TEMPLATE_NAME
    if not src_root.exists():
        raise RuntimeError(f"Template not found: {src_root}")
    shutil.copytree(src_root, dest, dirs_exist_ok=False)


@click.group()
def cli():
    """UAIP command line tools."""
    pass


@cli.command()
@click.argument("name")
def init(name: str):
    """Scaffold a minimal UAIP workflow project."""
    dest = Path(name).resolve()
    if dest.exists():
        raise click.ClickException(f"Path already exists: {dest}")
    _copy_template(dest)
    click.echo(f"Created UAIP project at {dest}")
    click.echo("Next steps:")
    click.echo(f"  cd {dest}")
    click.echo("  python main.py")


if __name__ == "__main__":
    cli()
