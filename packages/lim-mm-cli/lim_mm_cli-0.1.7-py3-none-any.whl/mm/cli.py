import typer
from typing import Optional
from mm.core import (
    start_project, 
    run_project, 
    push_project, 
    validate_project, 
    build_project, 
    pull_project, 
    list_project
)

app = typer.Typer()


@app.command()
def start(name: str):
    """Create a new micro model project from template"""
    start_project(name)


@app.command()
def validate():
    """Verify MM compliance (checks /meta.json service health)"""
    validate_project()


@app.command()
def build():
    """Containerize the current MM"""
    build_project()


@app.command()
def run():
    """Execute the project locally (python run/start.py)"""
    run_project()


@app.command()
def push():
    """Publish the MM to the LIM repository"""
    push_project()


@app.command()
def pull(mms: str):
    """Retrieve MMs into local models/ directory"""
    # mms is comma separated string according to README "mm pull <mm1,mm2>"
    mm_list = [m.strip() for m in mms.split(",")]
    pull_project(mm_list)


@app.command("list")
def list_cmd(name: Optional[str] = typer.Argument(None)):
    """Display metadata and status of an MM"""
    list_project(name)


if __name__ == "__main__":
    app()
