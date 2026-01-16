"""JupyterBook CLI extension."""

import os
from importlib import resources
from threading import Thread
from typing import Annotated

from livereload import Server, shell
from typer import Argument, Option, Typer

cli = Typer()


@cli.command()
def build(
    path: Annotated[str, Argument(help="Path to the OU book")],
    output_format: Annotated[str, Option(help="The format to generate")] = "html",
) -> None:
    """Serve the OU Book locally."""
    if output_format == "html":
        shell(f"sphinx-build --builder html --fresh-env {path} {os.path.join(path, '_build', 'html')}")()
    elif output_format == "pdf":
        shell(f"sphinx-build --builder latex --fresh-env {path} {os.path.join(path, '_build', 'latex')}")()
        if not os.path.exists(os.path.join(path, "_build", "latex")):
            os.makedirs(os.path.join(path, "_build", "latex"), exist_ok=True)
        for resource in resources.files("ou_book_theme").joinpath("latex").iterdir():
            with resources.as_file(resource) as resource_path:
                with open(resource_path, "rb") as in_f:
                    with open(os.path.join(path, "_build", "latex", os.path.basename(str(resource))), "wb") as out_f:
                        out_f.write(in_f.read())
        tex_filename = None
        for filename in os.listdir(os.path.join(path, "_build", "latex")):
            if filename.endswith(".tex"):
                tex_filename = filename
                break
        shell(f"xelatex {tex_filename}", cwd=os.path.join(path, "_build", "latex"))()


@cli.command()
def serve(
    path: Annotated[str, Argument(help="Path to the OU book")],
    host: Annotated[str, Option(help="The host to serve the book at")] = "127.0.0.1",
    port: Annotated[int, Option(help="The port to serve the book at")] = 8000,
) -> None:
    """Serve the OU Book locally."""
    partial_build = shell(f"sphinx-build --builder html {path} {os.path.join(path, '_build', 'html')}")
    full_build = shell(f"sphinx-build --builder html --fresh-env {path} {os.path.join(path, '_build', 'html')}")

    initial_build = Thread(target=full_build)
    initial_build.start()

    server = Server()
    server.watch(f"{path}/**/*.md", partial_build)
    server.watch(f"{path}/**/*.yml", full_build)
    server.watch(f"{path}/**/*.py", full_build)
    server.watch(f"{path}/**/*.png", full_build)
    server.watch(f"{path}/**/*.jpg", full_build)
    server.watch(f"{path}/**/*.jpeg", full_build)
    server.watch(f"{path}/**/*.svg", full_build)
    server.serve(root=f"{path}/_build/html", port=port, host=host)
