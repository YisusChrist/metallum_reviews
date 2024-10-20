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
from core_helpers.utils import print_welcome

from metallum_reviews.consts import GITHUB, PACKAGE
from metallum_reviews.consts import __desc__ as DESC
from metallum_reviews.consts import __version__ as VERSION
from metallum_reviews.models import Review
from metallum_reviews.utils import fetch_reviews, reviews_to_json


def main() -> None:
    """Main function."""
    install()
    print_welcome(PACKAGE, VERSION, DESC, GITHUB)

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
