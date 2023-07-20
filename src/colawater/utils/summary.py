import arcpy
from typing import Optional


class SummaryBuilder:
    """A helper class for iteratively building tool execution summaries."""

    def __init__(self) -> None:
        self._summary_content: list[str] = []

    def add_header(self, content: str) -> None:
        """Add a header to the summary's content."""
        if self._summary_content:
            self._summary_content.append(f"\n{content}")
        else:
            self._summary_content.append(content)

    def add_item(self, content: str) -> None:
        """Add an item to the summary's content."""
        self._summary_content.append(f"\n\t{content}")

    def clear(self) -> None:
        """Clear the summary's content."""
        self._summary_content.clear()

    def post(self, dumped: bool = False) -> None:
        """Add a message with the summary's content."""
        arcpy.AddMessage("".join(self._summary_content))
        if dumped:
            arcpy.AddMessage("[OUTPUT DUMPED DUE TO ERROR]")


class SummaryContainer:
    """A wrapper class for SummaryBuilder that can handle multiple summaries at once."""

    def __init__(self, summaries: Optional[list[str]] = None) -> None:
        self.items: dict[str, SummaryBuilder] = {}
        if summaries is not None:
            self.add_summaries(summaries)

    def add_summary(self, name: str) -> None:
        """Add a summary to the container."""
        self.items[name] = SummaryBuilder()

    def add_summaries(self, summaries: list[str]) -> None:
        """Invoke add_summary() for each item in the list."""
        for s in summaries:
            self.add_summary(s)

    def post(self, dumped: bool = False) -> None:
        """Invoke post() for each summary in the container."""
        for s in self.items.values():
            s.post(dumped=dumped)

    def clear(self) -> None:
        """Remove all summaries in the container."""
        self.__dict__.clear()
