import datetime
import math
from models.parking import Parking, Espacio
from models.ticket import Ticket
from models.vehiculo import Vehiculo
import random as r
import pickle
import threading as thr

from repositories.repo_cliente import RepoCliente
from repositories.repo_parking import RepoParking
from repositories.repo_ticket import RepoTicket

# repo_parking = RepoParking()
# repo_ticket = RepoTicket()
# repo_cliente = RepoCliente()
tarifa_coche = 0.12
tarifa_motocicleta = 0.08
tarifa_vmr = 0.1


def autoguardado():
    RepoParking.save_all(parking)
    RepoTicket.save_all(tickets)
    RepoCliente.save_all(tickets)
    thr.Timer(60.0, autoguardado).start()


print("Bienvenido!")
print("...................")
print("")
try:
    tickets = RepoTicket.find_all()
except FileNotFoundError:
    tickets = []
    RepoTicket.save_all(tickets)
try:
    parking = RepoParking.find_all()
    # Intenta leer el fichero de parking
except FileNotFoundError:  # Si este no existe, crea un parking y lo guarda
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

    parking = Parking("coords", espacios)
    with open('parking.pkl', 'wb') as f:
        pickle.dump(parking, f)
while True:
    # autoguardado()
    print("Elija su rol: ")
    print("-------------------------------------------------------------------")
    print("1. Cliente")
    print("2. Administrador")
    lectura = str(input("-> "))
    if lectura == "1":
        print("__ __ __ __ __")
        print("1. Depositar vehiculo")
        print("2. Retirar vehiculo")
        print("3. Depositar abonados")
        print("4. Retirar abonados")
        lectura = str(input("-> "))
        if lectura == "1":
            parking = RepoParking.find_all()
            espacios_libres = {"coches": 0, "motos": 0, "vrm": 0}
            for fila in parking.espacios:
                for espacio in fila:
                    if espacio.ocupado:
                        if espacio.tipo_parking == "Coche":
                            espacios_libres["coches"] += 1
                        elif espacio.tipo_parking == "Motocicleta":
                            espacios_libres["motos"] += 1
                        else:
                            espacios_libres["vrm"] += 1
            print("Espacios libres:")
            print("........................")
            print("Coches: " + str(espacios_libres.get("coches")))
            print("Motos: " + str(espacios_libres.get("motos")))
            print("VMR: " + str(espacios_libres.get("vrm")))
            print("........................")
            print("Introduzca su matrícula: ")
            matricula = str(input("-> "))
            print("........................")
            print("Elija según corresponda con su vehiculo:")
            print("0. Salir")
            print("1. Coche")
            print("2. Motocicleta")
            print("3. Vehiculo para personas con movilidad reducida (VMR)")
            tipo = str(input("-> "))
            if tipo == "0":
                print("")
            else:
                vehiculo = Vehiculo("Toyota", "Avensis",
                                    ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"), matricula)
                tipo = ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR")
                print(vehiculo)
                print("........................")
                for fila in parking.espacios:
                    for espacio in fila:
                        if (not espacio.ocupado) and (espacio.tipo_parking == tipo) and not espacio.espacio_abonado:
                            espacio_asignado = Espacio(espacio.numero, True, espacio.tipo_parking)

                if 'espacio_asignado' in locals():
                    pin = r.randint(100000, 999999)
                    tickets = []
                    try:
                        tickets = RepoTicket.find_all()
                    except:
                        RepoTicket.save_all(tickets)
                    print("La plaza asignada para usted es la plaza: " + str(espacio_asignado.numero))
                    RepoParking.edit_espacio(espacio_asignado)
                    ticket = Ticket(vehiculo, pin, espacio_asignado.numero)
                    tickets.append(ticket)
                    RepoTicket.save_all(tickets)
                    print("Su ticket:")
                    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    print(str(ticket))
                    print("Su pin es: "+str(ticket.pin_validacion))
                    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    print("Recoja su ticket (Pulse enter)")
                    input("-> ")
                else:
                    print("No se te ha podido asignar un sitio")
            lectura = "0"

        elif lectura == "2":
            parking = RepoParking.find_all()
            matricula = ""
            while matricula != "0":
                print("Escriba la matrícula del vehiculo, o 0 para salir: ")
                matricula = str(input("-> "))
                tickets = RepoTicket.find_all();
                matriculaEncontrada = False
                for ticket in tickets:
                    if ticket.vehiculo.matricula == matricula:
                        ticketAPagar = ticket
                        matriculaEncontrada = True
                if matriculaEncontrada:
                    plazaNoEncontrada = True
                    matricula = "0"
                    plaza = ""
                    while plaza != "0":
                        print("Introduzca la plaza en la que se encuentra su vehiculo, o 0 para salir: ")
                        plaza = str(input("-> "))
                        if plaza != str(ticket.plaza):
                            print("Plaza incorrecta!")
                        elif plaza == str(ticket.plaza):
                            pin = ""
                            while pin != "0":
                                print("Introduzca el PIN de validación")
                                pin = str(input("-> "))
                                if pin != str(ticket.pin_validacion):
                                    print("Pin incorrecto!")
                                elif plaza == str(ticket.plaza):
                                    minutos = math.floor((datetime.datetime.now() - ticket.hora_entrada).seconds / 60)
                                    if ticket.vehiculo.tipo_vehiculo == "Coche":
                                        if ticket.vehiculo.tipo_vehiculo == "Coche":
                                            precio = parking.tarifa_coche
                                        elif ticket.vehiculo.tipo_vehiculo == "Motocicleta":
                                            precio = parking.tarifa_motocicleta
                                        else:
                                            precio = parking.tarifa_vrm
                                            precio = float(precio)
                                        plazaObj = RepoParking.espacio_por_numero(int(plaza))
                                    print("Ha estado " + str(minutos) + " minutos en el parking")
                                    print("A " + str(precio) + "€/minuto, debe un total de: " + str(
                                        minutos * precio) + "€")
                                    sinRespuesta = True
                                    while sinRespuesta:
                                        print("...................................")
                                        print("Escriba su decisión")
                                        print("0. Salir")
                                        print("1. Pagar")
                                        print("...................................")
                                        decision = str(input("-> "))
                                        if decision == "1":
                                            sinRespuesta = False
                                            ticket.confirmar_pago(minutos * precio)
                                            RepoTicket.update_ticket(ticket)
                                            plazaObj.ocupado = False
                                            RepoParking.edit_espacio(plazaObj)
                                            print("Muchas gracias! Buen viaje!")
                                            pin = "0"
                                            plaza = "0"
                                            matricula = "0"
                                        elif decision == "0":
                                            sinRespuesta = False
                                            pin = "0"
                                        else:
                                            print("Error al leer")
                                else:
                                    pin = "0"
                                    plaza = "0"
                        else:
                            plaza = "0"
                else:
                    matricula = "0"
                    print("No se ha encontrado la matricula")
            lectura = "0"
        if lectura == "3":
            pass
        elif lectura == "4":
            pass
        elif lectura == "0":
            print("")
        else:
            print("Error al leer")

    elif lectura == "2":
        print("__ __ __ __ __")
        print("0. Atras")
        print("1. Estado del parking")
        print("2. Facturación")
        print("3. Consulta de abonados")
        print("4. Abonos")
        print("5. Caducidad de abonos")
        print("6. Ver todos los tickets")
        lectura = str(input("-> "))
        print()
        if lectura == "0":
            pass
        elif lectura == "1":
            parking = RepoParking.find_all()
            print(parking.verParking())
        elif lectura == "2":
            loop = True
            while loop:
                try:
                    fecha_leida = str(input("Desde: (DD-MM-AAAA, con guiones, o 0 para salir) -> "))
                    if fecha_leida != '0':
                        dia, mes, anyo = map(int, fecha_leida.split("-"))
                        fecha_desde = datetime.datetime(anyo, mes, dia)
                        fecha_leida = str(input("Hasta: (DD-MM-AAAA, con guiones, o 0 para salir) -> "))
                        if fecha_leida != '0':
                            dia, mes, anyo = map(int, fecha_leida.split("-"))
                            fecha_hasta = datetime.datetime(anyo, mes, dia)
                            print("A")
                            loop = False
                            tickets_en_fecha = []
                            for ticket in RepoTicket.find_all():
                                if (ticket.hora_entrada > fecha_desde) & (
                                        ticket.hora_entrada < fecha_hasta) & ticket.abonado:
                                    tickets_en_fecha.append(ticket)
                            print("Tickets realizado entre las fechas introducidas:")
                            total_recaudado = 0.0
                            for ticket in tickets_en_fecha:
                                print(str(ticket))
                                total_recaudado += ticket.total_recaudado
                            print("Total recaudado entre las fechas introducidas:")
                            print("{:.2f}".format(total_recaudado)+"€")
                        else:
                            loop = False
                    else:
                        loop = False
                except ValueError:
                    print("Error al leer")

        elif lectura == "3":
            # Ver abonos temporales
            pass
        elif lectura == "4":
            # Modificar, dar de alta o de baja un abono

            pass
        elif lectura == "5":
            # Ver abonos que caducan el mes elegido
            pass
        elif lectura == "6":
            tickets = RepoTicket.find_all()
            for ticket in tickets:
                print(str(ticket))
    else:
        print("Error al leer")
