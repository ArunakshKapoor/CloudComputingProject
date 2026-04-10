from abc import ABC, abstractmethod


class BaseConnector(ABC):
    name: str

    @abstractmethod
    def health_check(self) -> dict: ...

    @abstractmethod
    def simulate(self, action_type: str, payload: dict) -> dict: ...

    @abstractmethod
    def execute(self, action_type: str, payload: dict) -> dict: ...
