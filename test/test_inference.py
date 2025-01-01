from modules.llm.card_interpreter import CardInterpreter
from utils.commom import Card

cards = [
    Card(name="The Fool", number=0, is_major_arcana=True, image_pth="", reversed=True),
    Card(name="Five of Cups", number=5, is_major_arcana=False, image_pth="", reversed=False),
    Card(name="The Lovers", number=6, is_major_arcana=False, image_pth="", reversed=False),
    ]

interpreter = CardInterpreter()
response = interpreter.generate_interpretation(cards, "I'm feeling sad and lost")
print(response)
