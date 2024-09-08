from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

from app.main import app
from app.routers.ai_text_summarization import MIN_NUMBER_OF_WORDS_WORTH_TO_SUMMARIZE

from decouple import config

API_KEY = config("API_KEY")
API_KEY_NAME = config("API_KEY_NAME")

client = TestClient(app)

small_test_text = "I'm a string, please test me."
empty_string = ""
regular_text = """Baldur's Gate 3 Wiki covers the entirely next-generation RPG taking place in the Forgotten Realms® setting from Dungeons & Dragons® and is 20 years in the making. Return to the legendary city of Baldur's Gate® in a tale of fellowship and betrayal, sacrifice and survival and the lure of absolute power. Baldur's Gate 3 is developed and published by Larian Studios for Microsoft Windows and PlayStation 5. It is the third installment in the Baldur's Gate Series and will be set in the DnD universe from Wizards of the Coast. Players can expect to get their hands on the game on the 3rd of August, 2023 for the PC version, and on the 6th of September, 2023 for the PS5.\nBaldur's Gate 3 features a new story with several familiar characters from the Dungeons & Dragons campaign. Choose from a wide selection of D&D races and classes, or play as an origin character with a hand-crafted background. Adventure, loot, battle and romance as you journey through the Forgotten Realms and beyond. Play alone, and select your companions carefully, or as a party of up to four in multiplayer. Baldur's Gate 3 follows the 5th Edition Ruleset from DnD.

Gather your party, and return to the Forgotten Realms in a tale of fellowship and betrayal, sacrifice and survival, and the lure of absolute power. Mysterious abilities are awakening inside you, drawn from a Mind Flayer parasite planted in your brain. Resist, and turn darkness against itself. Or embrace corruption, and become ultimate evil. Abducted, infected, lost. You are turning into a monster, but as the corruption inside you grows, so does your power. That power may help you to survive, but there will be a price to pay, and more than any ability, the bonds of trust that you build within your party could be your greatest strength. Caught in a conflict between devils, deities, and sinister otherworldly forces, you will determine the fate of the Forgotten Realms together.

The Forgotten Realms are a vast, detailed and diverse world, and there are secrets to be discovered all around you -- verticality is a vital part of exploration. Sneak, dip, shove, climb, and jump as you journey from the depths of the Underdark to the glittering rooftops of the Upper City. How you survive, and the mark you leave on the world, is up to you.
"""


def test_input_not_string():
    response = client.post(
        "/summarize/", headers={API_KEY_NAME: API_KEY}, json={"text": 1}
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_input_string():
    response = client.post(
        "/summarize/",
        headers={API_KEY_NAME: API_KEY},
        json={"text": "I'm a string, please test me."},
    )

    assert response.status_code == HTTP_200_OK


def test_input_small_text():
    response = client.post(
        "/summarize/",
        headers={API_KEY_NAME: API_KEY},
        json={"text": small_test_text},
    )

    assert len(small_test_text.split(" ")) <= MIN_NUMBER_OF_WORDS_WORTH_TO_SUMMARIZE
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"summary": "Text not long enough. Nothing to summarize."}


def test_input_empty_string():
    response = client.post(
        "/summarize/",
        headers={API_KEY_NAME: API_KEY},
        json={"text": empty_string},
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {"summary": "Text is empty. Nothing to summarize."}


def test_input_regular_text():
    response = client.post(
        "/summarize/",
        headers={API_KEY_NAME: API_KEY},
        json={"text": regular_text},
    )

    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json()["summary"], str)
