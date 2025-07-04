# SixtAI CLI: Internal AI Developer Platform

The `sixtai` CLI is a self-service platform for AI/LLM engineers to scaffold, test, deploy, and debug agent-based applications with ease. Inspired by tools like Replit, LangChain, MLflow, and GitHub Copilot, `sixtai` aims to bring an AI-native developer experience to enterprise teams.

---

## 🚀 Features

- Scaffold new agent apps with built-in templates
- Automatically generate config (`sixtai.yaml`) and secret management (`.env`)
- Run prompt-based tests and log latency, cost, and responses
- Analyze failures using an LLM-powered assistant
- Modular, extensible CLI built with Typer

---

## 📦 Requirements

- Python 3.8+
- `pip install -e .` from the root directory

---

## 🛠️ Installation

```bash
# Clone the repo
cd llmops-internal-dev-platform
pip install -e .
```

After installing, the `sixtai` CLI becomes globally available:

```bash
sixtai --help
```

---

## 🧱 Directory Structure (Example)

```
llmops-internal-dev-platform/
├── sixtai/                # CLI source code
│   └── cli/
│       ├── agent.py
│       ├── deploy.py
│       ├── config.py
│       └── assistant.py
├── templates/
│   ├── langchain_template/
│   └── fastapi_template/
├── support-bot/           # Generated agent project
│   ├── main.py
│   ├── sixtai.yaml
│   ├── .env
│   └── logs.jsonl
```

---

## 🔧 Usage

### 1. Scaffold a New Agent

```bash
sixtai agent init support-bot --template=langchain --api-key=< YOUR OPENAI_API_KEY >
```

This creates:

- A scaffolded `main.py`
- A `sixtai.yaml` with LLM config
- A `.env` with your OpenAI key

---

### 2. Test Your Agent

```bash
sixtai agent test support-bot --prompt="How do I cancel a booking?"
```

- Runs the prompt against your agent
- Logs response, latency, and deploy ID

---

### 3. View Logs

```bash
sixtai agent logs support-bot
```

- View average latency, failure rate, and recent prompt runs

---

## 🧩 Templates

Available via `--template=`:

- `langchain`: LLM agent scaffold using LangChain
- `fastapi`: (WIP) Serve agents as REST APIs -------updates coming
- `rag`: (WIP) Retrieval-augmented generation pipelines ------updates coming

---

## 🔐 Secret Management

Use `.env` inside each agent project:

```
OPENAI_API_KEY=sk-xxx
PINECONE_API_KEY=xyz
```

Secrets are loaded automatically with `dotenv` during test and deploy.

---

## 📌 Roadmap

- Prompt regression testing
- Agent orchestration (`compose`)
- CI/CD safety + eval hooks
- Model cost tracking and token accounting
- Multi-provider support (Anthropic, OpenRouter, Mistral)

---

## 🧠 Philosophy

> "Not just infrastructure abstraction — developer acceleration."

`sixtai` is designed to make AI engineers **build fast, test confidently, and deploy safely**. It’s DevOps meets LLMOps, with an agent-native mindset.

---

## License

MIT

