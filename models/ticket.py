from datetime import datetime as dt
from models.vehiculo import Vehiculo


class Ticket:
    __hora_entrada = dt
    __vehiculo = Vehiculo
    __abonado = False
    __plaza = 0
    __pin_validacion = 0

    def __init__(self, vehiculo, pin, plaza):
        self.__vehiculo = vehiculo
        self.__hora_entrada = dt.now()
        self.__abonado = False
        self.__plaza = plaza
        self.__pin_validacion = pin

    def __str__(self):
        return "Matricula: " + self.__vehiculo.matricula + ". " + "Hora de entrada: " + str(
            self.__hora_entrada) + ".\nTarifa aplicada: Tarifa de " + str(self.__vehiculo.tipo_vehiculo).lower() + ". " \
            + "Abonado: " + ("Sí." if self.__abonado else "No.") + (("Recaudado: "+str(self.__total_recaudado)+"€") if self.__abonado else "")

    @property
    def hora_entrada(self):
        return self.__hora_entrada

    @property
    def vehiculo(self):
        return self.__vehiculo

    @property
    def abonado(self):
        return self.__abonado

    @property
    def plaza(self):
        return self.__plaza

    @property
    def pin_validacion(self):
        return self.__pin_validacion

    @abonado.setter
    def abonado(self, abonado):
        self.__abonado = abonado

    @hora_entrada.setter
    def set_hora_entrada(self, entrada: dt):
        self.__hora_entrada = entrada

    @vehiculo.setter
    def set_vehiculo(self, vehiculo: Vehiculo):
        self.__vehiculo = vehiculo

    @hora_entrada.setter
    def set_abonado(self, abonado: bool):
        self.__abonado = abonado

    @plaza.setter
    def set_plaza(self, plaza: int):
        self.__plaza = plaza

    @pin_validacion.setter
    def set_pin_validacion(self, pin: int):
        self.__pin_validacion = pin


    def confirmar_pago(self, recaudado):
        self.__abonado = True
