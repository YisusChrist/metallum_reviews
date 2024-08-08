"""Utility functions for fetching and processing reviews from Encyclopaedia Metallum."""

import re
import time
from datetime import datetime
from typing import Any

import enmet  # type:ignore
from bs4 import BeautifulSoup, ResultSet, Tag  # type:ignore
from fake_useragent import FakeUserAgent  # type:ignore
from requests import HTTPError, Response, Session  # type:ignore
from requests_cache import CachedResponse, CachedSession, OriginalResponse
from rich import print

from metallum_reviews.models import Review, User
from metallum_reviews.progress import progress

ua = FakeUserAgent()


def send_request(
    session: CachedSession | Session,
    url: str,
) -> OriginalResponse | CachedResponse:
    """
    Send a request to a URL and handle rate limiting.

    Args:
        session (CachedSession | Session): The cached session to use for making requests.
        url (str): The URL to send the request to.

    Returns:
        OriginalResponse | CachedResponse: The response object from the request.
    """
    response: OriginalResponse | CachedResponse | Response = session.get(
        url, headers={"User-Agent": ua.random}
    )
    if response.status_code == 429:
        print("[red]ERROR: Rate limited[/]")
        retry_after = int(response.headers.get("Retry-After", 10))
        print(f"Retrying after {retry_after} seconds...")
        time.sleep(retry_after)

        return session.get(url, headers={"User-Agent": ua.random})

    try:
        response.raise_for_status()
        # print(f"[green]OK[/]")
    except HTTPError as e:
        print(f"[red]ERROR: {e}[/]")
    return response


def extract_date(date_string: str) -> datetime:
    """
    Extract a datetime object from a date string.

    Args:
        date_string (str): The date string to extract the datetime object from.

    Returns:
        datetime.datetime: The datetime object extracted from the date string.
    """
    # Regular expression to remove ordinal suffixes (e.g., 'st', 'nd', 'rd', 'th')
    date_string_cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_string)

    # Convert the cleaned date string to a datetime object
    date_obj: datetime = datetime.strptime(date_string_cleaned, "%B %d, %Y")

    # Print the datetime object
    return date_obj


def process_review(url: str, album: enmet.Album, review_html: Tag) -> Review:
    """
    Process a review HTML tag to extract the review information.

    Args:
        url (str): The base URL to use for constructing the review URL.
        album (enmet.Album): The album object to associate the review with.
        review_html (Tag): The review HTML tag to process.

    Returns:
        Review: The processed review object.
    """
    review_title: str = review_html.find("h3", {"class": "reviewTitle"}).text.strip()
    title, rating_str = review_title.rsplit(" - ", maxsplit=1)
    rating = int(rating_str.split("%")[0].strip())

    profile_menu = review_html.find("a", {"class": "profileMenu"})
    author: str = profile_menu.get_text(strip=True)
    author_link: str = profile_menu["href"].strip()
    date: str = (
        profile_menu.next_sibling.get_text(separator=", ", strip=True)
        .split(", ", maxsplit=1)[1]
        .strip()
    )

    content: str = review_html.find("div", {"class": "reviewContent"}).text.strip()
    review_url: str = f"{url}{author.replace(' ', '_')}"

    return Review(
        title=title,
        rating=rating,
        author=User(name=author, url=author_link),
        date=extract_date(date),
        content=content,
        url=review_url,
        album=album,
    )


def find_reviews(session: CachedSession | Session, result: enmet.Album) -> list[Review]:
    """
    Find reviews for an album on Encyclopaedia Metallum.

    Args:
        session (CachedSession): The cached session to use for making requests.
        result (enmet.Album): The album object to search for reviews.

    Returns:
        list[Review]: The list of reviews found for the album.
    """
    if not result.reviews:
        print(f"No reviews available for album {result} by {result.bands}")
        return []

    url, data = result.reviews
    print(url, data)

    response = send_request(session, url)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews: ResultSet[Any] = soup.find_all("div", {"class": "reviewBox"})

    return [process_review(url, result, r) for r in reviews]


def fetch_reviews(
    session: CachedSession | Session, results: list[enmet.Album], total_results: int
) -> list[Review]:
    """
    Fetch reviews for a list of album search results.

    Args:
        session (CachedSession): The cached session to use for making requests.
        results (list[enmet.Album]): The list of album search results.
        total_results (int): The total number of results found for the search.

    Returns:
        list[Review]: The list of reviews found for the albums.
    """
    if not results:
        print("No results found")

    reviews_list: list[Review] = []
    with progress:
        task = progress.add_task("Searching for reviews...", total=total_results)
        for result in results:
            reviews: list[Review] = find_reviews(session, result)
            for review in reviews_list:
                # print(review.album)
                print(review, end="")
                # Send test request to the review URL to ensure it's valid
                send_request(session, review.url)
            reviews_list.extend(reviews)
            progress.update(task, advance=1)
            break

    return reviews_list
