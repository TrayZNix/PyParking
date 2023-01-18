import datetime

from models.cliente import Cliente
from datetime import datetime as dt


class Cobro:
    __cliente = Cliente
    __cantidad_euros = 0.00
    __fecha_cobro = dt
    __cobro_abono = False

    def __init__(self, cliente, cantidad, abono, matricula = None):
        self.__cliente = ("Anonimo. " if cliente is None else str(cliente)) + \
                         (("Matricula: " + str(matricula)) if matricula is not None else "")
        self.__cantidad_euros = cantidad
        self.__fecha_cobro = datetime.datetime.now()
        self.__cobro_abono = abono

    def __str__(self):
        return "Cliente: "+str(self.__cliente)+". \n" \
                "Fecha de cobro: "+str(self.__fecha_cobro)+". \n" \
                "Cantidad: "+str(self.__cantidad_euros)+"€."

    @property
    def cliente(self):
        return self.__cliente

    @property
    def cantidad_euros(self):
        return self.__cantidad_euros

    @property
    def fecha_cobro(self):
        return self.__fecha_cobro

    @property
    def cobro_abono(self):
        return self.__cobro_abono

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    @cantidad_euros.setter
    def cantidad_euros(self, cantidad):
        self.__cantidad_euros = cantidad

    @fecha_cobro.setter
    def fecha_cobro(self, fecha):
        self.__fecha_cobro = fecha

    @cobro_abono.setter
    def cobro_abono(self, tipo_cobro):
        self.__cobro_abono = tipo_cobro