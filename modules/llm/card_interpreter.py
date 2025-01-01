import os
from typing import Dict, List, Optional

from huggingface_hub import login
from transformers import pipeline

from modules.utils.commom import Card, CardReadingMethod

from ..interfaces.llm_interface import CardInterpreterInterface


class CardInterpreter(CardInterpreterInterface):
    def __init__(self) -> None:
        # Login to Hugging Face
        hf_token = os.getenv("HF_TOKEN")
        login(token=hf_token)
        # Initialize pipeline once and cache it
        self.pipeline = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.2-1B-Instruct",
            device_map="auto", 
            pad_token_id=128001,
        )
        
        # Cache base prompt content that doesn't change
        self._base_content = """
        You are a powerful occultist and exceptional tarot reader. Provide a concise reading based on the given cards.

        Focus on Rider Waite Tarot symbolism and card imagery.

        The possible methods are:
            - PAST_PRESENT_FUTURE: Three cards, past, present and future;
            - CELTIC_CROSS: Ten cards, the situation, challenges, what to focus on, your past, your strengths, near future, suggested approach, what you need to know, your hopes and fears, and outcomes;
            - HAND_OF_ERIS: Five cards, about your question, what may help you, what may hinder you, possible outcome number 1, and possible outcome number 2;

        Reading Guidelines:
            - Keep answers brief and focused;
            - Provide a summary overview;
            - Only interpret reversed cards when specified;
            - With context: Focus on context-specific interpretation;
            - Without context: Give practical daily guidance;

        If the context is General reading:
            - Provide a general daily life reading;
            - Focus on practical matters;

        If other context is provided:
            - Focus on the context provided;
            - Provide a reading related to the context;
            - Focus primarily on interpreting within the given context
            - Keep the symbolism of the cards first, but make sure to use the context to interpret the cards.
        """

    def _format_card(self, card: Card) -> str:
        # Helper to format card name
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
            """
        }

        question = method_templates[method]()
        question += f"\nIn the context of: {context}\nDrawn with the method: {method.value}"

        return [
            {"role": "system", "content": self._base_content},
            {"role": "user", "content": question}
        ]

    def generate_interpretation(
        self, cards: List[Card], context: Optional[str], method: CardReadingMethod
    ) -> str:
        prompt = self.generate_prompt(cards, context or "General reading", method)
        result = self.pipeline(
            prompt, 
            max_new_tokens=512,  # Limit token generation
            num_return_sequences=1,  # Only generate one response
            do_sample=False  # Deterministic output
        )
        return result[0]["generated_text"][-1]["content"]
