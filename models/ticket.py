from datetime import datetime as dt

from models.cliente import Cliente


class Ticket:
    __hora_entrada = dt
    __cliente = Cliente
    __abonado = False
    __plaza = 0
    __pin_validacion = 0

    def __init__(self, cliente, pin, plaza):
        self.__cliente = cliente
        self.__hora_entrada = dt.now()
        self.__abonado = False
        self.__plaza = plaza
        self.__pin_validacion = pin

    def __str__(self):
        return "Matricula: " + self.__cliente.matricula + ". " + "Hora de entrada: " + str(
            self.__hora_entrada) + ".\nTarifa aplicada: Tarifa de " + str(self.__cliente.tipo_vehiculo).lower() + ". " \
            + "Abonado: " + ("Sí." if self.__abonado else "No.") + \
            (("Recaudado: "+str(self.__total_recaudado)+"€") if self.__abonado else "") + \
            "Plaza: "+str(self.__plaza)

    @property
    def hora_entrada(self):
        return self.__hora_entrada


    @property
    def abonado(self):
        return self.__abonado

    @property
    def plaza(self):
        return self.__plaza

    @property
    def pin_validacion(self):
        return self.__pin_validacion

    @property
    def cliente(self):
        return self.__cliente

    @abonado.setter
    def abonado(self, abonado):
        self.__abonado = abonado

    @hora_entrada.setter
    def hora_entrada(self, entrada: dt):
        self.__hora_entrada = entrada


    @hora_entrada.setter
    def abonado(self, abonado: bool):
        self.__abonado = abonado

    @plaza.setter
    def plaza(self, plaza: int):
        self.__plaza = plaza

    @pin_validacion.setter
    def pin_validacion(self, pin: int):
        self.__pin_validacion = pin

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    def confirmar_pago(self, recaudado):
        self.__abonado = True
