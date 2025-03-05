import os
from typing import List

from huggingface_hub import InferenceClient

from modules.utils.commom import Card, CardReadingMethod


class CardInterpreter:
    def __init__(self) -> None:
        hf_token = os.getenv("HF_TOKEN")
        self.client = InferenceClient(api_key=hf_token)

    def _format_card(self, card: Card):
        return f"{card.name} (Reversed)" if card.reversed else card.name

    def complet_prompt(self, cards, context, method) -> str:
        method_templates = {
            CardReadingMethod.PAST_PRESENT_FUTURE: lambda: f"""The provided cards are:
                Past: {self._format_card(cards[0])}
                Present: {self._format_card(cards[1])}
                Future: {self._format_card(cards[2])}

                The context are:
                {context}
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

                The context are:
                {context}
            """,
            CardReadingMethod.HAND_OF_ERIS: lambda: f"""The provided cards are:
                About your question: {self._format_card(cards[0])}
                What may help you: {self._format_card(cards[1])}
                What may hinder you: {self._format_card(cards[2])}
                Possible outcome number 1: {self._format_card(cards[3])}
                Possible outcome number 2: {self._format_card(cards[4])}

                The context are:
                {context}
            """,
        }

        return method_templates[method]()


    def generate_interpretation(self, cards: List[Card], context: str, method: CardReadingMethod) -> str:
        prompt = f"""
        You are specialized tarot reader. Your task is provide an insighful reading based on the drawn cards.

        Reading Guidelines:
            - Keep answers brief, focused and concise.
            - Only interpret reversed card when specified.
            - If a context is present, focous the reading on the context.
            - If the context is not present, give a daily life reading.
            - Do not mention the method name in the reading.

        Use the Rider Waiter Tarot symbolism and card imagery

        {self.complet_prompt(cards, context, method)}

        Before answers think step by step and make sure the the answer is complete for all the cards and giving a complete insight.

        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        result =  self.client.chat.completions.create(
            model="google/gemma-2-2b-it",
            messages=messages,
            max_tokens=1024,
            stream=False
        )

        return result["choices"][0]["message"]["content"]
