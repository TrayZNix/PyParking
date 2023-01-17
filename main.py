import datetime
import math
import pickle
import random as r
import threading as thr

from timedelta import Timedelta

from models.abono import Abono
from models.cliente import Cliente
from models.parking import Parking, Espacio
from models.ticket import Ticket
from models.vehiculo import Vehiculo
from repositories.repo_abono import RepoAbono
from repositories.repo_cliente import RepoCliente
from repositories.repo_parking import RepoParking
from repositories.repo_ticket import RepoTicket
from services.logica_negocio import LogicaNegocio
tarifa_coche = 0.12
tarifa_motocicleta = 0.08
tarifa_vmr = 0.1
mensualidades = {
    "Mensual": {"Tiempo": Timedelta(days=31), "precio": 25.00},
    "Trimestral": {"Tiempo": Timedelta(days=92), "precio": 70.00},
    "Semestral": {"Tiempo": Timedelta(days=182), "precio": 130.00},
    "Anual": {"Tiempo": Timedelta(days=365), "precio": 25.00}
}

def autoguardado():
    RepoParking.save_all(parking)
    RepoTicket.save_all(tickets)
    RepoCliente.save_all(tickets)
    thr.Timer(60.0, autoguardado).start()


print("Bienvenido!")
print("...................")
print("")
try:
    abonos = RepoAbono.find_all()
except FileNotFoundError:
    abonos = []
    RepoAbono.save_all(abonos)
try:
    clientes = RepoCliente.find_all()
except FileNotFoundError:
    clientes = []
    RepoCliente.save_all(clientes)
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
            elif tipo in ["1", "2", "3"]:
                vehiculo = Vehiculo(("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"), matricula)
                tipo = ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR")
                print("........................")
                espacio_asignado = LogicaNegocio.encontrar_espacio_libre(tipo)
                if espacio_asignado is not None:
                    pin = r.randint(100000, 999999)
                    tickets = []
                    try:
                        tickets = RepoTicket.find_all()
                    except:
                        RepoTicket.save_all(tickets)
                    print("La plaza asignada para usted es la plaza: " + str(espacio_asignado.numero))
                    espacio_asignado.ocupado = True
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
            else:
                print("Error al leer el tipo de coche")
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
            # Todo ¿Esto que es?
            pass
        elif lectura == "4":
            clientes = RepoCliente.find_all()
            loop = True;
            while loop:
                opcion = ""
                print("........................")
                print("0. Salir")
                print("1. Dar de alta")
                print("2. Modificar abono")
                print("3. Dar de baja")
                print("........................")
                print("Elija una opcion:")
                opcion = str(input("-> "))
                if opcion == "0":
                    loop = False
                elif opcion == "1":
                    while loop:
                        print("........................")
                        print("0. Salir")
                        print("1. Mensual")
                        print("2. Trimestal")
                        print("3. Semestral")
                        print("4. Anual")
                        print("........................")
                        print("Elija una opcion:")
                        opcion = str(input("-> "))
                        if opcion == "0":
                            loop = False
                        elif opcion in ["1", "2", "3", "4"]:
                            nombre = str(input("Introduzca su nombre: "))
                            dniIncorrecto = True
                            while dniIncorrecto:
                                dni = str(input("Introduzca su DNI: ")).upper()
                                if LogicaNegocio.checkear_dni(dni):
                                    dniIncorrecto = False
                                else:
                                    print("DNI incorrecto")
                                dniIncorrecto = not LogicaNegocio.checkear_dni(dni)
                            if not dniIncorrecto:
                                lecturaIncorrecta = True
                                while lecturaIncorrecta:
                                    print("........................")
                                    print("Elija según corresponda con su vehiculo:")
                                    print("0. Salir")
                                    print("1. Coche")
                                    print("2. Motocicleta")
                                    print("3. Vehiculo para personas con movilidad reducida (VMR)")
                                    tipo = str(input("-> "))
                                    if tipo in ["1", "2", "3"]:
                                        espacio_asignado = LogicaNegocio.encontrar_espacio_libre(("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"))
                                        if espacio_asignado is not None:
                                            while lecturaIncorrecta:
                                                matricula = str(input("Introduce la matricula de tu vehiculo: "))
                                                print("Ha introducido: " + matricula)
                                                print("¿Es correcto?")
                                                lectura = str(input("1. Sí. *Otro*. No"))
                                                if lectura == "1":
                                                    vehiculo = Vehiculo(("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"), matricula)
                                                    clientes.append(Cliente(nombre, dni, vehiculo))
                                                    RepoCliente.save_all(clientes)
                                                    espacio_asignado.espacio_abonado = True
                                                    print(str(espacio_asignado))
                                                    RepoParking.edit_espacio(espacio_asignado)
                                                    abonos = RepoAbono().find_all()
                                                    opciones = {
                                                        "1": "Mensual",
                                                        "2": "Trimestral",
                                                        "3": "Semestral",
                                                        "4": "Anual"
                                                    }
                                                    mensualidad_elegida = opciones.get(tipo)
                                                    abono = Abono(dni, mensualidades.get(mensualidad_elegida))
                                                    print(str(abono))
                                                    abonos.append(abono)
                                                    print("Se ha registrado como abonado. Gracias por su compra")
                                                    lecturaIncorrecta = False
                                                    loop = False
                                        else:
                                            print("No se ha encontrado un sitio libre que asignar")
                                    elif tipo == "0":
                                        lecturaIncorrecta = False
                                    else:
                                        print("Error al leer")

                        else:
                            print("Error al leer")

                elif opcion == "2":
                    pass
                elif opcion == "3":
                    pass
                else:
                    print("Error al leer")

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
