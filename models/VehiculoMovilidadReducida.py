from models.Vehiculo import Vehiculo


class VehiculoMovilidadReducida(Vehiculo):
    tarifa = 0.1

    def __init__(self, marca, modelo, matricula):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula

    def __str__(self):
        return "Coche: " + self.marca + " " + self.modelo + ". Matrícula: " + self.matricula + "."
