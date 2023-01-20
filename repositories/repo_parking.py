import pickle

from models import parking
from models.parking import Espacio


class RepoParking:
    @staticmethod
    def save_all(parking):
        with open('parking.pkl', 'wb') as f:
            pickle.dump(parking, f)

    @staticmethod
    def find_all():
        with open("parking.pkl", 'rb') as pick:
            return pickle.load(pick)
