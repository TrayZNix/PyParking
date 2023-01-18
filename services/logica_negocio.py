from models.parking import Espacio
from repositories.repo_parking import RepoParking


class LogicaNegocio:

    @staticmethod
    def encontrar_espacio_libre(tipo):
        parking = RepoParking.find_all()
        for fila in parking.espacios:
            for espacio in fila:
                if (not espacio.ocupado) and (espacio.tipo_parking == tipo) and not espacio.espacio_abonado:
                    return espacio

    @staticmethod
    def lectura_dni():
        while True:
            dni = str(input("Introduzca su DNI: ")).upper()
            if dni == "0":
                return None
            if LogicaNegocio.checkear_dni(dni):
                return dni
            else:
                print("DNI incorrecto")

    @staticmethod
    def checkear_dni(dni):
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        if len(dni) != 9:
            return False
        if not dni[:-1].isnumeric():
            return False
        return tabla[int(dni[:-1]) % 23] == dni[-1].upper()
