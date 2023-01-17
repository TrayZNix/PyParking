from models.vehiculo import Vehiculo


class ClienteAbonado:
    __nombre = ""
    __dni = ""
    __vehiculo = Vehiculo

    def __init__(self, nombre, dni, vehiculo):
        self.nombre = nombre
        self.dni = dni
        self.vehiculo = vehiculo

    def __str__(self):
        return self.nombre + ", con DNI '" + self.dni + "', poseedor del vehiculo: " + str(self.vehiculo)

    @property
    def nombre(self):
        return self.__nombre
    @property
    def dni(self):
        return self.__dni
    @property
    def vehiculo(self):
        return self.__vehiculo

    @nombre.setter
    def set_nombre(self, nombre):
        self.__nombre = nombre
    @dni.setter
    def set_dni(self, dni):
        self.__dni = dni
    @vehiculo.setter
    def set_vehiculo(self, vehiculo):
        self.__vehiculo = vehiculo
