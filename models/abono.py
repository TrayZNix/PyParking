from datetime import datetime as dt
from timedelta import Timedelta


class Abono:
    __cliente_abonado = ""
    __fecha_inicio = dt
    __fecha_fin = dt
    __numero_plaza = 0
    __expirado = False

    def __init__(self, cliente, tiempo_mensualidad, numero_plaza):
        self.__cliente_abonado = cliente
        self.__fecha_inicio = dt.now()
        self.__fecha_fin = dt.now() + tiempo_mensualidad
        self.__numero_plaza = numero_plaza
        self.__expirado = False

    def __str__(self):
        return "Cliente abonado: " + str(self.__cliente_abonado) + "\n" \
               "Inicio abono: " + str(self.__fecha_inicio) + "\n" \
               "Fin abono: " + str(self.__fecha_fin) + "\n" \
               "Plaza asignada: " + str(self.__numero_plaza)

    @property
    def cliente_abonado(self):
        return self.__cliente_abonado

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def dinero_abonado(self):
        return self.__dinero_abonado

    @property
    def numero_plaza(self):
        return self.__numero_plaza

    @property
    def expirado(self):
        return self.__expirado

    @cliente_abonado.setter
    def cliente_abonado(self, dni):
        self.__cliente_abonado = dni

    @fecha_fin.setter
    def fecha_fin(self, fecha_fin):
        self.__fecha_fin = fecha_fin

    @fecha_inicio.setter
    def fecha_inicio(self, fecha_inicio):
        self.__fecha_inicio = fecha_inicio

    @dinero_abonado.setter
    def dinero_abonado(self, dinero):
        self.__dinero_abonado = dinero

    @numero_plaza.setter
    def numero_plaza(self, numero):
        self.__numero_plaza = numero

    @expirado.setter
    def expirado(self, expirado):
        self.__expirado = expirado
