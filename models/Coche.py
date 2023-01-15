from models.Vehiculo import Vehiculo


class Coche(Vehiculo):
    tarifa = 0.12

    def __init__(self, marca, modelo, matricula):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula

    def __str__(self):
        return "Coche: " + self.marca + " " + self.modelo + ". Matrícula: " + self.matricula + "."
