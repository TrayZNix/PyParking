import datetime
import math
import pickle
import random as r
import threading as thr

import timedelta
from timedelta import Timedelta

from models.abono import Abono
from models.cliente import Cliente
from models.cobro import Cobro
from models.parking import Parking, Espacio
from models.ticket import Ticket
from models.vehiculo import Vehiculo
from repositories.repo_abono import RepoAbono
from repositories.repo_cobro import RepoCobro
from repositories.repo_parking import RepoParking
from repositories.repo_ticket import RepoTicket
from services.logica_negocio import LogicaNegocio
from services.servicio_abonos import ServicioAbono

tarifa_coche = 0.12
tarifa_motocicleta = 0.08
tarifa_vmr = 0.1
mensualidades = {
    "Mensual": {"Tiempo": Timedelta(days=31), "Precio": 25.00},
    "Trimestral": {"Tiempo": Timedelta(days=92), "Precio": 70.00},
    "Semestral": {"Tiempo": Timedelta(days=182), "Precio": 130.00},
    "Anual": {"Tiempo": Timedelta(days=365), "Precio": 200.00}
}

def autoguardado():
    RepoParking.save_all(parking)
    RepoTicket.save_all(tickets)
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
    cobros = RepoCobro.find_all()
except FileNotFoundError:
    cobros = []
    RepoCobro.save_all(cobros)
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
    try:
        lectura = str(abs(int(input("-> "))))
    except ValueError:
        lectura = "0"
    if lectura == "1":
        print("__ __ __ __ __")
        print("0. Salir")
        print("1. Depositar vehiculo")
        print("2. Retirar vehiculo")
        print("3. Depositar abonados")
        print("4. Retirar abonados")
        lectura = str(abs(int(input("-> "))))
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
            matricula = str(input("-> ")).upper()
            print("........................")
            print("Elija según corresponda con su vehiculo:")
            print("0. Salir")
            print("1. Coche")
            print("2. Motocicleta")
            print("3. Vehiculo para personas con movilidad reducida (VMR)")
            tipo = str(abs(int(input("-> "))))
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
                    print("Su pin es: " + str(ticket.pin_validacion))
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
                matricula = str(input("-> ")).upper()
                tickets = RepoTicket.find_all();
                matricula_encontrada = False
                for ticket in tickets:
                    if ticket.vehiculo.matricula == matricula:
                        ticketAPagar = ticket
                        matricula_encontrada = True
                if matricula_encontrada:
                    plazaNoEncontrada = True
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
                                        decision = str(abs(int(input("-> "))))
                                        if decision == "1":
                                            sinRespuesta = False
                                            ticket.abonado = True
                                            RepoTicket.update_ticket(ticket)
                                            plazaObj.ocupado = False
                                            RepoParking.edit_espacio(plazaObj)
                                            cobros.append(Cobro(None, (minutos * precio), False, matricula = matricula))
                                            RepoCobro.save_all(cobros)
                                            print("Muchas gracias! Buen viaje!")
                                            pin, plaza, matricula = "0", "0", "0"
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
        lectura = str(abs(int(input("-> "))))
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
                            cobros_en_fecha = []
                            for cobro in RepoCobro.find_all():
                                if (cobro.fecha_cobro > fecha_desde) & (
                                        cobro.fecha_cobro < fecha_hasta) & (not cobro.cobro_abono):
                                    cobros_en_fecha.append(cobro)
                            print("Tickets realizado entre las fechas introducidas:")
                            total_recaudado = 0.0
                            if len(cobros_en_fecha) != 0:
                                for cobro in cobros_en_fecha:
                                    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
                                print(str(cobro))
                                total_recaudado += cobro.cantidad_euros
                                print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
                                print("Total recaudado entre las fechas introducidas:")
                                print("{:.2f}".format(total_recaudado) + "€")
                            else:
                                print("No se han encontrado cobros realizados entre las fechas introducidas")
                        else:
                            loop = False
                    else:
                        loop = False
                except ValueError:
                    print("Error al leer")
        elif lectura == "3":
            # abonos = RepoAbono.find_all()
            # clientes_abonados = {}
            # for abono in abonos:
            #     if not abono.cliente_abonado.dni in clientes_abonados:

            pass
        elif lectura == "4":
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
                opcion = str(abs(int(input("-> "))))
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
                        opcion = str(abs(int(input("-> "))))
                        if opcion == "0":
                            loop = False
                        elif opcion in ["1", "2", "3", "4"]:
                            nombre = str(input("Introduzca su nombre: "))
                            dni = LogicaNegocio.lectura_dni()
                            if dni is not None:
                                lectura_incorrecta = True
                                while lectura_incorrecta:
                                    print("........................")
                                    print("Elija según corresponda con su vehiculo:")
                                    print("0. Salir")
                                    print("1. Coche")
                                    print("2. Motocicleta")
                                    print("3. Vehiculo para personas con movilidad reducida (VMR)")
                                    tipo = str(abs(int(input("-> "))))
                                    if tipo in ["1", "2", "3"]:
                                        espacio_asignado = LogicaNegocio.encontrar_espacio_libre(
                                            ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"))
                                        if espacio_asignado is not None:
                                            while lectura_incorrecta:
                                                matricula = str(input("Introduce la matricula de tu vehiculo: ")).upper()
                                                print("Ha introducido: " + matricula)
                                                print("¿Es correcto?")
                                                lectura = str(input("1. Sí. *Otro*. No -> "))
                                                if lectura == "1":
                                                    vehiculo = Vehiculo(("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"),
                                                                        matricula)
                                                    cliente = Cliente(nombre, dni, vehiculo)
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
                                                    mensualidad_elegida = opciones.get(opcion)
                                                    mensualidad = mensualidades.get(mensualidad_elegida)
                                                    abono = Abono(cliente, mensualidad.get("Tiempo"),
                                                                  espacio_asignado.numero)
                                                    cobros = RepoCobro.find_all()
                                                    print(str(mensualidad))
                                                    cobros.append(Cobro(cliente, mensualidad.get("Precio"), True))
                                                    RepoCobro.save_all(cobros)
                                                    print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                                                    print(str(abono))
                                                    print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                                                    abonos.append(abono)
                                                    RepoAbono.save_all(abonos)
                                                    print("Se ha registrado como abonado. Gracias por su compra")
                                                    lectura_incorrecta = False
                                                    loop = False
                                        else:
                                            print("No se ha encontrado un sitio libre que asignar")
                                    elif tipo == "0":
                                        lectura_incorrecta = False
                                    else:
                                        print("Error al leer")

                        else:
                            print("Error al leer")

                elif opcion == "2":
                    numero_abono, abono = ServicioAbono.elegir_abono()
                    if abono is not None:
                        print("¿Qué desea editar del abono?")
                        print("0. Salir")
                        print("1. Datos del cliente")
                        print("2. Fecha de fin del abono")
                        decision = str(abs(int(input("-> "))))
                        cliente = abono.cliente_abonado
                        if decision == "1":
                            print("El viejo DNI es" + cliente.dni)
                            print("Configure el nuevo DNI")
                            dni = LogicaNegocio.lectura_dni()
                            cliente.dni = dni
                            print("Configure el nuevo nombre")
                            nombre = str(input("Nuevo nombre: "))
                            cliente.nombre = nombre
                            abono.cliente_abonado = cliente
                            abonos[numero_abono] = abono
                            RepoAbono.save_all(abonos)
                            print("Abono modificado correctamente!")
                            loop_abono = False
                        elif decision == "2":
                            print("Respecto al día de hoy, renueva el abono con la mensualidad deseada:")
                            opciones = {
                                "1": "Mensual",
                                "2": "Trimestral",
                                "3": "Semestral",
                                "4": "Anual"
                            }
                            eleccion_mensualidad = True
                            while eleccion_mensualidad:
                                try:
                                    print("0. Salir")
                                    for idx, mensualidad in enumerate(mensualidades.keys()):
                                        print(str(idx + 1)+". "+mensualidad)
                                    eleccion = str(abs(int(input("-> "))))
                                    mensualidad = mensualidades.get(list(mensualidades.keys())[int(eleccion) - 1])
                                    abono.fecha_fin = datetime.datetime.now() + mensualidad.get("Tiempo")
                                    cobros = RepoCobro.find_all()
                                    cobros.append(Cobro(cliente, mensualidad.get("Precio"), True))
                                    RepoCobro.save_all(cobros)
                                    print("Se ha actualizado el abono: -- -- -- -- -- -- -- -- -- --")
                                    print(str(abono))
                                    print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                                    abonos[numero_abono] = abono
                                    RepoAbono.save_all(abonos)
                                    eleccion_mensualidad = False
                                    loop_abono = False
                                except IndexError:
                                    print("Ha introducido un valor erroneo")
                        elif decision == "0":
                            pass
                        else:
                            print("Error de lectura")

                elif opcion == "3":
                    idx, abono = ServicioAbono.elegir_abono()
                    if abono is not None:
                        confirmacion = ""
                        while confirmacion != "0":
                            print("-----------------------")
                            print("Dar de baja eliminará su reserva y vaciará el espacio")
                            print("¿Seguro quiere dar de baja este abono?")
                            print("0. No")
                            print("1. Sí")
                            confirmacion = str(abs(int(input("-> "))))
                            if confirmacion == "1":
                                ServicioAbono.eliminar_abono_existente_por_index(idx)
                                print("Abono borrado")
                                confirmacion = "0"
                            elif confirmacion == "0":
                                pass
                            else:
                                print("Error al leer")
                    else:
                        pass
                else:
                    print("Error al leer")

            # Modificar, dar de alta o de baja un abono

            pass
        elif lectura == "5":
            opcion = ""
            while opcion == "":
                print("Comprobar que abonos van a caducar: ----")
                print("0. Salir")
                print("1. Por mes")
                print("2. Proximos diez dias")
                print("----------------------------------")
                try:
                    opcion = str(abs(int(input("-> "))))
                except ValueError:
                    opcion = ""
                if opcion == "1":
                    print("Elija el mes a consultar: ---------------------------")
                    print("0. Salir")
                    print("1. Enero.  2. Febrero.  3. Marzo.  4. Abril.")
                    print("5. Mayo.  6. Junio.  7. Julio.  8. Agosto.")
                    print("9. Septiembre.  10. Octubre.  11. Noviembre.  12. Diciembre.")
                    print("-------------------------")
                    try:
                        opcion = str(abs(int(input("-> "))))
                    except ValueError:
                        opcion = ""
                    if opcion != "":
                        abonos = RepoAbono.find_all()
                        abonos_del_mes_elegido = []
                        for abono in abonos:
                            if str(abono.fecha_fin.month) == opcion:
                                abonos_del_mes_elegido.append(abono)
                        if len(abonos_del_mes_elegido) == 0:
                            print("Ningun abono caduca en ese mes")
                        else:
                            print("Los siguientes abonos caducan en el mes elegido: ")
                            for abono in abonos_del_mes_elegido:
                                print("-- -- -- -- -- -- -- -- -- -- -- -- -- ")
                                print(str(abono))
                            print("-- -- -- -- -- -- -- -- -- -- -- -- -- ")

                elif opcion == "2":
                    abonos = RepoAbono.find_all()
                    abonos_prox_diez_dias = []
                    for abono in abonos:
                        if abono.fecha_fin <= (datetime.datetime.now() + timedelta.Timedelta(days=10)):
                            abonos_prox_diez_dias.append(abono)
                    if len(abonos_prox_diez_dias) == 0:
                        print("Ningun abono caducará en los próximos 10 dias")
                    else:
                        print("Los próximos abonos caducarán en los próximos 10 dias")
                        for abono in abonos_prox_diez_dias:
                            print("-- -- -- -- -- -- -- -- -- -- -- -- -- ")
                            print(str(abono))
                        print("-- -- -- -- -- -- -- -- -- -- -- -- -- ")
                else:
                    print("Error al leer")
    else:
        print("Error al leer")
