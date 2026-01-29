# Cursor MCP Configuration Guide

This guide shows you how to install and configure the Debug Memory MCP server in Cursor.

## Step 1: Install the MCP Server

Choose one of these installation methods:

### Option A: Install from PyPI (Recommended)

Using uv (recommended):

```bash
uv pip install debug-mcp
```

### Option B: Download and Extract
1. Download the latest release
2. Extract to a folder (e.g., `~/debug-mcp` or `C:/tools/debug-mcp`)
3. Open terminal in that folder
4. Run: `uv pip install -e .` (or `pip install -e .`)

**Remember the installation path** - you'll need it in Step 3.

## Step 2: Get Your API Key

1. Go to your **Debug Memory** dashboard
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Copy the API key (it starts with `dm_`)
   - ⚠️ **Important**: Save this key somewhere safe! You won't be able to see it again.

## Step 3: Configure Cursor

### Option A: Workspace-Specific Configuration (Recommended)

Create or edit `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "debug-incident": {
      "command": "uvx",
      "args": ["debug-mcp"],
      "env": {
        "WORKSPACE_API_KEY": "dm_your_api_key_here"
      }
    }
  }
}
```

**⚠️ Important - Replace These Values:**
- `"dm_your_api_key_here"` → Use your actual API key from Step 2

If `uvx` is not available, use this alternative:

```json
{
  "mcpServers": {
    "debug-incident": {
      "command": "uv",
      "args": ["run", "debug-mcp"],
      "cwd": "/absolute/path/to/debug-mcp",
      "env": {
        "WORKSPACE_API_KEY": "dm_your_api_key_here"
      }
    }
  }
}
```

**Example `cwd` paths:**
- Windows: `"C:/tools/debug-mcp"`
- macOS: `"/Users/yourname/debug-mcp"`
- Linux: `"/home/yourname/debug-mcp"`

### Option B: Global Configuration

Alternatively, add to your global Cursor settings (applies to all projects):

1. Open Cursor Settings (Ctrl+Comma or Cmd+Comma)
2. Search for "MCP"
3. Edit the MCP Servers configuration
4. Add the same JSON configuration as above (with your paths!)

## Step 4: Restart Cursor

After saving the configuration:
1. Close and reopen Cursor completely
2. The MCP server will automatically start when Cursor launches

## Step 5: Verify Installation

To verify the MCP server is working:

1. Open the Cursor chat
2. Type: "Can you list the available MCP tools?"
3. You should see `ranked_solutions`, `add_solution`, `record_outcome`, `add_incident` in the list

Or simply try using it:
```
Rank solutions for "test incident" with env {"os_family":"windows"}
```

## Codex CLI / IDE Extension Setup (`~/.codex/config.toml`)

Codex stores MCP configuration in `~/.codex/config.toml`.

This package's current version is **`debug-mcp==0.1.7`** (from `pyproject.toml`). If you want reproducible behavior, pin that version in your Codex config.

**Important note about version pinning:** `uvx --from debug-mcp==...` (and `uv run --with debug-mcp==...`) can only install versions that are actually published to PyPI. If you bump `pyproject.toml` locally but haven’t published yet, Codex may still run an older published build — which can look like “Method not found” for newly added MCP capabilities.

### Option A: STDIO via `uvx` (recommended when available)

```toml
[mcp_servers.debug-incident]
command = "uvx"
# Pin the package version, then run the console script entrypoint.
args = ["--from", "debug-mcp==0.1.7", "debug-mcp"]

[mcp_servers.debug-incident.env]
WORKSPACE_API_KEY = "dm_your_api_key_here"
```

### Option B: STDIO via `uv run --with ...` (no `cwd`, works anywhere)

