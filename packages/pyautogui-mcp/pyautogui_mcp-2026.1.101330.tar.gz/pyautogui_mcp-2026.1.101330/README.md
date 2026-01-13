<div align="center">
  <a target="_blank" href="https://github.com/chigwell/pyautogui-mcp">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=PyAutoGUI-MCP&fontSize=50&fontAlignY=35&animation=fadeIn&fontColor=FFFFFF&descAlignY=55&descAlign=62" alt="Telegram MCP Server" width="100%" />
  </a>
</div>

PyAutoGUI-MCP exposes MCP tools dynamically from the [`PyAutoGUI`](https://pypi.org/project/PyAutoGUI/) API.
It does not manually reimplement or wrap each function: it auto-registers the available API.

## Install with pip

```bash
pip install pyautogui-mcp
```

Run the server:

```bash
pyautogui-mcp --transport stdio
pyautogui-mcp --transport http --host 127.0.0.1 --port 8000
```

MCP client config example:

```json
{
  "mcpServers": {
    "pyautogui-mcp": {
      "command": "pyautogui-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

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

## Use in your own project

Import only what you need and run it under your own server lifecycle:

```python
from pyautogui_mcp import mcp, register_pyautogui_api

register_pyautogui_api(prefix="pyautogui_")
mcp.run()  # or mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Other exports:

```python
from pyautogui_mcp import pyautogui_diagnose, pyautogui_tools
```

## Desktop control notes

- The server runs actions on the machine where it is launched (current desktop/display).
- PyAutoGUI requires a real GUI session; headless environments will fail.
- Safety: moving the mouse to a corner triggers the PyAutoGUI failsafe.
- Optional pause between actions via `PYAUTOGUI_PAUSE=0.1`.
