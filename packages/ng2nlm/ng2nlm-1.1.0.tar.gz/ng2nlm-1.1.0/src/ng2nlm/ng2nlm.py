"""A tool to turn a Norton Guide database into a source for NotebookLM."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Final

##############################################################################
# NGDB imports.
from ngdb import Entry, Link, Long, MarkupText, NortonGuide, Short, make_dos_like

##############################################################################
# Local imports.
from . import __version__

##############################################################################
WORD_LIMIT: Final[int] = 500_000
"""The word limit for a source in NotebookLM."""

##############################################################################
PREAMBLE: Final[str] = """\
# AI NAVIGATION & BEHAVIOR RULES

1. This file is a 'mega-source' containing an entire Norton Guide database file turned into a Markdown file.
2. Every entry is wrapped in 'BEGIN ENTRY: [entry-N]' and 'END ENTRY: [entry-N]' where N is a variable length number.
3. Every entry will start with a markdown h1 header followed by a 'entry-N' identifier. This relates to the [entry-N] in the point above and will have the same format.
4. Between 'BEGIN MENUS' and 'END MENUS' is a two-level bulleted list; this is the main menu for the guide. Use this for the overarching concepts of the guide.
5. Between `BEGIN CREDITS' and 'END CREDITS' are the credits for the guide. Consider this high-signal information for copyright and guide-wide details.
6. Linked concepts in the file will be in the normal Markdown link for of [this](#entry-N), where #entry-N is the id mentioned above.
7. If an entry has a 'SEE ALSO:' line take the Markdown links on that line to be related concepts to the current entry.
8. When writing code example, do not include citation links in the code itself. Instead write all citations and provide all linked concepts as paragraphs of explanations after the code.
"""


##############################################################################
def resolve_source(args: Namespace) -> Path:
    """Work out the name to use for the source file to create.

    Args:
        args: The command line arguments.

    Returns:
        The full path for the source file.
    """
    return args.source or Path(args.guide.stem).with_suffix(".md")


##############################################################################
def get_instructions(instructions: str | None) -> str | None:
    """Loads up any instructions to place in the output.

    Args:
        instructions: The instructions to look at and use.

    Returns:
        The instructions if there are any, or `None`.

    Notes:
        If there is a file in the filesystem that matches the content of
        `instructions` then the content of that file will be used, otherwise
        the text will be used.
    """
    if instructions is not None and Path(instructions).is_file():
        instructions = Path(instructions).read_text(encoding="utf-8")
    return instructions


##############################################################################
def entry_id(entry: Entry | Link) -> str:
    """Generate an ID for the given entry.

    Returns:
        The ID for the entry.
    """
    return f"entry-{entry.offset}"


##############################################################################
class ToMarkdown(MarkupText):
    """Class to convert some Norton Guide source into Markdown."""

    def open_markup(self, cls: str) -> str:
        """Open markup for the given class.

        Args:
            cls: The class of thing to open the markup for.

        Returns:
            The opening markup text.
        """
        return cls

    def close_markup(self, cls: str) -> str:
        """Close markup for the given class.

        Args:
            cls: The class of thing to close the markup for.

        Returns:
            The closing markup text.
        """
        return cls

    def text(self, text: str) -> None:
        """Handle the given text.

        Args:
            text: The text to handle.
        """
        super().text(str(make_dos_like(text)))

    def bold(self) -> None:
        """Handle being asked to go to bold mode."""
        self.begin_markup("**")

    def unbold(self) -> None:
        """Handle being asked to go out of bold mode."""
        self.end_markup()


##############################################################################
def as_markdown(entry: Short | Long) -> str:
    """Convert a guide entry into Markdown.

    Args:
        entry: The entry to convert.

    Returns:
        A Markdown version of the entry.
    """
    markdown = f"# {entry_id(entry)}\n\n"
    for line in entry:
        if isinstance(line, str) or not line.has_offset:
            markdown += f"{ToMarkdown(line)}\n"
        else:
            markdown += f"[{ToMarkdown(line)}](#{entry_id(line)})\n"
    if isinstance(entry, Long) and entry.has_see_also:
        markdown += "\nSEE ALSO:"
        for see_also in entry.see_also:
            markdown += f" [{make_dos_like(see_also.text)}](#{entry_id(see_also)})"
    return markdown


##############################################################################
def menus(guide: NortonGuide) -> str:
    """Get the menus for the guide.

    Returns:
        The menus for the guide.
    """
    menus = "BEGIN MENUS\n\n"
    for menu in guide.menus:
        menus += f"* {make_dos_like(menu.title)}\n"
        for prompt in menu:
            menus += f"  * [{make_dos_like(prompt.text)}](#{entry_id(prompt)})\n"
    return f"{menus}\nEND MENUS\n\n"


##############################################################################
def make_source(args: Namespace) -> None:
    """Make a source file for NotebookLM.

    Args:
        args: The command line arguments.
    """
    with NortonGuide(args.guide) as guide:
        source = resolve_source(args)
        preamble = get_instructions(args.instructions) or PREAMBLE
        extra_preamble = get_instructions(args.additional_instructions) or ""
        estimated_word_count = len((preamble + extra_preamble).split())
        with source.open("w", encoding="utf-8") as notebook_source:
            notebook_source.write(preamble)
            if extra_preamble:
                notebook_source.write(f"\n\n# ADDITIONAL RULES\n\n{extra_preamble}")
            notebook_source.write("\n\n---\n\n")
            if guide.menu_count:
                notebook_source.write(menus(guide))
            if guide.credits:
                notebook_source.write("\n\nBEGIN CREDITS\n\n")
                notebook_source.write(
                    "\n".join(make_dos_like(credit).strip() for credit in guide.credits)
                )
                notebook_source.write("\nEND CREDITS\n\n")
            for entry in guide:
                notebook_source.write(f"BEGIN ENTRY: {entry_id(entry)}\n\n")
                notebook_source.write(content := as_markdown(entry))
                estimated_word_count += len(content.split())
                notebook_source.write(f"\n\nEND ENTRY: {entry_id(entry)}\n\n")
        print(f"Estimated word count: {estimated_word_count:,}")
        if estimated_word_count > WORD_LIMIT:
            print("NotebookLM will truncate this source!")
        else:
            print(f"{(estimated_word_count / WORD_LIMIT) * 100:.1f}% of the limit")


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments."""

    # Version information.
    version = f"v{__version__}"

    # Create the argument parser object.
    parser = ArgumentParser(
        prog=Path(__file__).stem,
        description="Turn a Norton Guide into a NotebookLM source",
        epilog=version,
    )

    # Add additional instructions.
    parser.add_argument(
        "-a",
        "--additional-instructions",
        help="Additional instructions to pass on to NotebookLM at the top of the source",
    )

    # Replace the builtin instructions.
    parser.add_argument(
        "-i",
        "--instructions",
        help="Override the builtin instructions to pass on to NotebookLM at the top of the source,",
    )

    # Add the guide.
    parser.add_argument(
        "-g",
        "--guide",
        type=Path,
        help="The path to the Norton Guide",
        required=True,
    )

    # Add the name of the source file that will be created.
    parser.add_argument(
        "-s",
        "--source",
        type=Path,
        help="The path to the file to create as the source for NotebookLM",
        required=False,
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s {version}",
    )

    # Parse the command line.
    return parser.parse_args()


##############################################################################
def main() -> None:
    """Main entry point."""
    make_source(get_args())


### ng2nlm.py ends here