If you installed with `uv pip install debug-mcp` (or just want a config that doesn't depend on a checkout path),
you can also run the tool in an isolated, ephemeral environment:

```toml
[mcp_servers.debug-incident]
command = "uv"
args = ["run", "--with", "debug-mcp==0.1.7", "debug-mcp"]

[mcp_servers.debug-incident.env]
WORKSPACE_API_KEY = "dm_your_api_key_here"
```

### Option C: STDIO via installed entrypoint (no `cwd`, no version pin)

If `debug-mcp` is on your PATH (e.g. installed into an environment that Codex can see), you can run it directly:

```toml
[mcp_servers.debug-incident]
command = "debug-mcp"

[mcp_servers.debug-incident.env]
WORKSPACE_API_KEY = "dm_your_api_key_here"
```

### Option D: STDIO via local checkout (requires `cwd`)

```toml
[mcp_servers.debug-incident]
command = "uv"
args = ["run", "python", "mcp_server.py"]
cwd = "C:/absolute/path/to/debug-mcp" # Windows example

[mcp_servers.debug-incident.env]
WORKSPACE_API_KEY = "dm_your_api_key_here"
```

## Configuration Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `command` | Command to run | `uvx` |
| `args` | Arguments to command | `["debug-mcp"]` |
| `WORKSPACE_API_KEY` | Your workspace API key | `dm_abc123...` |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `EDGE_FUNCTION_URL` | Override the Debug Memory backend (defaults to production) | `https://<your>.supabase.co/functions/v1` |

### Understanding the `cwd` Field

The `cwd` (current working directory) tells Cursor **where you installed the MCP server**.

**Key Points:**
- ✅ Must be an **absolute path** (full path from root)
- ✅ Only needed if you're using the `uv run debug-mcp` fallback config
- ✅ Every user has a different path based on where they installed it

**Finding Your Path:**

**Windows:**
```bash
cd debug-mcp
cd
# Output: C:\Users\YourName\debug-mcp
# Use: "C:/Users/YourName/debug-mcp"
```

**macOS/Linux:**
```bash
cd debug-mcp
pwd
# Output: /Users/yourname/debug-mcp
# Use: "/Users/yourname/debug-mcp"
```

**Path Format Examples:**

Windows:
```json
"cwd": "C:/tools/debug-mcp"
"cwd": "C:/Users/john/projects/debug-mcp"
```

macOS:
```json
"cwd": "/Users/john/debug-mcp"
"cwd": "/opt/debug-mcp"
```

Linux:
```json
"cwd": "/home/john/debug-mcp"
"cwd": "/opt/debug-mcp"
```

## Multiple Workspaces

If you work with multiple Debug Memory workspaces, you can configure multiple MCP servers with different API keys:

```json
{
  "mcpServers": {
    "debug-work": {
      "command": "uv",
      "args": ["run", "debug-mcp"],
      "cwd": "/your/install/path",
      "env": {
        "WORKSPACE_API_KEY": "dm_work_workspace_key"
      }
    },
    "debug-personal": {
      "command": "uv",
      "args": ["run", "debug-mcp"],
      "cwd": "/your/install/path",
      "env": {
        "WORKSPACE_API_KEY": "dm_personal_workspace_key"
      }
    }
  }
}
```

Note: Both use the same installation path, just different API keys!

## Troubleshooting

### MCP Server Not Showing Up

1. **Check Python installation**: Run `python --version` in terminal
2. **Verify install path**: Make sure `cwd` points to the folder where you installed this repo
3. **Check logs**: Look at Cursor's output panel for error messages
4. **Restart Cursor**: Sometimes a full restart is needed

### "Invalid API Key" Error

1. Verify your API key is correct (starts with `dm_`)
2. Check that the key is active in your Debug Memory dashboard
3. Make sure there are no extra spaces in the configuration

### "Module not found" Error

Install dependencies in the folder where you installed the MCP server:
```bash
cd /path/to/debug-mcp
uv pip install -e .
```

Or using pip:
```bash
pip install -e .
```

If you get permission errors with pip, try:
```bash
pip install --user -e .
```

### Permission Denied

**Windows**: Make sure Python is in your PATH
**macOS/Linux**: Use `python3` instead of `python` in the command

## Security Best Practices

- ✅ **DO**: Keep your API key secret
- ✅ **DO**: Use workspace-specific config (`.cursor/mcp.json`) to avoid committing keys
- ✅ **DO**: Add `.cursor/mcp.json` to `.gitignore` if it contains keys
- ❌ **DON'T**: Share your API key in public repositories
- ❌ **DON'T**: Commit API keys to version control

## Example .gitignore

```gitignore
# Cursor MCP config with secrets
.cursor/mcp.json

# Environment files
.env
.env.local
```

