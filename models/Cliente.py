from models.Vehiculo import Vehiculo


class Cliente:
    nombre = ""
    dni = ""
    vehiculo = Vehiculo

    def __init__(self, nombre, dni, vehiculo):
        self.nombre = nombre
        self.dni = dni
        self.vehiculo = vehiculo

    def __str__(self):
        return self.nombre + ", con DNI '" + self.dni + "', poseedor del vehiculo: " + str(self.vehiculo)
