# A4E MCP Server

[![PyPI version](https://badge.fury.io/py/a4e.svg)](https://badge.fury.io/py/a4e)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A4E MCP Server** enables you to build AI agents using natural language directly in your IDE (Cursor, VS Code, Claude Desktop).

## Quick Start

### 1. Install

```bash
pip install a4e
```

### 2. Configure your IDE

```bash
# For Cursor
a4e mcp setup cursor

# For Claude Desktop
a4e mcp setup claude-desktop

# For VS Code
a4e mcp setup vscode
```

### 3. Restart your IDE

After restarting, A4E tools will be available to your AI assistant.

### 4. Start building!

In your IDE chat, try:

```
Create an agent called "nutrition-coach" that helps users track meals and calculate calories.
```

## Features

- **22 MCP Tools** for agent development
- **CLI** for quick commands (`a4e init`, `a4e add tool`, etc.)
- **Hot-reload dev server** for rapid iteration
- **Auto-schema generation** from Python code and TypeScript
- **One-click deployment** to A4E Cloud

## Usage

### With MCP (AI Assistant)

Once configured, ask your AI assistant to:

- "Create a new agent called my-assistant"
- "Add a tool to calculate BMI"
- "Add a view to display results"
- "Start the development server"
- "Validate and deploy the agent"

### With CLI

```bash
# Initialize a new agent
a4e init

# Add components
a4e add tool calculate_bmi
a4e add view bmi_result
a4e add skill show_bmi

# Development
a4e dev start

# Validate and deploy
a4e validate
a4e deploy
```

## MCP Configuration

### Automatic Setup (Recommended)

```bash
a4e mcp setup cursor      # For Cursor
a4e mcp setup claude-desktop  # For Claude Desktop
a4e mcp setup vscode      # For VS Code
```

### Manual Setup

<details>
<summary>Cursor (~/.cursor/mcp.json)</summary>

```json
{
  "mcpServers": {
    "a4e": {
      "command": "/path/to/python",
      "args": ["-m", "a4e.server"],
      "env": {
        "A4E_WORKSPACE": "${workspaceFolder}"
      }
    }
  }
}
```

</details>

<details>
<summary>Claude Desktop</summary>

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "a4e": {
      "command": "/path/to/python",
      "args": ["-m", "a4e.server"]
    }
  }
}
```

</details>

## Concepts

### Agent Structure

```
my-agent/
├── agent.py           # Agent configuration
├── metadata.json      # Agent metadata
├── prompts/
│   └── agent.md       # System prompt
├── tools/
│   ├── my_tool.py     # Custom tools
│   └── schemas.json   # Auto-generated
├── views/
│   ├── my_view/
│   │   └── view.tsx   # React components
│   └── schemas.json   # Auto-generated
└── skills/
    ├── my_skill/
    │   └── SKILL.md   # Skill documentation
    └── schemas.json   # Auto-generated
```

### Tools

Python functions that give the agent capabilities:

```python
from a4e.sdk import tool

@tool
def calculate_bmi(params: dict) -> dict:
    """Calculate BMI from height and weight."""
    height = params.get("height_m")
    weight = params.get("weight_kg")
    bmi = weight / (height ** 2)
    return {"bmi": round(bmi, 1)}
```

### Views

React components for rich UI:

```tsx
interface BMIResultProps {
  bmi: number;
  category: string;
}

export default function BMIResult({ bmi, category }: BMIResultProps) {
  return (
    <div>
      <h2>Your BMI: {bmi}</h2>
      <p>Category: {category}</p>
    </div>
  );
}
```

### Skills

Connect intents to tools and views:

```yaml
id: show_bmi
name: Show BMI Result
intent_triggers:
  - calculate my bmi
  - what's my bmi
internal_tools:
  - calculate_bmi
output:
  view: bmi_result
```

## Development

### Dev Server

Start a local development server with hot-reload:

```bash
a4e dev start
```

This starts:
- Local server at `http://localhost:5000`
- ngrok tunnel for external access
- File watcher for hot-reload

### Validation

Check your agent before deployment:

```bash
a4e validate
```

## Requirements

- Python 3.11+
- pip or uv
- ngrok account (for dev server tunneling)

## CLI Commands

| Command | Description |
|---------|-------------|
| `a4e init` | Initialize new agent (interactive) |
| `a4e add tool` | Add a tool |
| `a4e add view` | Add a view |
| `a4e add skill` | Add a skill |
| `a4e list [tools\|views\|skills]` | List components |
| `a4e remove [tool\|view\|skill]` | Remove component |
| `a4e update [tool\|view\|skill]` | Update component |
| `a4e validate` | Validate agent |
| `a4e deploy` | Deploy to production |
| `a4e dev start` | Start dev server |
| `a4e mcp setup <ide>` | Configure MCP for IDE |
| `a4e mcp show <ide>` | Show MCP config |
| `a4e mcp test` | Test MCP server |

## Troubleshooting

### "a4e: command not found"

Ensure pip scripts are in your PATH:

```bash
# Check where pip installs scripts
python -m site --user-base
# Add to PATH (example for bash)
export PATH="$HOME/.local/bin:$PATH"
```

### MCP not connecting

1. Run `a4e mcp test` to verify server works
2. Check config with `a4e mcp show cursor`
3. Restart your IDE after configuration changes

### ngrok issues

For dev server, ensure ngrok is configured:

```bash
ngrok config add-authtoken YOUR_TOKEN
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Documentation](https://github.com/simetrik-inc-public/a4e-mcp-server#readme)
- [Issues](https://github.com/simetrik-inc-public/a4e-mcp-server/issues)
- [PyPI](https://pypi.org/project/a4e/)
