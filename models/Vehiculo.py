class Vehiculo:
    __marca = "default"
    __modelo = "default"
    __matricula = "0000XXX"
    __tipo_vehiculo = "indefinido"

    def __init__(self, marca, modelo, tipo_vehiculo, matricula):
        self.__marca = marca
        self.__modelo = modelo
        self.__matricula = matricula
        self.__tipo_vehiculo = tipo_vehiculo

    def __str__(self):
        return "Coche: " + self.__marca + " " + self.__modelo + ". Matrícula: " + self.__matricula + "."

    @property
    def marca(self):
        return self.__marca

    @property
    def matricula(self):
        return self.__matricula

    @property
    def modelo(self):
        return self.__modelo

    @property
    def tipo_vehiculo(self):
        return self.__tipo_vehiculo

    @marca.setter
    def marca(self, marca):
        self.__marca = marca

    @modelo.setter
    def modelo(self, modelo):
        self.__modelo = modelo

    @matricula.setter
    def matricula(self, matricula):
        self.__matricula = matricula

    @tipo_vehiculo.setter
    def tipo_vehiculo(self, tipo_vehiculo):
        self.__tipo_vehiculo = tipo_vehiculo
