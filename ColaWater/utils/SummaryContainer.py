import utils


class SummaryContainer:
    """A wrapper class for SummaryBuilder that can handle multiple summaries at once."""
    def __init__(self):
        pass

    def add_summary(self, name: str) -> None:
        """Add a summary to the container."""
        self.__dict__[name] = utils.SummaryBuilder()

    def add_summaries(self, summaries: list[str]) -> None:
        """Invoke add_summary() for each item in the list."""
        for s in summaries:
            self.add_summary(s)

    def post(self, dumped=False) -> None:
        """Invoke post() for each summary in the container."""
        for s in self.__dict__.values():
            s.post(dumped=dumped)

    def clear(self) -> None:
        """Remove all summaries in the container."""
        self.__dict__.clear()

