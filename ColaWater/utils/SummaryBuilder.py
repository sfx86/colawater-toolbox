import arcpy


class SummaryBuilder:
    """A helper class for iteratively building tool execution summaries."""

    def __init__(self):
        self._content = ""

    def add_header(self, content: str) -> None:
        """Add a header to the summary's content."""
        if self._content:
            self._content += f"\n{content}\n"
        else:
            self._content += f"{content}\n"

    def add_item(self, content: str) -> None:
        """Add an item to the summary's content."""
        self._content += f"\t{content}\n"

    def clear(self) -> None:
        """Clear the summary's content."""
        self._content = ""

    def post(self) -> None:
        """Add a message with the summary's content."""
        arcpy.AddMessage(self._content)
