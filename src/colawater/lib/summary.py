"""
Functions for managing tool summaries.

Examples:
    .. code-block:: python

        import colawater.status.summary as sy

        sy.add_header("a subject", "helpful message")
        sy.add_item("helpful message") # etc. for other methods
        sy.post()

"""

from collections.abc import Sequence
from enum import Enum, unique
from typing import Any, Optional

import arcpy

from . import attribute as attr

OUTPUT_DUMPED_MSG = "OUTPUT DUMPED DUE TO ERROR"
"""
Error message text to display when the summary output is dumped due to an error.
"""


@unique
class _ContentType(Enum):
    """
    The various content types.

    Enumerated values are the prefixes for the messages.
    """

    HEADER = ""
    ITEM = "\t"
    NOTE = "[NOTE] "
    RESULT = "[RESULT] "
    TOOL = "[TOOL] "


class _Summary:
    """
    Internal summary class to structure shared summary state.
    """

    def __init__(self) -> None:
        self._list: list[str] = []

    def __bool__(self) -> bool:
        return bool(self._list)

    @property
    def text(self) -> str:
        """
        Returns the summary text.

        Returns:
            str: The summary as a string.
        """
        return "\n".join(self._list)

    def append(self, content: str, type: _ContentType) -> None:
        """
        Appends a string to the summary.

        Arguments:
            content (str): A string containing the content.
            type (_ContentType): A content type.
        """
        self._list.append(f"{type.value}{content}")

    def clear(self) -> None:
        """
        Clears the internal list.
        """
        self._list.clear()


_summary = _Summary()
"""
The shared summary state.
"""


def _subject_str(subject: str, content: str) -> str:
    """
    Returns a string formatted with a subject prefix.

    Format: "[{subject}] {content}"

    Arguments:
        subject (str): A string containing the subject.
        content (str): A string containing the content.

    Returns:
        str: The correctly prefixed string.
    """
    return f"[{subject}] {content}"


def add_header(subject: str, content: str) -> None:
    """
    Adds a header to the summary's content.

    Arguments:
        subject (str): A string containing the subject.
        content (str): A string containing the content.
    """
    _summary.append(_subject_str(subject, content), _ContentType.HEADER)


def add_item(content: str) -> None:
    """
    Adds an item to the summary's content.

    Arguments:
        content (str): A string containing the content.
    """
    _summary.append(content, _ContentType.ITEM)


def add_items(contents: Sequence[Sequence[Optional[Any]]], csv: bool = False) -> None:
    """
    Adds items from an sequence of sequences to the summary's content.

    Optionally apply ``attribute.process()`` to each item.

    Arguments:
        content (Sequence[Sequence[Any]]): Rows to add as items (can be jagged).
        csv (bool): Whether to apply CSV pre-processing.
    """
    if len(contents) == 0:
        return

    for row in contents:
        add_item(", ".join(map(lambda item: attr.process(item, csv=csv), row)))


def add_note(subject: str, content: str) -> None:
    """
    Adds a note header to the summary's content.

    Arguments:
        subject (str): A string containing the subject.
        content (str): A string containing the content.
    """
    _summary.append(_subject_str(subject, content), _ContentType.NOTE)


def add_result(subject: str, content: str) -> None:
    """
    Adds a result header to the summary's content.

    Arguments:
        subject (str): A string containing the subject.
        content (str): A string containing the content.
    """
    _summary.append(_subject_str(subject, content), _ContentType.RESULT)


def clear() -> None:
    """
    Clears the summary.
    """
    _summary.clear()


def post(dumped: bool = False) -> None:
    """
    Adds a message with the summary's full text.

    Assembles all of the headers and miscellaneous messages in the order added.
    Clears summary content after posting message.
    Optionally add an additional message indicating the summary was
    dumped due to an error.

    Arguments:
        dumped (bool): Whether to add a message indicating the summary was
                       dumped due to an error.
    """
    # note:
    #   the added header will be *after* the other content
    if dumped:
        add_header(OUTPUT_DUMPED_MSG, "")
    arcpy.AddMessage(_summary.text)
    clear()
