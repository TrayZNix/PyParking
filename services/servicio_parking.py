from models.parking import Espacio
from repositories.repo_parking import RepoParking


class ServicioParking:
    @staticmethod
    def edit_espacio(espacio_editado):
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