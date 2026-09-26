"""Minimal named-formatter registry used by the CLI."""
from typing import Callable, Dict, List

_REGISTRY: Dict[str, Callable] = {}


def register_formatter(name: str, formatter: Callable) -> None:
    _REGISTRY[name] = formatter


def get_formatter(name: str) -> Callable:
    if name not in _REGISTRY:
        raise KeyError(f"unknown formatter: {name}")
    return _REGISTRY[name]


def available_formatters() -> List[str]:
    return sorted(_REGISTRY.keys())
