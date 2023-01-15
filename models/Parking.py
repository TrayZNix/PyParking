import numpy as np


class Espacio:
    numero = 0
    ocupado = False
    tipo_parking = "Vehiculo"

    def __init__(self, numero, ocupado, tipo_parking):
        self.numero = numero
        self.ocupado = ocupado
        self.tipo_parking = tipo_parking
    def __str__(self):
        return "[" + str(self.numero) + ("🚗" if self.tipo_parking == "Coche" else "🛵" if self.tipo_parking == "Motocicleta" else "🦽") + "]"" Vacío: " + ("❌ " if self.ocupado else "✔  ")
        # return """
        # ┌───┐
        #  """+str(self.numero)+"""
        #   """+("❌ " if self.ocupado else "✔  ")+"""
        # └───┘"""


class Parking:
    coordenadas = "no-coords"
    espacios = np.array([], dtype=Espacio)
    # espacios = []

    def __init__(self, coordenadas, espacios=[]):
        self.coordenadas = coordenadas
        self.espacios = espacios

    def __str__(self):
        return "Parking: Coordenadas: " + self.coordenadas + ". Espacios: " + str(self.espacios)

    def verParking(self):
        for idx, fila in enumerate(self.espacios):
            for espacio in fila:
                print(espacio, end=" ")
            print("")
            print("Calle " + str(
                idx + 1) + " =============================================================================================================================")
