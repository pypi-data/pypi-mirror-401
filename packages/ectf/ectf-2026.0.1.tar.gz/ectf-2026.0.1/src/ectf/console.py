"""Interface to print to the console

Author: Ben Janis

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

from typing import Any

from rich.console import Console
from rich.theme import Theme

from ectf import CONFIG

console = Console(
    theme=Theme(
        {
            "trace": "italic white",
            "debug": "italic cyan",
            "success": "green",
            "warning": "orange1",
            "error": "bold red",
        },
    ),
)


def trace(msg: Any) -> None:  # noqa: ANN401
    """Print a debug info message"""
    if CONFIG["VERBOSE"] >= 2:  # noqa: PLR2004
        console.print(msg, style="trace")


def debug(msg: Any) -> None:  # noqa: ANN401
    """Print a debug info message"""
    if CONFIG["VERBOSE"] >= 1:
        console.print(msg, style="debug")


def info(msg: Any) -> None:  # noqa: ANN401
    """Print an info message"""
    console.print(msg)


def success(msg: Any) -> None:  # noqa: ANN401
    """Print a success message"""
    console.print(msg, style="success")


def warning(msg: Any) -> None:  # noqa: ANN401
    """Print a warning message"""
    console.print(msg, style="warning")


def error(msg: Any) -> None:  # noqa: ANN401
    """Print an error message"""
    console.print(msg, style="error")
