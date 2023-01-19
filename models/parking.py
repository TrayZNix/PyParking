import numpy as np


class Espacio:
    __numero = 0
    __ocupado = False
    __espacio_abonado = False
    __tipo_parking = "Cliente"

    def __init__(self, numero, ocupado, tipo_parking):
        self.__numero = numero
        self.__ocupado = ocupado
        self.__tipo_parking = tipo_parking

    def __str__(self):
        return "[" + str(self.__numero) + (
            "🚗" if self.__tipo_parking == "Coche" else "🛵" if self.__tipo_parking == "Motocicleta" else "🦽") + (
            "💳" if self.__espacio_abonado else "🛑") + "]"" Vacio: " + (
            "❌ " if self.__ocupado else "✅ ")

    @property
    def numero(self):
        return self.__numero

    @property
    def ocupado(self):
        return self.__ocupado

    @property
    def espacio_abonado(self):
        return self.__espacio_abonado

    @property
    def tipo_parking(self):
        return self.__tipo_parking

    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    @ocupado.setter
    def ocupado(self, ocupado):
        self.__ocupado = ocupado

    @espacio_abonado.setter
    def espacio_abonado(self, espacio_abonado):
        self.__espacio_abonado = espacio_abonado

    @tipo_parking.setter
    def tipo_parking(self, tipo_parking):
        self.__tipo_parking = tipo_parking


class Parking:
    __tarifa_coche = 0
    __tarifa_vrm = 0
    __tarifa_motocicleta = 0
    __coordenadas = "no-coords"
    __espacios = []

    def __init__(self, coordenadas, espacios=[]):
        self.__coordenadas = coordenadas
        self.__espacios = espacios
        self.__tarifa_coche = 0.12
        self.__tarifa_vrm = 0.1
        self.__tarifa_motocicleta = 0.08

    def __str__(self):
        return "Parking: Coordenadas: " + self.__coordenadas + ". Espacios: " + str(self.__espacios)

    def verParking(self):
        for idx, fila in enumerate(self.__espacios):
            for espacio in fila:
                print(espacio, end=" ")
            print("")
            print("Calle " + str(
                idx + 1) + "==========================================================================================")

    @property
    def espacios(self):
        return self.__espacios

    @property
    def tarifa_coche(self):
        return self.__tarifa_coche

    @property
    def tarifa_motocicleta(self):
        return self.__tarifa_motocicleta

    @property
    def tarifa_vrm(self):
        return self.__tarifa_vrm

    @espacios.setter
    def espacios(self, espacios):
        self.__espacios = espacios

    @tarifa_coche.setter
    def tarifa_coche(self, precio: float):
        self.__tarifa_coche = precio

    @tarifa_motocicleta.setter
    def tarifa_motocicleta(self, precio: float):
        self.__tarifa_motocicleta = precio

    @tarifa_vrm.setter
    def tarifa_vrm(self, precio: float):
        self.__tarifa_vrm = precio
