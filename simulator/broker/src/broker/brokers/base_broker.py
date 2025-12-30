from abc import ABC, abstractmethod


class BaseBroker(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.broker = None

    @abstractmethod
    def push_to_target(self, topic: str, batch: list[str]):
        pass
