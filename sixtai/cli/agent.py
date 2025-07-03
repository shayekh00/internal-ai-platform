# sixtai/cli/agent.py

import typer
from pathlib import Path
import importlib.util
import time
import json
import uuid
from .observability import load_logs, summarize_logs, print_summary
from .assistant import explain_failure
from .config import load_config
import yaml
from dotenv import load_dotenv
import shutil

agent_app = typer.Typer(help="Agent-related commands")

@agent_app.command("init")
def init(
    name: str,
    template: str = typer.Option("langchain", "--template", "-t", help="Template type (e.g. langchain, fastapi)"),
    api_key: str = typer.Option(None, "--api-key", help="OpenAI API key to prefill in .env file")
):
    """Scaffold a new agent project."""
    import shutil
    import yaml
    src = Path(__file__).parent.parent / "templates" / f"{template}_template"
    dst = Path.cwd() / name

    if dst.exists():
        typer.echo("❌ Project already exists.")
        raise typer.Exit()

    shutil.copytree(src, dst)

    # Generate sixtai.yaml
    config = {
        "name": name,
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.2
        },
        "deployment": {
            "env": "staging",
            "autoscale": True
        },
        "observability": {
            "evals": True
        }
    }
    with open(dst / "sixtai.yaml", "w") as f:
        yaml.dump(config, f, sort_keys=False)

    # Write .env with optional key
    with open(dst / ".env", "w") as f:
        f.write("# Add your API keys here\n")
        if api_key:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        else:
            f.write("OPENAI_API_KEY=\n")

    typer.echo(f"✅ Created agent '{name}' with template '{template}'")
    if not api_key:
        typer.echo("⚠️  Remember to add your OPENAI_API_KEY in .env")



@agent_app.command("test")
def test_agent(name: str, prompt: str = typer.Option(..., "--prompt", "-p")):
    """Run a test prompt against the agent."""

    config = load_config(name)
    llm_config = config.get("llm", {})

    # Dynamically import the agent
    agent_file = Path.cwd() / name / "main.py"
    spec = importlib.util.spec_from_file_location("agent_main", agent_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    start = time.time()
    response = mod.run_agent(prompt)
    latency = time.time() - start

    log = {
        "timestamp": time.time(),
        "agent": name,
        "prompt": prompt,
        "response": response,
        "latency": latency,
        "deploy_id": f"deploy/{str(uuid.uuid4())[:8]}"
    }
    with open(Path.cwd() / name / "logs.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")

    typer.echo(f"🤖 {response}\n⏱️ {latency:.2f}s")


@agent_app.command("logs")
def show_logs(name: str):
    logs = load_logs(name)
    summary = summarize_logs(logs)
    print_summary(summary)

@agent_app.command("explain-failure")
def explain(deploy_id: str):
    logs = []
    for agent in Path.cwd().iterdir():
        if agent.is_dir():
            try:
                logs += load_logs(agent.name)
            except:
                pass
    match = next((log for log in logs if log.get("deploy_id") == deploy_id), None)
    if not match:
        typer.echo("❌ Deploy ID not found.")
        raise typer.Exit()
    typer.echo(f"🧾 Prompt: {match['prompt']}")
    typer.echo(f"🧠 Response: {match['response'][:200]}")
    result = explain_failure(match["prompt"], match["response"], match["latency"])
    typer.echo(f"🧠 Assistant Suggestion:\n{result}")


def load_config(agent_name: str) -> dict:
    base_path = Path.cwd() / agent_name
    config_path = base_path / "sixtai.yaml"
    env_path = base_path / ".env"

    if not config_path.exists():
        raise FileNotFoundError(f"❌ No sixtai.yaml found for {agent_name}")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Load .env if it exists
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    return config