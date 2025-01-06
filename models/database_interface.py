from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def enqueue_data(self, data: dict):
        pass

    @abstractmethod
    def dequeue_data(self) -> dict:
        pass

    @abstractmethod
    def get_all_data(self) -> list:
        pass
