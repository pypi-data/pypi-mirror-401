from __future__ import annotations

from .app import mcp, pyautogui_diagnose, pyautogui_tools
from .app import main as main
from .app import _register_pyautogui_api as _register_pyautogui_api


def register_pyautogui_api(
    prefix: str = "pyautogui_",
    include: str = "",
    exclude: str = "",
) -> tuple[int, int]:
    return _register_pyautogui_api(prefix, include, exclude)


__all__ = [
    "main",
    "mcp",
    "pyautogui_diagnose",
    "pyautogui_tools",
    "register_pyautogui_api",
]
