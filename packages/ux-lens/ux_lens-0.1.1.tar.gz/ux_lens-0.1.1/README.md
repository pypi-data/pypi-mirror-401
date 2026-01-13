# UX Lens

An MCP server that captures browser interactions and uses Gemini 3 Flash Preview to provide comprehensive UX/frontend critique.

## What it does

1. Launches a browser and records your interaction with any website
2. Sends the video to Gemini 3 Flash Preview for analysis
3. Returns detailed UX/frontend feedback

## Installation

```bash
# Clone and install
git clone https://github.com/nice-bills/ux-lens.git
cd ux-lens
uv tool install .
```

## Configuration

This tool requires a Gemini API key. You can also optionally configure the model.

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (Required)
- `GEMINI_MODEL`: The model to use (Optional, defaults to `gemini-3-flash-preview`)

## Usage

### With MCP Clients (Claude Code, Gemini CLI)

Add to your MCP configuration (e.g., `~/.gemini/settings.json` or `claude_code_config.json`):

```json
{
  "mcpServers": {
    "ux-watcher": {
      "command": "ux-watcher",
      "env": {
        "GEMINI_API_KEY": "your-key-here",
        "GEMINI_MODEL": "gemini-3-flash-preview"
      }
    }
  }
}
```

Then simply ask the assistant:

> "Check the UX of https://example.com"

### Direct CLI

If you have installed it as a tool, you can run the server directly:

```bash
ux-watcher
```

## Requirements

- Python 3.11+
- Chromium browser (installed automatically by Playwright)
- Gemini API key

## License

MIT
