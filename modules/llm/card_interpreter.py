import os
from typing import Dict, List, Optional

from huggingface_hub import HfFolder, login
from transformers import pipeline

from modules.utils.commom import Card, CardReadingMethod

from ..interfaces.llm_interface import CardInterpreterInterface
from .rules import content

PIPELINE = None


def get_pipeline():
    global PIPELINE
    if PIPELINE is None:
        PIPELINE = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.2-1B-Instruct",
            device_map="auto",
            pad_token_id=2,
            model_kwargs={"low_cpu_mem_usage": True, "use_cache": False},
        )
    return PIPELINE


class CardInterpreter(CardInterpreterInterface):
    def __init__(self) -> None:
        # Login to Hugging Face
        hf_token = os.getenv("HF_TOKEN")
        if not HfFolder.get_token():
            login(token=hf_token)

        # Initialize pipeline
        self.pipeline = get_pipeline()

        # Base prompt template
        self._base_content = content

    def _format_card(self, card: Card) -> str:
        # Format card name with reversed state
        return f"{card.name} (Reversed)" if card.reversed else card.name

    def generate_prompt(
        self, cards: List[Card], context: str, method: CardReadingMethod
    ) -> List[Dict[str, str]]:
        method_templates = {
            CardReadingMethod.PAST_PRESENT_FUTURE: lambda: f"""The provided cards are:
                Past: {self._format_card(cards[0])}
                Present: {self._format_card(cards[1])}
                Future: {self._format_card(cards[2])}
            """,
            CardReadingMethod.CELTIC_CROSS: lambda: f"""The provided cards are:
                The situation: {self._format_card(cards[0])}
                Challenges: {self._format_card(cards[1])}
                What to focus on: {self._format_card(cards[2])}
                Your past: {self._format_card(cards[3])}
                Your strengths: {self._format_card(cards[4])}
                Near future: {self._format_card(cards[5])}
                Suggested approach: {self._format_card(cards[6])}
                What you need to know: {self._format_card(cards[7])}
                Your hopes and fears: {self._format_card(cards[8])}
                Outcomes: {self._format_card(cards[9])}
            """,
            CardReadingMethod.HAND_OF_ERIS: lambda: f"""The provided cards are:
                About your question: {self._format_card(cards[0])}
                What may help you: {self._format_card(cards[1])}
                What may hinder you: {self._format_card(cards[2])}
                Possible outcome number 1: {self._format_card(cards[3])}
                Possible outcome number 2: {self._format_card(cards[4])}
            """,
        }

        question = method_templates[method]()
        question += (
            f"\nIn the context of: {context}\nDrawn with the method: {method.value}"
        )

        return [
            {"role": "system", "content": self._base_content},
            {"role": "user", "content": question},
        ]

    def generate_interpretation(
        self, cards: List[Card], context: Optional[str], method: CardReadingMethod
    ) -> str:
        prompt = self.generate_prompt(cards, context or "General reading", method)
        result = self.pipeline(
            prompt,
            max_new_tokens=512,
            num_return_sequences=1,
            do_sample=False,
        )
        return result[0]["generated_text"][-1]["content"]
