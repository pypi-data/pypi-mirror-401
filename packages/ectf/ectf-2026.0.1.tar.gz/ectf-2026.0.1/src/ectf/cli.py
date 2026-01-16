"""CLI to interact with the eCTF API

Author: Ben Janis

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import sys
import webbrowser
from typing import Annotated

import typer

import ectf.api.cli
import ectf.hw.cli
import ectf.tools.cli
from ectf import CONFIG
from ectf.api import API
from ectf.console import error, info, success, warning

app = typer.Typer(help="Interact with the eCTF hardware, design, and API")

app.add_typer(ectf.tools.cli.app, name="tools", help="Run the host tools")
app.add_typer(ectf.api.cli.app, name="api", help="Interact with the API")
app.add_typer(ectf.hw.cli.app, name="hw", help="Interact with the MITRE bootloader")


@app.command()
def config(
    token: Annotated[
        str,
        typer.Option(help="Team API token", prompt=True),
    ] = API.config.token,
    git_url: Annotated[
        str,
        typer.Option(help="API URL", prompt=True),
    ] = API.config.git_url,
    api_url: Annotated[
        str,
        typer.Option(help="API URL", prompt=True),
    ] = API.config.api_url,
    force: Annotated[bool, typer.Option("--force", "-f")] = False,  # noqa: FBT002
) -> None:
    """Create or update the configuration file"""
    if API.config.exists():
        if not force:
            error(f"Config file {API.config.PATH} already exists! Use -f to overwrite")
            sys.exit(-1)
        else:
            warning(f"Overwriting config file {API.config.PATH}")

    API.config.token = token
    API.config.git_url = git_url
    API.config.api_url = api_url
    API.config.dump()

    success(f"Wrote config file to {API.config.PATH}")


@app.command("docs")
def docs() -> None:
    """Open the API documentation website"""
    url = f"{API.config.api_url}/docs"
    info(f"Opening API interface website at {url}")
    webbrowser.open_new_tab(url)


@app.command("rules")
def rules() -> None:
    """Open the eCTF rules website"""
    url = "https://rules.ectf.mitre.org"
    info(f"Opening eCTF rules website at {url}")
    webbrowser.open_new_tab(url)


@app.callback()
def set_globals(
    verbose: Annotated[
        int,
        typer.Option("--verbose", "-v", count=True, help="Enable debug prints"),
    ] = 0,
) -> None:
    """Set the verbosity of all scripts"""
    CONFIG["VERBOSE"] = verbose


if __name__ == "__main__":
    app()
