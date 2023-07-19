import arcpy


class SummaryBuilder:
    """A helper class for iteratively building tool execution summaries."""

    def __init__(self):
        self._summary_content = []

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

    def post(self, dumped=False) -> None:
        """Add a message with the summary's content."""
        arcpy.AddMessage("".join(self._summary_content))
        if dumped:
            arcpy.AddMessage("[OUTPUT DUMPED DUE TO ERROR]")
