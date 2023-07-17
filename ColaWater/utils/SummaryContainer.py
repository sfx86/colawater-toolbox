import utils


class SummaryContainer:
    def __init__(self):
        pass

    def add_summary(self, name: str) -> None:
        self.__dict__[name] = utils.SummaryBuilder()

    def add_summaries(self, summaries: list[str]) -> None:
        for s in summaries:
            self.add_summary(s)

    def post(self) -> None:
        for s in self.__dict__.values():
            s.post()
