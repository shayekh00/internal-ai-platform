from langchain.tools import tool
from sixtai.cli.agent import init as cli_init
import re

@tool
def init_agent(command: str) -> str:
    """
    Create an agent project from natural language command.
    Example input: 'Create an agent called support-bot using langchain with key sk-xyz'
    """
    try:
        name_match = re.search(r"(called|named)\s+([a-zA-Z0-9\-_]+)", command, re.IGNORECASE)
        template_match = re.search(r"using\s+([a-zA-Z0-9\-_]+)", command, re.IGNORECASE)
        key_match = re.search(r"(?:key|api[-_\s]*key)\s+(sk-[\w\-]+)", command, re.IGNORECASE)

        if not name_match:
            return "❌ Could not extract agent name from input. Try: 'called support-bot'"

        name = name_match.group(2)
        template = template_match.group(1) if template_match else "langchain"
        api_key = key_match.group(1) if key_match else ""

        print(f"🚧 Creating agent '{name}' with template '{template}' and API key '{api_key}'...")

        # ✅ Direct function call now
        cli_init(name=name, template=template, api_key=api_key)

        return f"✅ Agent '{name}' created with template '{template}'."
    except Exception as e:
        return f"❌ Failed to create agent: {str(e)}"
