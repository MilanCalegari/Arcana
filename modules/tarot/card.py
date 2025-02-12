import json
import os
import random

from ..utils.commom import Card, CardReadingMethod


class TarotDeck:
    def __init__(self):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        data_dir = os.path.join(base_dir, "data")
        json_file = os.path.join(data_dir, "tarot-images.json")

        print(f"TarotDeck looking for JSON at: {json_file}")

        with open(json_file) as f:
            self.cards_json = json.load(f)

    def get_cards(self):
        cards = []
        for card_data in self.cards_json["cards"]:
            name = card_data["name"]
            number = int(card_data["number"])
            is_major_arcana = card_data["arcana"]
            image_pth = os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                "data",
                "cards",
                card_data["img"],
            )

            card = Card(
                name=name,
                number=number,
                is_major_arcana=is_major_arcana,
                image_pth=image_pth,
            )
            cards.append(card)

        self.cards = cards

    def shuffle(self, reversal_prob: float):
        random.shuffle(self.cards)
        for card in self.cards:
            card.reversed = random.random() < reversal_prob

        return self.cards

    def draw(self, method: CardReadingMethod = CardReadingMethod.PAST_PRESENT_FUTURE):
        if method == CardReadingMethod.PAST_PRESENT_FUTURE:
            return self.cards[0:3]
        elif method == CardReadingMethod.CELTIC_CROSS:
            return self.cards[0:10]
        elif method == CardReadingMethod.HAND_OF_ERIS:
            return self.cards[0:5]
        else:
            raise ValueError(f"Invalid method: {method}")
