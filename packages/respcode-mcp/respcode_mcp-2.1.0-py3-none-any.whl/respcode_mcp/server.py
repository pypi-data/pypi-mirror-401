#!/usr/bin/env python3
"""
RespCode MCP Server v2.1
========================
Updated to match actual RespCode backend API.
All modes generate AND execute by default.
"""

import asyncio
import os
import uuid
from pathlib import Path
from typing import Any, Optional
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

# =============================================================================
# CONFIG - MATCHES YOUR ACTUAL BACKEND
# =============================================================================

API_BASE_URL = os.environ.get("RESPCODE_API_URL", "https://respcode.com")
API_KEY = os.environ.get("RESPCODE_API_KEY", "")

# Model names - EXACTLY as your backend expects
MODELS = ["claude-sonnet-4-5", "gpt-4o", "deepseek-coder", "gemini-2.5-flash"]

# Simplified names users can type -> actual backend names
MODEL_ALIASES = {
    "claude": "claude-sonnet-4-5",
    "claude-sonnet": "claude-sonnet-4-5",
    "gpt4o": "gpt-4o",
    "gpt4": "gpt-4o",
    "gpt-4o": "gpt-4o",
    "openai": "gpt-4o",
    "deepseek": "deepseek-coder",
    "deepseek-coder": "deepseek-coder",
    "gemini": "gemini-2.5-flash",
    "gemini-flash": "gemini-2.5-flash",
    "gemini-2.5-flash": "gemini-2.5-flash",
}

# Languages supported
LANGUAGES = ["c", "cpp", "python", "verilog", "vhdl"]

# Architectures - EXACTLY as your backend expects (x86, not x86_64!)
ARCHITECTURES = ["x86", "arm64", "riscv64", "arm32", "verilog"]

MODEL_INFO = {
    "claude-sonnet-4-5": {"name": "Claude Sonnet 4.5", "emoji": "🟣"},
    "gpt-4o": {"name": "GPT-4o", "emoji": "🟢"},
    "deepseek-coder": {"name": "DeepSeek Coder", "emoji": "🔵"},
    "gemini-2.5-flash": {"name": "Gemini 2.5 Flash", "emoji": "🟡"},
}

ARCH_INFO = {
    "x86": {"emoji": "💻", "desc": "Intel/AMD (Daytona)"},
    "arm64": {"emoji": "🔥", "desc": "ARM64 (Firecracker)"},
    "riscv64": {"emoji": "⚡", "desc": "RISC-V 64 (QEMU)"},
    "arm32": {"emoji": "🔧", "desc": "ARM32 (Firecracker)"},
    "verilog": {"emoji": "🔌", "desc": "HDL Simulation (iverilog/ghdl)"},
}

server = Server("respcode")
http_client: Optional[httpx.AsyncClient] = None


def get_device_id() -> str:
    """Get or create persistent device ID for API tracking."""
    config_dir = Path.home() / ".config" / "respcode"
    config_dir.mkdir(parents=True, exist_ok=True)
    device_file = config_dir / "device_id"
    if device_file.exists():
        return device_file.read_text().strip()
    device_id = str(uuid.uuid4())
    device_file.write_text(device_id)
    return device_id


def resolve_model(model: str) -> str:
    """Resolve model alias to actual backend model name."""
    return MODEL_ALIASES.get(model.lower(), model)


async def get_client() -> httpx.AsyncClient:
    global http_client
    if http_client is None:
        if not API_KEY:
            raise ValueError("RESPCODE_API_KEY environment variable not set")
        http_client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "RespCode-MCP/2.1",
                "X-Device-Id": get_device_id(),
                "X-Client-Type": "mcp",
            },
            timeout=180.0,
        )
    return http_client


async def api_post(endpoint: str, data: dict) -> dict:
    client = await get_client()
    try:
        response = await client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        error_msg = ""
        try:
            error_data = e.response.json()
            error_msg = error_data.get("error", "") or error_data.get("message", "")
        except:
            error_msg = e.response.text[:200]
        return {"error": f"HTTP {e.response.status_code}: {error_msg}"}
    except Exception as e:
        return {"error": str(e)}


async def api_get(endpoint: str) -> dict:
    client = await get_client()
    try:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def error_result(msg: str) -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=f"❌ **Error:** {msg}")])


