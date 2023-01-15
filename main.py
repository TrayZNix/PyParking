from models.Parking import Parking, Espacio
from models.Coche import Coche
from models.Motocicleta import Motocicleta
from models.Ticket import Ticket
from models.VehiculoMovilidadReducida import VehiculoMovilidadReducida
import numpy as np
import random as r
import pickle
import threading as thr

from repositories import RepoParking

repo_parking = RepoParking

def autoguardado():
    repo_parking.saveAll(parking)
    thr.Timer(60.0, autoguardado).start()


print("Bienvenido")
try:
    repo_parking.findAll()
    autoguardado()
    # Intenta leer el fichero de parking
except:  # Si este no existe, crea un parking y lo guarda
    espacios = []
    fila_espacio = []
    cantidad_parking = 140
    espacio_coches = 70 * cantidad_parking / 100
    espacio_VMR = 15 * cantidad_parking / 100
    espacio_motos = 15 * cantidad_parking / 100
    for i in range(1, cantidad_parking + 1):
        tipo = ""
        if espacio_coches != 0:
            tipo = "Coche"
            espacio_coches -= 1
        elif espacio_motos != 0:
            tipo = "Motocicleta"
            espacio_motos -= 1
        else:
            tipo = "VMR"
            espacio_VMR -= 1

        espacio = Espacio(i, (False if r.randint(0, 1) == 0 else True), tipo)
        fila_espacio.append(espacio)
        if i % 7 == 0:
            espacios.append(fila_espacio)
            fila_espacio = []

    parking = Parking("coords", np.array(espacios))
    with open('parking.pkl', 'wb') as f:
        pickle.dump(parking, f)
while True:
    print("Elija su rol: ")
    print("-------------------------------------------------------------------")
    print("1. Cliente")
    print("2. Administrador")
    lectura = str(input(""))
    if lectura == "1":
        print("__ __ __ __ __")
        print("1. Depositar vehiculo")
        print("2. Retirar vehiculo")
        print("3. Depositar abonados")
        print("4. Retirar abonados")
        lectura = str(input(""))
        if lectura == "1":
            espacios_libres_coche = 0
            espacios_libres_motos = 0
            espacios_libres_VMR = 0
            for fila in parking.espacios:
                for espacio in fila:
                    if espacio.ocupado:
                        if espacio.tipo_parking == "Coche":
                            espacios_libres_coche += 1
                        elif espacio.tipo_parking == "Motocicleta":
                            espacios_libres_motos += 1
                        else:
                            espacios_libres_VMR += 11
            print("Espacios libres:")
            print("........................")
            print("Coches: " + str(espacios_libres_coche))
            print("Motos: " + str(espacios_libres_motos))
            print("VMR: " + str(espacios_libres_VMR))
            print("........................")
            print("Introduzca su matrícula: ")
            matricula = str(input(""))
            print("........................")
            print("Elija según corresponda con su vehiculo:")
            print("0. Salir")
            print("1. Coche")
            print("2. Motocicleta")
            print("3. Vehiculo para personas con movilidad reducida (VMR)")
            tipo = str(input(" "))
            if tipo == "0":
                print(" <- ")
            if tipo == "1":
                tipo = "Coche"
                vehiculo = Coche("Toyota", "Avensis", matricula)
            if tipo == "2":
                tipo = "Motocicleta"
                vehiculo = Motocicleta("Kawasaki", "Ninja", matricula)
            if tipo == "3":
                tipo = "VMR"
                vehiculo = VehiculoMovilidadReducida("Scooters VRM", "", matricula)
            print("........................")
            for fila in parking.espacios:
                for espacio in fila:
                    if (not espacio.ocupado) and (espacio.tipo_parking == tipo):
                        espacio_asignado = espacio
            if 'espacio_asignado' in locals():
                tickets = []
                try:
                    with open("tickets.pkl", 'rb') as pick:
                        tickets = pickle.load(pick)
                except:
                    with open('tickets.pkl', 'wb') as f:
                        pickle.dump(tickets, f)
                print("La plaza asignada para usted es la plaza: " + str(espacio_asignado))
                ticket = Ticket(vehiculo)
                tickets.append(ticket)
                with open('tickets.pkl', 'wb') as f:
                    pickle.dump(tickets, f)
                print("Su ticket:")
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                print(str(ticket))
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                print("Recoja su ticket (Pulse enter)")
                input()
            else:
                print("No se te ha podido asignar un sitio")

            lectura = "0"

        elif lectura == "2":
            pass
        if lectura == "3":
            pass
        elif lectura == "4":
            pass
        elif lectura == "0":
            print("")
        else:
            print("Error al leer")

    elif lectura == "2":
        try:
            with open("tickets.pkl", 'rb') as pick:
                tickets = pickle.load(pick)
            print()
            print("-----------------------------")
            if len(tickets) == 0: print("No hay tickets")
            for ticket in tickets:
                print(str(ticket))
            print("-----------------------------")
            print()
        except:
            with open('tickets.pkl', 'wb') as f:
                pickle.dump([], f)
    elif lectura == "0":
        print("")
    else:
        print("Error al leer")

parking.verParking()
