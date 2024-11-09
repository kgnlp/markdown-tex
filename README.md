# Markdown Tex

A custom formatter for [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences) that displays LuaLaTeX as SVGs within Markdown.

This project was inspired by [Markdown TikZ](https://github.com/vvasseur/markdown-tikz).

## Installation

For LuaLaTeX compilation, a LaTeX distribution that includes `lualatex` and `dvisvgm` executables is required, which have to be available in `PATH`.

The formatter can be installed via `pip`. This will also install the [`PyMdown Extensions`](https://facelessuser.github.io/pymdown-extensions/) package if it is not already available.
```bash
pip install git+https://github.com/kgnlp/markdown-tex
```

## Configuration

For use with MkDocs, the formatter can be configured as a custom [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences) fence in `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
      - name: latex
        class: latex
        format: !!python/name:markdown_tex.formatter
```

For direct compatibility with [`Obsidian TikZJax`](https://github.com/artisticat1/obsidian-tikzjax), it can also be configured for `tikz` code blocks:

```yaml
      - name: tikz
        class: tikz
        format: !!python/name:markdown_tex.formatter
```

## Usage

Based on the configuration, `latex` and `tikz` codeblocks without a `documentclass` will now be rendered to SVG and displayed inline. Note that the document class is set to `standalone` and `tikz` is included by default to support [`Obsidian TikZJax`](https://github.com/artisticat1/obsidian-tikzjax).

````md
```latex
\usepackage{amssymb}
\begin{document}

Some \textit{math} can be included as follows: $5x^2 - 4x + 2 = 0$, where $x \in \mathbb{R}^{N}$

\end{document}
```
````
