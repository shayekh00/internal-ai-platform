# sixtai/cli/main.py

import typer
from .agent import agent_app
from .deploy import deploy_app

app = typer.Typer()
app.add_typer(agent_app, name="agent")
app.add_typer(deploy_app, name="deploy")

def main():
    app()

if __name__ == "__main__":
    main()
