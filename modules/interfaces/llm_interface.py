from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from modules.utils.commom import Card, CardReadingMethod


class CardInterpreterInterface(ABC):
    @abstractmethod
    def generate_interpretation(self, cards: List[Card], context: Optional[str], method: CardReadingMethod) -> str:
        ...

    @abstractmethod
    def generate_prompt(self, cards: List[Card], context: str, method: CardReadingMethod) -> List[Dict[str, str]]:
        ...
