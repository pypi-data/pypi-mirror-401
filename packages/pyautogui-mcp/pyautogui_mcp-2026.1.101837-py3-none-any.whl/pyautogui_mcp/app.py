from __future__ import annotations

import argparse
import base64
import functools
import inspect
import os
import sys
import typing
from dataclasses import is_dataclass
from typing import Any, Callable, Iterable, Mapping

import anyio
from fastmcp import FastMCP
from fastmcp.utilities.types import Image as MCPImage

try:
    import pyautogui
except ImportError as e:
    raise SystemExit("Missing dependency. Install with: pip install pyautogui") from e


pyautogui.FAILSAFE = True
pyautogui.PAUSE = float(os.getenv("PYAUTOGUI_PAUSE", "0.0"))

mcp = FastMCP(name="PyAutoGUI-MCP")

REGISTERED_TOOLS: dict[str, str] = {}


_NAME_TYPE_HINTS: dict[str, type[Any]] = {
    "x": int,
    "y": int,
    "xOffset": int,
    "yOffset": int,
    "left": int,
    "top": int,
    "width": int,
    "height": int,
    "clicks": int,
    "interval": float,
    "duration": float,
    "pause": float,
    "button": str,
    "message": str,
    "text": str,
    "key": str,
    "keys": list,
    "region": list,
}


READ_ONLY_NAME_HINTS = (
    "position",
    "size",
    "onScreen",
    "pixel",
    "screenshot",
    "locate",
    "center",
)


def _annotation_has_forward_ref(tp: Any) -> bool:
    if isinstance(tp, str):
        return True
    if isinstance(tp, typing.ForwardRef):
        return True

    origin = typing.get_origin(tp)
    if origin is None:
        return False

    return any(_annotation_has_forward_ref(a) for a in typing.get_args(tp))


def _annotation_is_safe(tp: Any) -> bool:
    return not _annotation_has_forward_ref(tp)


def _is_jsonable_default(v: Any) -> bool:
    if v is None or isinstance(v, (bool, int, float, str)):
        return True
    if isinstance(v, (list, tuple)):
        return all(_is_jsonable_default(x) for x in v)
    if isinstance(v, dict):
        return all(isinstance(k, str) and _is_jsonable_default(val) for k, val in v.items())
    return False


def _make_safe_signature(
    sig: inspect.Signature,
) -> tuple[inspect.Signature, set[str]]:
    omit_if_none: set[str] = set()
    params: list[inspect.Parameter] = []

    for p in sig.parameters.values():
        if p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            raise ValueError("varargs signature is not supported")

        ann = _infer_param_type(p)
        default = p.default

        if default is not inspect._empty and not _is_jsonable_default(default):
            omit_if_none.add(p.name)
            default = None
            if ann is not Any:
                ann = ann | None

        params.append(p.replace(annotation=ann, default=default))

    safe_sig = sig.replace(parameters=params, return_annotation=Any)
    return safe_sig, omit_if_none


def _annotations_from_sig(sig: inspect.Signature) -> dict[str, Any]:
    ann: dict[str, Any] = {}
    for name, p in sig.parameters.items():
        ann[name] = Any if p.annotation is inspect._empty else p.annotation
    ann["return"] = Any if sig.return_annotation is inspect._empty else sig.return_annotation
    return ann


