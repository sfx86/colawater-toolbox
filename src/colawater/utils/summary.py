"""
Contains helper classes for managing tool summaries.

Examples:
    .. code-block:: python

        summary = SummaryBuilder()

        summary.add_header("Header content")
        summary.add_item("Item")
        summary.post() # Adds a message with the text "Header content\\n\\tItem"
        summary.clear() # To continue using this instance without initializing a new object

    .. code-block:: python

        summaries = SummaryCollection(["foo", "bar"])

        summaries.items["foo"].add_header("Header content") # Same API as SummaryBuilder()
        summaries.post() # Invokes post() for each summary in the collection
"""

import arcpy
from colawater.utils.constants import OUTPUT_DUMPED_MSG
from typing import Optional


class SummaryBuilder:
    """
    A helper class for iteratively building tool execution summaries.
    """

    def __init__(self) -> None:
        self._summary_list: list[str] = []

    @property
    def summary(self) -> str:
        """
        Returns the summary as a string.

        Returns:
            str: The content of the summary.
        """
        return "".join(self._summary_list)

    def add_header(
        self, layer_name: str, content: str, qualifier: Optional[str] = None
    ) -> None:
        """
        Adds a header to the summary's content.

        Arguments:
            layer_name (str): The name of the layer relevant to the header.
            content (str): The header content to be added.
        """
        if qualifier:
            contents = f"[{qualifier}] [{layer_name}] {content}"
        else:
            contents = f"[{layer_name}] {content}"

        if self._summary_list:
            self._summary_list.append(f"\n{contents}")
        else:
            self._summary_list.append(contents)

    def add_item(self, content: str) -> None:
        """
        Adds an item to the summary's content.

        Arguments:
            content (str): The item content to be added.
        """
        self._summary_list.append(f"\n\t{content}")

    def add_result(self, layer_name: str, content: str) -> None:
        """
        Adds a result header to the summary's content.

        Same behavior as ``add_header()`` but prepends the content with '[RESULT]'.

        Arguments:
            layer_name (str): The name of the layer relevant to the result.
            content (str): The result content to be added.
        """
        self.add_header(layer_name, content, "RESULT")

    def add_note(self, layer_name: str, content: str) -> None:
        """
        Adds a result header to the summary's content.

        Same behavior as ``add_header()`` but prepends the content with '[NOTE]'.

        Arguments:
            layer_name (str): The name of the layer relevant to the note.
            content (str): The note content to be added.
        """
        self.add_header(layer_name, content, "NOTE")

    def clear(self) -> None:
        """
        Clears the summary's content.
        """
        self._summary_list.clear()

    def post(self, dumped: bool = False) -> None:
        """
        Adds a message with the summary's content.

        Optionally add an additional message indicating the summary was
        dumped due to an error.

        Arguments:
            dumped (bool): Whether to add a message indicating the summary was
                           dumped due to an error.
        """
        if dumped:
            arcpy.AddMessage(OUTPUT_DUMPED_MSG)
        arcpy.AddMessage(self.summary)


class SummaryCollection:
    """
    A collection of ``SummaryBuilders``.

    Attributes:
        items (dict[str, SummaryBuilder]): A dictionary mapping summary names to
                                           a ``SummaryBuilder`` object.
    """

    def __init__(self, summaries: Optional[list[str]] = None) -> None:
        """
        Initializes the instance with an optional list of summaries.

        Arguments:
            summaries (Optional[list[str]])
        """
        self.items: dict[str, SummaryBuilder] = {}
        if summaries is not None:
            self.add_summaries(summaries)

    def add_summary(self, name: str) -> None:
        """
        Adds an empty summary to the collection.

        Arguments:
            name (str): The name of the summary.
        """
        self.items[name] = SummaryBuilder()

    def add_summaries(self, summaries: list[str]) -> None:
        """
        Adds summaries to the collection.

        Invokes ``add_summary()`` for each item in the list.

        Arguments:
            summaries (list[str]): A list of summary names to add to the collection.
        """
        for s in summaries:
            self.add_summary(s)

    def post(self, dumped: bool = False) -> None:
        """
        Posts all the summaries in the collection.

        Invokes ``post()`` for each summary in the collection.
        Optionally add an additional message indicating the summaries were
        dumped due to an error.

        Arguments:
            dumped (bool): Whether to add a message indicating the summaries were
                           dumped due to an error.
        """
        for s in self.items.values():
            s.post(dumped=dumped)

    def clear(self) -> None:
        """
        Removes all summaries in the collection.
        """
        self.items.clear()
