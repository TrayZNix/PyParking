import pickle

from models import Parking


def saveAll(parking):
    with open('parking.pkl', 'wb') as f:
        pickle.dump(parking, f)


def findAll():
    with open("parking.pkl", 'rb') as pick:
        return pickle.load(pick)
