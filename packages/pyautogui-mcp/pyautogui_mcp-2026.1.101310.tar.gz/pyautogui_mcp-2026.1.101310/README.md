# pyautogui-mcp

## Run with uv

Dependencies are declared in `pyproject.toml`, so uv can resolve and run directly:

```json
{
  "mcpServers": {
    "pyautogui-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/pyautogui-mcp",
        "run",
        "python",
        "-m",
        "pyautogui_mcp"
      ]
    }
  }
}
```

You can also launch manually:

```bash
uv run python -m pyautogui_mcp --transport stdio
uv run python -m pyautogui_mcp --transport http --host 127.0.0.1 --port 8000
```
