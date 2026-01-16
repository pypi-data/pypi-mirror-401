# ng2nlm - Turn a Norton Guide into a source for NotebookLM

## Introduction

`ng2nlm` is a simple command line tool designed to turn a [Norton
Guide](https://en.wikipedia.org/wiki/Norton_Guides) file into a single
[Markdown](https://en.wikipedia.org/wiki/Markdown) file that can be uploaded
to Google's [NotebookLM](https://notebooklm.google.com/) (or presumably used
with other LLM tools for similar purposes).

It's probably fair to say that it's "opinionated" in that I wrote this to
serve my specific purpose; but where possible I've attempted to make it
generic and configurable.

## Installing

`ng2nlm` is a Python application and [is distributed via
PyPI](https://pypi.org/project/ng2nlm/). It can be installed with tools such
as [pipx](https://pipx.pypa.io/stable/):

```sh
pipx install ng2nlm
```

or [`uv`](https://docs.astral.sh/uv/):

```sh
uv tool install ng2nlm
```

Also, if you do have uv installed, you can simply use
[`uvx`](https://docs.astral.sh/uv/guides/tools/):

```sh
uvx ng2nlm
```

to run `ng2nlm`.

## Using

See [the main documentation](https://ng2nlm.davep.dev/) for details on how
to use the tool.

## Getting help

If you need some help using `ng2nlm`, or have ideas for improvements, please
feel free to drop by [the
discussions](https://github.com/davep/ng2nlm/discussions) and ask or
suggest. If you believe you've found a bug please feel free to [raise an
issue](https://github.com/davep/ng2nlm/issues).

[//]: # (README.md ends here)
