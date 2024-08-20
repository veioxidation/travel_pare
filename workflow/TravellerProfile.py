from typing import Optional, List
import pickle

from pydantic import BaseModel


class TravellerProfile(BaseModel):
    name: str
    physical_level: str
    personality: str
    interests: Optional[List[str]] = []
    languages: Optional[List[str]] = []

    def add_to_db(self):
        """
        Save object to postgres database
        :return:
        """
        # TOdo -> build database dump for the given
        pass

    @classmethod
    def get_from_db(cls, name):
        """
        Use Postgres db to get TravellerProfile based by unique name
        :param name:
        :return:
        """
        pass

    def __str__(self):
        return f"TravellerProfile(name={self.name}, physical_level={self.physical_level}, " \
               f"personality={self.personality}, interests={self.interests})"

    def get_traveller_description(self):
        """
        Return a genering description of the traveller.
        :return:
        """
        return f"{self.name} is a {self.physical_level} person with a {self.personality} personality. " \
               f"Interests: {', '.join(self.interests) or 'Unknown'}, languages spoken: {', '.join(self.languages) or 'Unknown'}"
    def get_traveler_intro_message(self):
        """
        Return a genering description of the traveller.
        :return:
        """
        return f"My name is {self.name}. My physical activity level is {self.physical_level}, my personality is {self.personality}. " \
               f"My interests: {', '.join(self.interests) or 'Unknown'}, languages spoken: {', '.join(self.languages) or 'Unknown'}"


def load_users_from_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        return pickle.load(f)


def save_users_to_pkl(users_list: list, pkl_file: str):
    with open(pkl_file, 'wb') as f:
        pickle.dump(users_list, f)


if __name__ == '__main__':
    tp1 = TravellerProfile(name='John',
                           physical_level='active',
                           personality='outgoing',
                           interests=['animals', 'adventure sports', 'surfing'])

    tp2 = TravellerProfile(name='Amy',
                           physical_level='moderate',
                           personality='introvert',
                           interests=['vegan food', 'animals', 'nature', 'spirituality', 'yoga'])

    travellers_list = [tp1, tp2]
    save_users_to_pkl(travellers_list, 'test_users.pkl')
