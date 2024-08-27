"""Models for the project."""

from datetime import datetime

import enmet  # type:ignore
from pydantic import Field, HttpUrl
from pydantic.dataclasses import dataclass


@dataclass
class User:
    """User class to represent a user on the site."""

    name: str
    url: HttpUrl

    def __str__(self) -> str:
        return f"{self.name} ({self.url})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__str__()}>"


@dataclass(config={"arbitrary_types_allowed": True})
class Review:
    """Review class to represent a review on the site."""

    title: str
    author: User
    date: datetime
    content: str
    album: enmet.Album
    url: HttpUrl
    rating: int = Field(..., ge=0, le=100)

    def full_info(self) -> str:
        """
        Return the full information of the review.

        Returns:
            str: The full information of the review.
        """
        return f"""\
[cyan]Title[/]: {self.title}
[cyan]Rating[/]: {self.rating}%
[cyan]Author[/]: {self.author}
[cyan]Date[/]: {self.date}
[cyan]Album[/]: {self.album}
[cyan]URL[/]: {self.url}
[cyan]Content[/]: {self.content}
"""

    def __str__(self) -> str:
        return f"'{self.title}' ({self.rating}%) by {self.author} on {self.date} ({self.url})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__str__()}>"
