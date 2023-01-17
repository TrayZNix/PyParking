from datetime import datetime as dt


class Abono:
    __dni_cliente_abonado = ""
    __fecha_inicio = dt
    __fecha_fin = dt
    __dinero_abonado = 0

    def __init__(self, dni, dt_inicio, dt_fin, abonado):
        self.__dni_cliente_abonado = dni
        self.__fecha_inicio = dt_inicio
        self.__fecha_fin = dt_fin
        self.__dinero_abonado = abonado

    def __str__(self):
        return "con DNI '" + self.dni

    @property
    def nombre(self):
        return self.__nombre

    @__dni_cliente_abonado.setter
    def set_vehiculo(self, dni):
        self.__dni_cliente_abonado = dni
