"""Progress bar for the scraping process."""

from rich.progress import (BarColumn, Progress, TaskProgressColumn, TextColumn,
                           TimeRemainingColumn)

progress: Progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=None),  # Stretch the bar to fit the available width
    TaskProgressColumn("[progress.completed]{task.completed}/{task.total}"),
    TaskProgressColumn("[progress.percentage]{task.percentage:>5.2f}%"),
    TimeRemainingColumn(),
)
