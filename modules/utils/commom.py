from enum import Enum

from pydantic import BaseModel


class ArcanaType(str, Enum):
    MAJOR = "Major Arcana"
    MINOR = "Minor Arcana"


class CardReadingMethod(str, Enum):
    PAST_PRESENT_FUTURE = "past_present_future"
    CELTIC_CROSS = "celtic_cross"
    HAND_OF_ERIS = "hand_of_eris"


label4method = {
    CardReadingMethod.PAST_PRESENT_FUTURE: ["Past", "Present", "Future"],
    CardReadingMethod.CELTIC_CROSS: [
        "Situation",
        "Potential/Challenges",
        "Focus",
        "Past",
        "Possibilities",
        "Near Future",
        "Power",
        "Environment",
        "Hopes/Fears",
        "Outcomes",
    ],
    CardReadingMethod.HAND_OF_ERIS: [
        "About your question",
        "What may help you",
        "What may hinder you",
        "Possible outcome number 1",
        "Possible outcome number 2",
    ],
}


class Card(BaseModel):
    name: str
    number: int
    is_major_arcana: ArcanaType
    reversed: bool = False
    image_pth: str

    @property
    def is_major(self) -> bool:
        return self.is_major_arcana == ArcanaType.MAJOR
