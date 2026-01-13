<div align="center">
  <a target="_blank" href="https://github.com/chigwell/pyautogui-mcp">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=PyAutoGUI-MCP&fontSize=50&fontAlignY=35&animation=fadeIn&fontColor=FFFFFF&descAlignY=55&descAlign=62" alt="Telegram MCP Server" width="100%" />
  </a>
</div>

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
