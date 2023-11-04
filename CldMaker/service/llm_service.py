from abc import ABC, abstractmethod


class LLMServiceInterface(ABC):
    @abstractmethod
    def run_full_chain(self, required_input: dict):
        pass
