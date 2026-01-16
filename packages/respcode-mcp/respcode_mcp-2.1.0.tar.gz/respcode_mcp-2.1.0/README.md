# RespCode MCP Server

Multi-architecture code execution for Claude Desktop via MCP.

## Installation
```bash
pip install respcode-mcp
```

## Setup

1. Get your API key at [respcode.com](https://respcode.com)

2. Configure Claude Desktop (`~/.config/claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "respcode": {
      "command": "respcode-mcp",
      "env": {
        "RESPCODE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

3. Restart Claude Desktop

## Available Tools

| Tool | Description | Credits |
|------|-------------|---------|
| `generate` | AI generates & executes code | 2-6 |
| `execute` | Run your own code | 1 |
| `compete` | Compare 4 AI models | ~15 |
| `collaborate` | Models refine each other | ~12 |
| `consensus` | Best-of-4 selection | ~15 |
| `history` | View past prompts | 0 |
| `credits` | Check balance | 0 |

## Architectures

- x86_64 (Intel/AMD)
- ARM64 (Apple Silicon, Raspberry Pi)
- RISC-V 64
- ARM32
- Verilog/VHDL simulation

## Example Usage in Claude

> "Generate a fibonacci function in Rust and run it on ARM64"

> "Compare all 4 AI models writing quicksort in C"

> "Execute this code on RISC-V: print('Hello RISC-V')"

## Links

- Website: https://respcode.com
- Docs: https://docs.respcode.com
- API: https://respcode.com/api
