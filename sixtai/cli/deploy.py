# sixtai/cli/deploy.py

import typer

deploy_app = typer.Typer(help="Deployment commands")

@deploy_app.command("start")
def start(name: str, env: str = "staging"):
    typer.echo(f"🚀 Pretending to deploy {name} to {env}...")
    typer.echo("✅ Deployed. Use 'explain-failure' to debug if needed.")
