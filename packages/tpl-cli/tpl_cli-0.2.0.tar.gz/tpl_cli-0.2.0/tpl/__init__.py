"""Template Puller (tpl) CLI package.

Exports the Typer app entrypoint used by `python -m tpl` and the `tpl` console
script.
"""

from .cli import main

__all__ = ["main"]
