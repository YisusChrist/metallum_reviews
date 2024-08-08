"""Models for the project."""

from dataclasses import dataclass
from datetime import datetime

import enmet  # type:ignore


@dataclass
class User:
    """User class to represent a user on the site."""

    name: str
    url: str

    def __str__(self) -> str:
        return f"{self.name} ({self.url})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__str__()}>"


@dataclass
class Review:
    """Review class to represent a review on the site."""

    title: str
    rating: int
    author: User
    date: datetime
    content: str
    album: enmet.Album
    url: str

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