# =============================================================================
# TOOLS
# =============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate",
            description="Generate code with ONE AI model and execute it. Default: deepseek-coder on x86.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "What code to generate"},
                    "architecture": {
                        "type": "string",
                        "enum": ARCHITECTURES,
                        "default": "x86",
                        "description": "x86, arm64, riscv64, arm32, or verilog"
                    },
                    "model": {
                        "type": "string",
                        "enum": list(MODEL_ALIASES.keys()) + MODELS,
                        "default": "deepseek",
                        "description": "AI model (claude, gpt4o, deepseek, gemini)"
                    },
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="compete",
            description="Generate with ALL 4 AI models and execute each. Compare which produces best code!",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "What code to generate"},
                    "architecture": {
                        "type": "string",
                        "enum": ARCHITECTURES,
                        "default": "x86"
                    },
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="collaborate",
            description="Models work together: first generates, others refine, then execute final result.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "What code to generate"},
                    "architecture": {
                        "type": "string",
                        "enum": ARCHITECTURES,
                        "default": "x86"
                    },
                    "models": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "2-4 models in order (default: deepseek → claude)",
                        "default": ["deepseek", "claude"]
                    },
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="consensus",
            description="All 4 models generate solutions, Claude picks/merges best one, then execute.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "What code to generate"},
                    "architecture": {
                        "type": "string",
                        "enum": ARCHITECTURES,
                        "default": "x86"
                    },
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="execute",
            description="Execute YOUR code (no AI generation). Just run it on the sandbox. 1 credit.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Your source code to execute"},
                    "architecture": {
                        "type": "string",
                        "enum": ARCHITECTURES,
                        "default": "x86"
                    },
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="history",
            description="View your recent prompts and execution results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10, "description": "Number of items (max 50)"},
                },
            }
        ),
        Tool(
            name="history_search",
            description="Search your prompt history by keyword.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rerun",
            description="Re-run a previous prompt on a different architecture.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_id": {"type": "integer", "description": "Prompt ID from history"},
                    "architecture": {"type": "string", "enum": ARCHITECTURES},
                },
                "required": ["prompt_id", "architecture"]
            }
        ),
        Tool(
            name="credits",
            description="Check your credit balance and see pricing.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
    handlers = {
        "generate": handle_generate,
        "compete": handle_compete,
        "collaborate": handle_collaborate,
        "consensus": handle_consensus,
        "execute": handle_execute,
        "history": handle_history,
        "history_search": handle_history_search,
        "rerun": handle_rerun,
        "credits": handle_credits,
    }
    handler = handlers.get(name)
    if handler:
        return await handler(arguments)
    return error_result(f"Unknown tool: {name}")


# =============================================================================
# HANDLERS
# =============================================================================

async def handle_generate(args: dict) -> CallToolResult:
    """Single model generation + execution."""
    model = resolve_model(args.get("model", "deepseek-coder"))
    architecture = args.get("architecture", "x86")
    
    result = await api_post("/api/generate", {
        "prompt": args["prompt"],
        "architecture": architecture,
        "model": model,
    })
    
    if "error" in result:
        return error_result(result["error"])

    gen = result.get("generation", {})
    exe = result.get("execution", {})
    arch_info = ARCH_INFO.get(architecture, {})
    model_info = MODEL_INFO.get(gen.get("model", model), {})
    
    status = "✅ Success" if exe.get("success") else "❌ Failed"

    output = f"""{status} — {arch_info.get('emoji', '')} **{architecture.upper()}** | {model_info.get('emoji', '')} {model_info.get('name', model)}

## Generated Code

```
{gen.get('code', '')}
```

## Execution Result

| Exit Code | Duration | Provider |
|-----------|----------|----------|
| {exe.get('exit_code', -1)} | {exe.get('duration_ms', 0)}ms | {exe.get('provider', 'unknown')} |

**Output:**
```
{exe.get('output', '(no output)')}
```

💳 Credits remaining: **{result.get('credits_remaining', '?')}**
"""
    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_compete(args: dict) -> CallToolResult:
    """4 models compete, all execute."""
    architecture = args.get("architecture", "x86")
    
    result = await api_post("/api/compete", {
        "prompt": args["prompt"],
        "architecture": architecture,
    })
    
    if "error" in result:
        return error_result(result["error"])

    arch_info = ARCH_INFO.get(architecture, {})
    
    output = f"## 🏆 Compete Mode — {arch_info.get('emoji', '')} {architecture.upper()}\n\n"
    output += "| Model | Status | Exit | Duration | Provider |\n"
    output += "|-------|--------|------|----------|----------|\n"

    for r in result.get("results", []):
        model_info = MODEL_INFO.get(r.get("model"), {})
        status = "✅" if r.get("success") else "❌"
        output += f"| {model_info.get('emoji', '')} {r.get('model')} | {status} | {r.get('exit_code', '-')} | {r.get('duration_ms', 0)}ms | {r.get('provider', '-')} |\n"

    output += f"\n💳 Credits remaining: **{result.get('credits_remaining', '?')}**\n"
    
    # Show code from each model
    output += "\n---\n\n### Generated Code\n"
    for r in result.get("results", []):
        model_info = MODEL_INFO.get(r.get("model"), {})
        output += f"\n<details>\n<summary>{model_info.get('emoji', '')} {r.get('model')}</summary>\n\n```\n{r.get('code', '(no code)')}\n```\n\n**Output:**\n```\n{r.get('output', '(no output)')}\n```\n</details>\n"

    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_collaborate(args: dict) -> CallToolResult:
    """Models iterate on code, execute final."""
    architecture = args.get("architecture", "x86")
    models = args.get("models", ["deepseek", "claude"])
    
    # Resolve model aliases
    models = [resolve_model(m) for m in models]
    
    result = await api_post("/api/collaborate", {
        "prompt": args["prompt"],
        "architecture": architecture,
        "models": models,
    })
    
    if "error" in result:
        return error_result(result["error"])

    exe = result.get("execution", {})
    status = "✅ Success" if exe.get("success") else "❌ Failed"
    arch_info = ARCH_INFO.get(architecture, {})

    output = f"## 🤝 Collaborate Mode {status}\n\n"
    output += f"**Architecture:** {arch_info.get('emoji', '')} {architecture.upper()}\n\n"
    output += "### Pipeline\n"
    
    for r in result.get("rounds", []):
        model_info = MODEL_INFO.get(r.get("model"), {})
        output += f"- {model_info.get('emoji', '')} **{r.get('model')}**: {r.get('action')}\n"

    output += f"\n### Final Code\n\n```\n{result.get('final_code', '')}\n```\n"
    output += f"\n### Execution\n\n| Exit | Duration | Provider |\n|------|----------|----------|\n"
    output += f"| {exe.get('exit_code', -1)} | {exe.get('duration_ms', 0)}ms | {exe.get('provider', '-')} |\n"
    output += f"\n**Output:**\n```\n{exe.get('output', '(no output)')}\n```\n"
    output += f"\n💳 Credits remaining: **{result.get('credits_remaining', '?')}**"

    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_consensus(args: dict) -> CallToolResult:
    """All models generate, Claude picks best, execute."""
    architecture = args.get("architecture", "x86")
    
    result = await api_post("/api/consensus", {
        "prompt": args["prompt"],
        "architecture": architecture,
    })
    
    if "error" in result:
        return error_result(result["error"])

    exe = result.get("execution", {})
    status = "✅ Success" if exe.get("success") else "❌ Failed"
    arch_info = ARCH_INFO.get(architecture, {})

    output = f"## 🗳️ Consensus Mode {status}\n\n"
    output += f"**Architecture:** {arch_info.get('emoji', '')} {architecture.upper()}\n\n"
    
    output += "### Candidates\n"
    for c in result.get("candidates", []):
        model_info = MODEL_INFO.get(c.get("model"), {})
        output += f"- {model_info.get('emoji', '')} {c.get('model')}\n"
    
    output += f"\n### Winner: **{result.get('winner', 'consensus')}** 🏆\n\n"
    output += f"```\n{result.get('winning_code', '')}\n```\n"
    output += f"\n### Execution\n\n**Output:**\n```\n{exe.get('output', '(no output)')}\n```\n"
    output += f"\n💳 Credits remaining: **{result.get('credits_remaining', '?')}**"

    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_execute(args: dict) -> CallToolResult:
    """Execute user's code, no AI generation."""
    architecture = args.get("architecture", "x86")
    
    result = await api_post("/api/execute", {
        "code": args["code"],
        "architecture": architecture,
    })
    
    if "error" in result:
        return error_result(result["error"])

    arch_info = ARCH_INFO.get(architecture, {})
    status = "✅ Success" if result.get("success") else "❌ Failed"

    output = f"""{status} — {arch_info.get('emoji', '')} **{architecture.upper()}**

| Exit Code | Duration | Provider |
|-----------|----------|----------|
| {result.get('exit_code', -1)} | {result.get('duration_ms', 0)}ms | {result.get('provider', 'unknown')} |

**Output:**
```
{result.get('output', '(no output)')}
```

💳 Credits remaining: **{result.get('credits_remaining', '?')}**
"""
    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_history(args: dict) -> CallToolResult:
    """Get recent prompts."""
    limit = min(args.get("limit", 10), 50)
    result = await api_get(f"/api/history/recent?limit={limit}")
    
    if "error" in result:
        return error_result(result["error"])

    prompts = result.get("data", [])
    if not prompts:
        return CallToolResult(content=[TextContent(type="text", text="📜 No history found.")])

    output = "## 📜 Recent History\n\n"
    output += "| ID | Mode | Prompt | Status |\n"
    output += "|----|------|--------|--------|\n"
    
    for p in prompts:
        prompt_preview = (p.get('body') or '[execute]')[:40]
        if len(p.get('body', '')) > 40:
            prompt_preview += "..."
        output += f"| {p['id']} | {p.get('mode', '-')} | {prompt_preview} | {'✅' if p.get('status') == 'completed' else '⏳'} |\n"
    
    output += f"\n*Use `rerun` tool with prompt_id to re-run on different architecture.*"

    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_history_search(args: dict) -> CallToolResult:
    """Search prompt history."""
    query = args["query"]
    limit = min(args.get("limit", 10), 50)
    
    result = await api_get(f"/api/history/search?q={query}&limit={limit}")
    
    if "error" in result:
        return error_result(result["error"])

    prompts = result.get("data", [])
    if not prompts:
        return CallToolResult(content=[TextContent(type="text", text=f"🔍 No results for '{query}'")])

    output = f"## 🔍 Search: '{query}'\n\n"
    for p in prompts:
        output += f"**#{p['id']}** ({p.get('mode', '-')}): {(p.get('body') or '')[:60]}...\n\n"

    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_rerun(args: dict) -> CallToolResult:
    """Re-run prompt on different architecture."""
    result = await api_post(f"/api/history/{args['prompt_id']}/rerun", {
        "architecture": args["architecture"],
    })
    
    if "error" in result:
        return error_result(result["error"])

    exe = result.get("execution", {})
    arch_info = ARCH_INFO.get(args["architecture"], {})
    status = "✅ Success" if exe.get("success") else "❌ Failed"

    output = f"""{status} — Re-ran prompt #{args['prompt_id']} on {arch_info.get('emoji', '')} **{args['architecture'].upper()}**

**Output:**
```
{exe.get('output', '(no output)')}
```

💳 Credits remaining: **{result.get('credits_remaining', '?')}**
"""
    return CallToolResult(content=[TextContent(type="text", text=output)])


async def handle_credits(args: dict) -> CallToolResult:
    """Check credit balance."""
    result = await api_get("/api/user")
    
    if "error" in result:
        return error_result(result["error"])

    output = f"""## 💳 Credit Balance

**{result.get('name', 'User')}**: **{result.get('credit_balance', 0)}** credits

### Approximate Costs

| Mode | Credits |
|------|---------|
| Generate (DeepSeek/Gemini) | ~3 |
| Generate (GPT-4o) | ~5 |
| Generate (Claude) | ~6 |
| Compete (4 models) | ~19 |
| Collaborate (2 models) | ~10 |
| Consensus (4 models + merge) | ~20 |
| Execute only | ~1 |

### Architectures

| Arch | Description |
|------|-------------|
| x86 | 💻 Intel/AMD (Daytona sandbox) |
| arm64 | 🔥 ARM64 (Firecracker microVM) |
| riscv64 | ⚡ RISC-V 64 (QEMU emulation) |
| arm32 | 🔧 ARM32 (Firecracker) |
| verilog | 🔌 HDL Simulation (iverilog/ghdl) |
"""
    return CallToolResult(content=[TextContent(type="text", text=output)])


# =============================================================================
# MAIN
# =============================================================================

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