def _register_callable_as_tool(
    func: Callable[..., Any],
    *,
    tool_name: str,
    description: str,
    sig: inspect.Signature,
    omit_if_none: set[str] | None = None,
    normalize_kwargs: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> None:
    omit_if_none = omit_if_none or set()

    async def _runner(*args: Any, **kwargs: Any) -> Any:
        if normalize_kwargs:
            kwargs = normalize_kwargs(dict(kwargs))
        for k in list(omit_if_none):
            if kwargs.get(k, "__missing__") is None:
                kwargs.pop(k, None)

        call = functools.partial(func, *args, **kwargs)
        result = await anyio.to_thread.run_sync(call)
        return _normalise(result)

    _runner.__name__ = tool_name
    _runner.__doc__ = description or (func.__doc__ or "")
    _runner.__signature__ = sig  # type: ignore[attr-defined]
    _runner.__annotations__ = _annotations_from_sig(sig)

    mcp.tool(
        name=tool_name,
        description=_runner.__doc__ or "",
        annotations=_tool_annotations(tool_name),
    )(_runner)
    REGISTERED_TOOLS[tool_name] = _runner.__doc__ or ""


def _infer_param_type(p: inspect.Parameter) -> Any:
    ann = p.annotation
    if ann is not inspect._empty and _annotation_is_safe(ann):
        return ann

    if p.default is not inspect._empty and p.default is not None:
        if isinstance(p.default, bool):
            return bool
        if isinstance(p.default, int) and not isinstance(p.default, bool):
            return int
        if isinstance(p.default, float):
            return float
        if isinstance(p.default, str):
            return str
        if isinstance(p.default, (list, tuple)):
            return list

    return _NAME_TYPE_HINTS.get(p.name, Any)


def _is_varargs(sig: inspect.Signature) -> bool:
    for p in sig.parameters.values():
        if p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            return True
    return False


def _encode_png_bytes(pil_image: Any) -> bytes:
    from io import BytesIO

    buf = BytesIO()
    pil_image.save(buf, format="PNG")
    return buf.getvalue()


def _encode_image_bytes(pil_image: Any, image_format: str, quality: int | None) -> bytes:
    from io import BytesIO

    image_format = image_format.lower()
    if image_format == "jpg":
        image_format = "jpeg"

    if image_format not in ("png", "jpeg"):
        raise ValueError("format must be 'png' or 'jpeg'")

    buf = BytesIO()
    save_kwargs: dict[str, Any] = {}
    if image_format == "jpeg":
        if quality is not None:
            if not 1 <= int(quality) <= 95:
                raise ValueError("quality must be between 1 and 95")
            save_kwargs["quality"] = int(quality)
        if getattr(pil_image, "mode", None) not in ("RGB", "L"):
            pil_image = pil_image.convert("RGB")
        pil_image.save(buf, format="JPEG", **save_kwargs)
    else:
        pil_image.save(buf, format="PNG")
    return buf.getvalue()


def _normalise(obj: Any) -> Any:
    if obj is None:
        return None

    if hasattr(obj, "save") and hasattr(obj, "size") and hasattr(obj, "mode"):
        png = _encode_png_bytes(obj)
        return MCPImage(data=png, format="png")

    if hasattr(obj, "_asdict"):
        return {k: _normalise(v) for k, v in obj._asdict().items()}

    if is_dataclass(obj):
        return {k: _normalise(getattr(obj, k)) for k in obj.__dataclass_fields__.keys()}

    if all(hasattr(obj, k) for k in ("left", "top", "width", "height")):
        return {
            "left": int(getattr(obj, "left")),
            "top": int(getattr(obj, "top")),
            "width": int(getattr(obj, "width")),
            "height": int(getattr(obj, "height")),
        }

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple)):
        return [_normalise(v) for v in obj]

    if isinstance(obj, Mapping):
        return {str(k): _normalise(v) for k, v in obj.items()}

    if isinstance(obj, (bytes, bytearray)):
        return {
            "base64": base64.b64encode(bytes(obj)).decode("ascii"),
        }

    return str(obj)


def _tool_annotations(tool_name: str) -> dict[str, Any]:
    read_only = any(h in tool_name for h in READ_ONLY_NAME_HINTS)
    if read_only:
        return {"readOnlyHint": True}
    return {"destructiveHint": True}


def _normalize_move_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    if "xOffset" not in kwargs and "x" in kwargs:
        kwargs["xOffset"] = kwargs.pop("x")
    if "yOffset" not in kwargs and "y" in kwargs:
        kwargs["yOffset"] = kwargs.pop("y")
    return kwargs


def _import_status(module_name: str) -> dict[str, Any]:
    import importlib

    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", None) or getattr(module, "VERSION", None)
        return {"ok": True, "version": str(version) if version else None}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{exc.__class__.__name__}: {exc}"}


def _iter_pyautogui_functions() -> Iterable[tuple[str, Callable[..., Any]]]:
    for name, obj in inspect.getmembers(pyautogui):
        if name.startswith("_"):
            continue
        if inspect.isclass(obj):
            continue
        if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isbuiltin(obj):
            yield name, obj


