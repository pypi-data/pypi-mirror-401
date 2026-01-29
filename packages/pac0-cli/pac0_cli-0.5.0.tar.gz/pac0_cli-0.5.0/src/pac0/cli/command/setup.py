import typer
from pathlib import Path
import subprocess

app = typer.Typer()

DEFAULT_REPO_URL = "https://github.com/paxpar-tech/PA_Communautaire"


@app.command()
def tool():
    """Vérifie les versions d'outils et les installe si besoin"""
    typer.echo("Vérification des outils...")
    raise NotImplementedError()


@app.command()
def source(
    repo_url: str = DEFAULT_REPO_URL,
    target_dir: str = '.',
    uv_sync: bool = True,
):
    """Clone le dépôt git"""
    subprocess.call(["git", "clone", repo_url], cwd=target_dir)
    app_base_dir = Path(target_dir) / Path(repo_url).name
    if uv_sync:
        subprocess.call(["uv", "sync", "--all-packages"], cwd=app_base_dir)
