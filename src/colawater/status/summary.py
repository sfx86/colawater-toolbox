"""
Utilities for managing tool summaries.

Examples:
    .. code-block:: python

        import colawater.status.summary as sy

        sy.add_header("a subject", "helpful message")
        sy.add_item("helpful message") # etc. for other methods
        sy.post()

"""

from enum import Enum, unique
from functools import partial
from typing import Any, Iterable, Optional

import arcpy

import colawater.attribute as attr

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
            content (str): The content to be added.
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
    Returns a string correctly formatted with a subject prefix.

    Arguments:
        subject (str): The subject to be used.
        content (str): The content to be used.

    Returns:
        str: The correctly prefixed string.
    """
    return f"[{subject}] {content}"


def add_header(subject: str, content: str) -> None:
    """
    Adds a header to the summary's content.

    Arguments:
        subject (str): The subject of the header.
        content (str): The header content to be added.
    """
    _summary.append(_subject_str(subject, content), _ContentType.HEADER)


def add_item(content: str) -> None:
    """
    Adds an item to the summary's content.

    Arguments:
        content (str): The item content to be added.
    """
    _summary.append(content, _ContentType.ITEM)


def add_items(contents: Iterable[Iterable[Optional[Any]]], csv: bool = False) -> None:
    """
    Adds items from an interable of iterable to the summary's content.

    Optionally apply ``attribute.process()`` to each item.

    Arguments:
        content (Iterable[Iterable[Any]]): The contents to be added.
        csv (bool): Whether to apply CSV pre-processing.
    """
    if not contents:
        return

    process = partial(attr.process, csv=csv)
    for i in contents:
        add_item(", ".join(map(process, i)))


def add_note(subject: str, content: str) -> None:
    """
    Adds a note header to the summary's content.

    Arguments:
        subject (str): The subject of the header.
        content (str): The note content to be added.
    """
    _summary.append(_subject_str(subject, content), _ContentType.NOTE)


def add_result(subject: str, content: str) -> None:
    """
    Adds a result header to the summary's content.

    Arguments:
        subject (str): The subject of the header.
        content (str): The result content to be added.
    """
    _summary.append(_subject_str(subject, content), _ContentType.RESULT)


def clear() -> None:
    """
    Clears the summary's content.
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
    if dumped:
        add_header(OUTPUT_DUMPED_MSG, "")
    arcpy.AddMessage(_summary.text)
    clear()