def _install_special_wrappers(prefix: str) -> None:
    if hasattr(pyautogui, "hotkey"):

        def _hotkey(keys: list[str], interval: float = 0.0) -> None:
            pyautogui.hotkey(*keys, interval=interval)

        sig = inspect.signature(_hotkey)
        _register_callable_as_tool(
            _hotkey,
            tool_name=f"{prefix}hotkey",
            description="Press a key chord, e.g. keys=['ctrl','c']",
            sig=sig,
        )


def _should_register_name(name: str, include: str, exclude: str) -> bool:
    if include and include not in name:
        return False
    if exclude and exclude in name:
        return False
    return True


def _safe_signature_for(func: Callable[..., Any]) -> tuple[inspect.Signature, set[str]] | None:
    try:
        orig_sig = inspect.signature(func)
    except (TypeError, ValueError):
        return None

    if _is_varargs(orig_sig):
        return None

    try:
        return _make_safe_signature(orig_sig)
    except ValueError:
        return None


def _register_pyautogui_api(prefix: str, include: str, exclude: str) -> tuple[int, int]:
    _install_special_wrappers(prefix)

    registered = 0
    skipped = 0
    normalizers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
        "moveRel": _normalize_move_kwargs,
        "move": _normalize_move_kwargs,
    }

    for name, func in _iter_pyautogui_functions():
        if not _should_register_name(name, include, exclude):
            continue

        sig_info = _safe_signature_for(func)
        if sig_info is None:
            skipped += 1
            continue

        safe_sig, omit_if_none = sig_info

        tool_name = f"{prefix}{name}"
        description = (getattr(func, "__doc__", "") or "").strip()

        _register_callable_as_tool(
            func,
            tool_name=tool_name,
            description=description or f"PyAutoGUI: {name}",
            sig=safe_sig,
            omit_if_none=omit_if_none,
            normalize_kwargs=normalizers.get(name),
        )
        registered += 1

    return registered, skipped


@mcp.tool(
    name="pyautogui_tools",
    description="List which PyAutoGUI tools were registered by this server.",
    annotations={"readOnlyHint": True},
)
def pyautogui_tools() -> dict[str, Any]:
    return {
        "note": "Use your MCP client’s tool list for full details.",
        "tools": [
            {"name": name, "description": desc}
            for name, desc in sorted(REGISTERED_TOOLS.items())
        ],
    }


@mcp.tool(
    name="pyautogui_diagnose",
    description="Inspect PyAutoGUI and dependency availability on the server.",
    annotations={"readOnlyHint": True},
)
def pyautogui_diagnose() -> dict[str, Any]:
    deps = [
        "pyautogui",
        "pyscreeze",
        "PIL",  # Pillow
        "mouseinfo",
        "pymsgbox",
        "pytweening",
        "pygetwindow",
    ]
    return {
        "python": sys.version,
        "platform": sys.platform,
        "deps": {name: _import_status(name) for name in deps},
    }


@mcp.tool(
    name="pyautogui_screenshot_encoded",
    description="Capture a screenshot and return encoded image bytes.",
    annotations={"readOnlyHint": True},
)
def pyautogui_screenshot_encoded(
    format: str = "png",
    quality: int | None = None,
    region: list[int] | None = None,
) -> MCPImage:
    format_normalized = format.lower()
    if format_normalized == "jpg":
        format_normalized = "jpeg"
    screenshot = pyautogui.screenshot(region=tuple(region) if region else None)
    data = _encode_image_bytes(screenshot, format_normalized, quality)
    return MCPImage(data=data, format=format_normalized)


REGISTERED_TOOLS["pyautogui_screenshot_encoded"] = "Capture a screenshot and return encoded bytes."


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--prefix", default="pyautogui_")
    parser.add_argument(
        "--include",
        default="",
        help="Optional substring filter: only register names containing this.",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Optional substring filter: skip names containing this.",
    )
    return parser.parse_args()


def _run_server(transport: str, host: str, port: int) -> None:
    if transport == "http":
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()


def main() -> None:
    args = _parse_args()

    _register_pyautogui_api(args.prefix, args.include, args.exclude)
    _run_server(args.transport, args.host, args.port)
