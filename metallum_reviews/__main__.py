"""Main module for the CLI application."""

import os
import random
import re
from typing import Any

import enmet  # type:ignore
import pyfiglet  # type: ignore
from requests_cache import CachedSession
from rich import print
from rich.prompt import Prompt
from rich.traceback import install

from metallum_reviews.consts import GITHUB, PACKAGE
from metallum_reviews.consts import __desc__ as DESC
from metallum_reviews.consts import __version__ as VERSION
from metallum_reviews.models import Review
from metallum_reviews.utils import fetch_reviews, reviews_to_json


def strip_rich_tags(text: str) -> str:
    """
    Remove rich text tags from a string.

    Args:
        text (str): The text to remove tags from.

    Returns:
        str: The text with tags removed.
    """
    return re.sub(r"\[\/?[\w=#]*\]", "", text)


def get_random_font() -> str:
    """
    Return a random font from pyfiglet.

    Returns:
        str: A random font name.
    """
    fonts: list[str] = pyfiglet.FigletFont.getFonts()
    return random.choice(fonts)


def print_welcome() -> None:
    """Print a welcome message in the terminal."""
    # Get terminal width
    width: int = os.get_terminal_size().columns

    # Pickup a random font
    font: str = "slant"  # get_random_font()

    # Create and format title, repository, and description
    title: str = PACKAGE.replace("_", " ").capitalize()
    version: str = f"[i][red]Version: {VERSION}[/]"
    repo: str = f"[cyan]{GITHUB}[/]"
    desc: str = f"[blue]{DESC}[/] - {version}"

    # Render and print title using pyfiglet
    figlet = pyfiglet.Figlet(font=font, justify="center", width=width)
    print(f"""[green]{figlet.renderText(title)}[/]""")

    # Calculate visible lengths and center accordingly
    visible_desc: str = strip_rich_tags(desc)
    visible_repo: str = strip_rich_tags(repo)

    # Print description and repository info with rich formatting
    print(desc.center(width + len(desc) - len(visible_desc)))
    print(repo.center(width + len(repo) - len(visible_repo)))
    print()


def main() -> None:
    """Main function."""
    install()
    print_welcome()

    try:
        band: str = Prompt.ask("Enter the band to search", default="Opeth")
        album: str = Prompt.ask("Enter the album to search", default="Blackwater Park")
    except KeyboardInterrupt:
        return

    print(f"Searching for album '{album}' by '{band}'...")
    results: list[Any | enmet.Album] = enmet.search_albums(
        name=album,
        band=band,
    )
    total_results: int = len(results)
    print(f"Found {total_results} results for album '{album}' by '{band}'")

    session = CachedSession()
    reviews: list[Review] = fetch_reviews(session, results, total_results)

    # Save the reviews to a JSON file
    reviews_to_json(reviews)


if __name__ == "__main__":
    main()
