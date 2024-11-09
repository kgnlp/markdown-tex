import subprocess
from subprocess import CalledProcessError
import re
from typing import Any, Dict
import sys
from os import path
from tempfile import TemporaryDirectory


def _postprocess_svg(svg: str) -> str:
    """
    Replaces colors in the SVG to fit the current markdown theme in a mkdocs environment.
    Inspired by the color handling in [obsidian-tikzjax](https://github.com/artisticat1/obsidian-tikzjax)

    :param svg: The original SVG source code

    :return: The SVG with all white and black colors replaced by
    `currentColor` and `var(--md-default-bg-color,#fff)` respectively
    """
    # Dynamically falls back to white if mkdocs is not used or the variable is not in scope
    svg = re.sub("'#fff'|'white'", '"var(--md-default-bg-color,#fff)"', svg)
    return re.sub("'#000'|'black'", '"currentColor"', svg)


def _compile_tex(source: str, css_class: str = "") -> str:
    """
    Compiles the given LuaLaTeX source to SVG as a standalone document and returns the SVG code centered in a div. The class of the wrapper div is set to `css_class` if it is not empty.

    :param source: LuaLaTeX source code
    :param css_class: An optional CSS class name that will be assigned to the wrapper div

    :return: The compiled SVG centered in a wrapper div
    """
    with TemporaryDirectory() as directory:
        compiled_path = path.join(directory, "tikz")
        source_path = compiled_path + ".tex"

        with open(source_path, "w", encoding="utf-8") as file:
            # Compile in standalone mode with dvisvgm support
            file.write(
                rf"""
                \documentclass[dvisvgm]{{standalone}}
                \usepackage{{tikz}}
                {source}
                """
            )

        # Compile to DVI format without interaction
        subprocess.run(
            (
                "lualatex",
                "--output-format=dvi",
                "--interaction=nonstopmode",
                "--output-directory",
                directory,
                source_path,
            ),
            check=True,
        )
        # Generate the SVG from DVI directly to stdout
        # Render text to SVG shapes for compatibility and more reliable formatting
        output = subprocess.run(
            ("dvisvgm", "--no-fonts", "-s", compiled_path), check=True, capture_output=True
        )

    # Postprocess the generated SVG
    processed = _postprocess_svg(output.stdout.decode("utf-8"))
    # Wrap in centered div and add a css_class if it's non-empty
    css_class = f' class="{css_class}"' if css_class else ""
    # Fill sets the default font color when compiling the SVG with --no-fonts
    return f'<div{css_class} style="text-align:center;fill:currentColor">{processed}</div>'


def formatter(
    source: str, _language: str, css_class: str, _options: Dict[str, str], _md: Any, **kwargs
) -> str:
    """
    Compiles the given LuaLaTeX source to SVG as a standalone document and returns the SVG code centered in a div. If compilation fails the original source is returned.

    :param source: LuaLaTeX source code.
    :param css_class: CSS class added to the wrapper div element

    :return: `source` compiled to SVG wrapped in a div or the unmodified `source` if compilation fails.
    """
    try:
        return _compile_tex(source, css_class)
    except CalledProcessError as error:
        print(error, file=sys.stderr)
        return source
