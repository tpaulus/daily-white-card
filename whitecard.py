import os
import json
import random
import requests


class Cards(object):
    """
    Work with the Cards Against Humanity Cards
    Card Source: https://www.crhallberg.com/cah/json/
    """
    cards = None

    @classmethod
    def load_cards(cls, filepath='cards.json'):
        with open(filepath) as cardFile:
            cls.cards = json.loads(cardFile.read())
        print("Loaded %d Black Cards" % len(cls.cards['blackCards']))
        print("Loaded %d White Cards" % len(cls.cards['whiteCards']))

    @classmethod
    def get_white_cards(cls):
        if cls.cards is None:
            cls.load_cards()
        return cls.cards['whiteCards']

    @classmethod
    def get_black_cards(cls):
        if cls.cards is None:
            cls.load_cards()
        return cls.cards['blackCards']


class GroupMe(object):
    """
    Communicate with GroupMe's API
    Docs: https://dev.groupme.com/tutorials/bots
    """
    BASE_URL = "https://api.groupme.com/v3"
    BOT_ID = os.environ['BOT_ID']

    @classmethod
    def post_message(cls, text):
        """
        Post a Message to the Group
        :param text: Message Text
        :type text: str
        :return:
        """
        print("Posting Message: " + text)

        r = requests.post(cls.BASE_URL + "/bots/post",
                          data={'bot_id': cls.BOT_ID,
                                'text': text})
        if r.status_code != 202:
            print("Problem Posting Message - " + r.text)
        else:
            print('Message Posted!')


if __name__ == "__main__":
    # Message Context
    MESSAGES = ['Today you are looking for... %s',
                'Can you find... %s',
                'How about... %s',
                '%s Find it!',
                '%s DO YOUR WORST!',
                '%s']

    # Pick a Random White Card & Message Context
    secure_random = random.SystemRandom()
    card = secure_random.choice(Cards.get_white_cards())
    message = secure_random.choice(MESSAGES)

    # Post the Card text to GroupMe
    GroupMe.post_message(message % card)
