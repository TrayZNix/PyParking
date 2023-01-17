from datetime import datetime as dt
from timedelta import Timedelta


class Abono:
    __dni_cliente_abonado = ""
    __fecha_inicio = dt
    __fecha_fin = dt
    __dinero_abonado = 0

    def __init__(self, dni, tipo_mensualidad):
        # mensualidades = {
        #  "Mensual": {"Tiempo": Timedelta(days=31), "precio": 25.00},
        #  "Trimestral": {"Tiempo": Timedelta(days=92), "precio": 70.00},
        #  "Semestral": {"Tiempo": Timedelta(days=182), "precio": 130.00},
        #  "Anual": {"Tiempo": Timedelta(days=365), "precio": 25.00}
        #  }
        self.__dni_cliente_abonado = dni
        self.__fecha_inicio = dt.now()
        self.__fecha_fin = dt.now() + tipo_mensualidad["Tiempo"]
        self.__dinero_abonado = tipo_mensualidad["precio"]

    def __str__(self):
        return "\nDNI del cliente abonado: " + self.__dni_cliente_abonado + "\n" \
               "Inicio abono: " + str(self.__fecha_inicio) + "\n" \
               "Fin abono: " + str(self.__fecha_fin) + "\n" \
               "Pago realizado: " + str(self.__dinero_abonado)+"€\n"

    @property
    def dni_cliente_abonado(self):
        return self.__dni_cliente_abonado

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def dinero_abonado(self):
        return self.__dinero_abonado

    @dni_cliente_abonado.setter
    def dni_cliente_abonado(self, dni):
        self.__dni_cliente_abonado = dni

    @fecha_fin.setter
    def fecha_fin(self, fecha_fin):
        self.__fecha_fin = fecha_fin

    @fecha_inicio.setter
    def fecha_inicio(self, fecha_inicio):
        self.__fecha_inicio = fecha_inicio

    @dinero_abonado.setter
    def dinero_abonado(self, dinero):
        self.__dinero_abonado = dinero
