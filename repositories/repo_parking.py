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

    @staticmethod
    def edit_espacio(espacio_editado: Espacio):
        parking = RepoParking.find_all()
        for idx, fila in enumerate(parking.espacios):
            for sub_idx, espacio in enumerate(fila):
                if espacio.numero == espacio_editado.numero:
                    parking.espacios[idx][sub_idx] = espacio_editado
        RepoParking.save_all(parking)

    @staticmethod
    def espacio_por_numero(numero: int):
        parking = RepoParking.find_all()
        for fila in parking.espacios:
            for espacio in fila:
                if espacio.numero == numero:
                    return espacio
        return None
