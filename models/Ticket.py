from datetime import datetime as dt

from models.Vehiculo import Vehiculo

class Ticket:
    hora_entrada = dt
    vehiculo = Vehiculo
    abonado = False

    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.hora_entrada = dt.now()
        self.abonado = False

    def __str__(self):
        return "Matricula: " + self.vehiculo.matricula + ". " + "Hora de entrada: " + str(
            self.hora_entrada) + ". Tarifa: " + str(self.vehiculo.tarifa)+ "€/min"
