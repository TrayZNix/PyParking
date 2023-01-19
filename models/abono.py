from datetime import datetime as dt
from timedelta import Timedelta

from models.cliente import Cliente


class Abono(Cliente):
    __fecha_inicio = dt
    __fecha_fin = dt
    __numero_plaza = 0
    __expirado = False
    __nombre = ""
    __apellidos = ""
    __email = ""
    __tarjeta_credito = ""
    __tipo_abono = ""
    __dni = ""
    __pin_abono = 0

    def __init__(self, nombre, apellidos, email, tarjeta_credito, dni, tipo_abono, tiempo_mensualidad, numero_plaza, tipo_vehiculo, matricula, pin_abono):
        super().__init__(tipo_vehiculo, matricula)
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__email == email
        self.__tarjeta_credito = tarjeta_credito
        self.__tipo_abono = tipo_abono
        self.__dni = dni
        self.__fecha_inicio = dt.now()
        self.__fecha_fin = dt.now() + tiempo_mensualidad
        self.__numero_plaza = numero_plaza
        self.__expirado = False
        self.__pin_abono = pin_abono

    def __str__(self):
        return "Cliente abonado: " + str(self.__nombre) + ". DNI: "+str(self.__dni) +"\n" \
               "Inicio abono: " + str(self.__fecha_inicio) + "\n" \
               "Fin abono: " + str(self.__fecha_fin) + "\n" \
               "Plaza asignada: " + str(self.__numero_plaza) + "\n" \
                "Vehiculo: " + super(Abono, self).__str__() + "\n " \
                "Su PIN es: "+ str(self.__pin_abono)


    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def email(self):
        return self.__email

    @property
    def tarjeta_credito(self):
        return self.__tarjeta_credito

    @property
    def tipo_abono(self):
        return self.__tipo_abono

    @apellidos.setter
    def apellidos(self, apellidos):
        self.__apellidos = apellidos

    @email.setter
    def email(self, email):
        self.__email = email

    @tarjeta_credito.setter
    def tarjeta_credito(self, tarjeta):
        self.__tarjeta_credito = tarjeta

    @tipo_abono.setter
    def tipo_abono(self, tipo_abono):
        self.__tipo_abono = tipo_abono

    @property
    def dni(self):
        return self.__dni

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

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @dni.setter
    def dni(self, dni):
        self.__dni = dni