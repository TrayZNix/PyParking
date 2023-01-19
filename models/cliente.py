class Cliente:
    __matricula = "0000XXX"
    __tipo_vehiculo = "indefinido"

    def __init__(self, tipo_vehiculo, matricula):
        self.__matricula = matricula
        self.__tipo_vehiculo = tipo_vehiculo

    def __str__(self):
        return self.tipo_vehiculo+": Matrícula: " + self.matricula + "."

    @property
    def matricula(self):
        return self.__matricula

    @property
    def tipo_vehiculo(self):
        return self.__tipo_vehiculo

    @matricula.setter
    def matricula(self, matricula):
        self.__matricula = matricula

    @tipo_vehiculo.setter
    def tipo_vehiculo(self, tipo_vehiculo):
        self.__tipo_vehiculo = tipo_vehiculo


