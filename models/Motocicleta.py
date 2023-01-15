from models.Vehiculo import Vehiculo


class Motocicleta(Vehiculo):
    tarifa = 0.8

    def __init__(self, marca, modelo, matricula):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula

    def __str__(self):
        return "Motocicleta: " + self.marca + " " + self.modelo + ". Matrícula: " + self.matricula + "."
