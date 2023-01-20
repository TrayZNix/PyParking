import datetime
import math
import os
import pickle
import random as r
import sys
import threading as thr

import timedelta
from timedelta import Timedelta

from models.abono import Abono
from models.cliente import Cliente
from models.cobro import Cobro
from models.parking import Parking, Espacio
from models.ticket import Ticket
from repositories.repo_cobro import RepoCobro
from repositories.repo_parking import RepoParking
from repositories.repo_ticket import RepoTicket
from repositories.repo_cliente import RepoCliente
from services.impresiones_service import ImpresionesService
from services.logica_negocio import LogicaNegocio
from services.servicio_abonos import ServicioAbono
from services.servicio_lectura import Lectura
from services.servicio_parking import ServicioParking

# Variables
tarifa_coche = 0.12
tarifa_motocicleta = 0.08
tarifa_vmr = 0.1
mensualidades = {
    "Mensual": {"Tiempo": Timedelta(days=31), "Precio": 25.00},
    "Trimestral": {"Tiempo": Timedelta(days=92), "Precio": 70.00},
    "Semestral": {"Tiempo": Timedelta(days=182), "Precio": 130.00},
    "Anual": {"Tiempo": Timedelta(days=365), "Precio": 200.00}
}
opciones = {
    "1": "Mensual",
    "2": "Trimestral",
    "3": "Semestral",
    "4": "Anual"
}


# Fin de variables


def autoguardado():
    # Cada 5 minutos se ejecutará este codigo, que guardará el valor de las variables en el pickle correspondiente
    RepoCliente.save_all(clientes)
    RepoParking.save_all(parking)
    RepoTicket.save_all(tickets)
    RepoCobro.save_all(cobros)
    thr.Timer(300.0, autoguardado).start()


# import time
# for x in range(2):
#     print("Cargando.", end='')
#     time.sleep(1)
#     print("Cargando.", end="\r")
#     print("Cargando..", end='')
#     time.sleep(1)
#     print("Cargando..", end="\r")
#     print("Cargando...", end='')
#     time.sleep(1)
#     print("Cargando...", end="\r")
# print("\r")
print("Bienvenido!")
print("...................")
print("")
try:
    clientes = RepoCliente.find_all()
except FileNotFoundError:
    clientes = {"Cliente": [], "Abonado": []}
    RepoCliente.save_all(clientes)
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
    # autoguardado() #Activación del autoguardado
    ImpresionesService().main_menu()
    try:
        lectura = str(abs(int(input("-> "))))
    except ValueError:
        lectura = "0"
    if lectura == "1":
        # os.system("cls")
        ImpresionesService().submenu_a()
        try:
            lectura = str(abs(int(input("-> "))))
        except ValueError:
            print("Ha habido un error al leer")
            lectura = "0"
        if lectura != "0":
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
                ImpresionesService().print_espacios_libres(
                    espacios_libres)  # IMPRIME LOS ESPACIOS DISPONIBLES SEGUN EL TIPO DE VEHICULO
                matricula = Lectura.leer_matricula()
                if matricula is not None:
                    ImpresionesService.submenuA_FM()
                    tipo = str(abs(int(input("-> "))))
                    if tipo == "0":
                        print("")
                    elif tipo in ["1", "2", "3"]:
                        cliente = Cliente(("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"), matricula)
                        tipo = ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR")
                        print("........................")
                        espacio_asignado = LogicaNegocio.encontrar_espacio_libre(tipo)
                        if espacio_asignado is not None:
                            tickets = RepoTicket.find_all()
                            print("La plaza asignada para usted es la plaza: " + str(espacio_asignado.numero))
                            espacio_asignado.ocupado = True
                            ServicioParking.edit_espacio(espacio_asignado)
                            ticket = Ticket(cliente, r.randint(100000, 999999), espacio_asignado.numero)
                            tickets.append(ticket)
                            RepoTicket.save_all(tickets)
                            clientes = RepoCliente.find_all()
                            clientes_normal = clientes.get("Cliente")
                            clientes_normal.append(Cliente(tipo, matricula))
                            clientes[Cliente] = clientes_normal
                            RepoCliente.save_all(clientes)
                            ImpresionesService().imprimir_ticket(ticket)
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
                        if ticket.cliente.matricula == matricula:
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
                                pin_correcto = Lectura.leer_pin(ticket.pin_validacion)
                                if pin_correcto & (plaza == str(ticket.plaza)):
                                    minutos = math.floor((datetime.datetime.now() - ticket.hora_entrada).seconds / 60)
                                    if ticket.cliente.tipo_vehiculo == "Coche":
                                        if ticket.cliente.tipo_vehiculo == "Coche":
                                            precio = parking.tarifa_coche
                                        elif ticket.cliente.tipo_vehiculo == "Motocicleta":
                                            precio = parking.tarifa_motocicleta
                                        else:
                                            precio = parking.tarifa_vrm
                                            precio = float(precio)
                                        plazaObj = ServicioParking().espacio_por_numero(int(plaza))
                                    print("Ha estado " + str(minutos) + " minutos en el parking")
                                    print("A " + str(precio) + "€/minuto, debe un total de: " + str(
                                        minutos * precio) + "€")
                                    sinRespuesta = True
                                    while sinRespuesta:
                                        ImpresionesService().decision_pago()
                                        decision = str(abs(int(input("-> "))))
                                        if decision == "1":
                                            sinRespuesta = False
                                            ticket.abonado = True
                                            RepoTicket.update_ticket(ticket)
                                            plazaObj.ocupado = False
                                            ServicioParking.edit_espacio(plazaObj)
                                            clientes = RepoCliente.find_all()
                                            clientes_normal = clientes.get("Cliente")
                                            indice = 0
                                            for idx, c in enumerate(clientes_normal):
                                                if c.matricula == matricula:
                                                    cliente = c
                                                    indice = idx
                                            del clientes_normal[indice]
                                            clientes["Cliente"] = clientes_normal
                                            RepoCliente.save_all(clientes)
                                            cobros.append(Cobro(cliente, (minutos * precio), False))
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
            elif lectura == "3":
                print("Introduzca su matrícula: ")
                matricula = str(input("-> ")).upper()
                dni = LogicaNegocio.lectura_dni()
                abonado = ServicioAbono.encontrar_abono_por_dni(dni)
                if abonado is not None:
                    desafio = Lectura.leer_pin(abonado.pin_abono)
                    if desafio:
                        espacio = ServicioParking().espacio_por_numero(abonado.numero_plaza)
                        espacio.ocupado = True
                        print(espacio)
                        ServicioParking.edit_espacio(espacio)
                        print("¡Bienvenido al parking!")
                else:
                    print("No se ha encontrado ningun abono con los datos introducidos anteriormente")
            elif lectura == "4":
                print("Introduzca la matrícula de su vehiculo: ")
                matricula = str(input("-> "))
                dni = LogicaNegocio.lectura_dni()
                if dni is not None:
                    abono = ServicioAbono.encontrar_abono_por_dni(dni)
                    error = True
                    while error:
                        try:
                            print("Introduzca la plaza en la que se encuentra su vehiculo: ")
                            numero = int(input("-> "))
                            espacio = ServicioParking().espacio_por_numero(numero)
                            print(str(espacio))
                        except ValueError:
                            print("Ha introducido un valor erroneo")
                        except IndexError:
                            print("Ese sitio no existe")
                        if espacio is not None:
                            error = False
                            print("Introduzca el pin desafio: ")
                            desafio = Lectura.leer_pin(abono.pin_abono)
                            if desafio:
                                espacio.ocupado = False
                                ServicioParking.edit_espacio(espacio)
                                print("¡Hasta pronto!")
        elif lectura == "0":
            print("")
        else:
            print("Error al leer")

    elif lectura == "2":
        ImpresionesService.submenu_b()
        lectura = str(abs(int(input("-> "))))
        print()
        if lectura == "0":
            pass
        elif lectura == "1":
            parking = RepoParking.find_all()
            os.system("cls")
            print(parking.verParking())
            input("Pulsa enter para continuar ->")
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
                                    ImpresionesService().imprimir_cobro(cobro)
                                    total_recaudado += cobro.cantidad_euros
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
            cobros = RepoCobro.find_all()
            abonos = RepoCliente.find_all().get("Abonado")
            cobros_abonos_no_activos = []
            total_recaudado = 0
            for cobro in cobros:
                total_recaudado += cobro.cantidad_euros
                if ServicioAbono.checkear_abono_activo(cobro.cliente.dni):
                    ImpresionesService().imprimir_cobro(cobro)
                else:
                    cobros_abonos_no_activos.append(cobro)
            if len(cobros_abonos_no_activos) != 0:
                print(" ================== Los siguientes cobros son de abonos que están dados de baja:")
                for cobro in cobros_abonos_no_activos:
                    ImpresionesService().imprimir_cobro(cobro)
            print("Se ha recaudado un total de: " + str(total_recaudado) + "€")
        elif lectura == "4":
            loop = True;
            while loop:
                opcion = ""
                ImpresionesService().submenu_b_p4()
                opcion = str(abs(int(input("-> "))))
                if opcion == "0":
                    loop = False
                elif opcion == "1":
                    while loop:
                        ImpresionesService().tipo_mensualidad()
                        opcion = str(abs(int(input("-> "))))
                        if opcion == "0":
                            loop = False
                        elif opcion in ["1", "2", "3", "4"]:
                            while loop:
                                dni = LogicaNegocio.lectura_dni()
                                abono = ServicioAbono.encontrar_abono_por_dni(dni)
                                if abono is not None:
                                    print("El DNI introducido ya está asociado a un abono")
                                if dni is not None and abono is None:
                                    nombre = str(input("Introduzca su nombre: "))
                                    apellidos = str(input("Introduzca sus apellidos: "))
                                    email = str(input("Introduzca su email: "))
                                    tarjeta = str(
                                        input("Introduzca su tarjeta de credito, con guiones (0123-4567-8901-2345): "))
                                    lectura_incorrecta = True
                                    while lectura_incorrecta:
                                        ImpresionesService().submenuA_FM()
                                        tipo = str(abs(int(input("-> "))))
                                        if tipo in ["1", "2", "3"]:
                                            espacio_asignado = LogicaNegocio.encontrar_espacio_libre(
                                                ("Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"))
                                            if espacio_asignado is not None:
                                                while lectura_incorrecta:
                                                    print("Introduzca la matrícula de su vehiculo")
                                                    matricula = Lectura.leer_matricula()
                                                    print("Ha introducido: " + matricula)
                                                    print("¿Es correcto?")
                                                    lectura = str(input("1. Sí. *Otro*. No -> "))
                                                    if lectura == "1":
                                                        espacio_asignado.espacio_abonado = True
                                                        ServicioParking().edit_espacio(espacio_asignado)
                                                        mensualidad_elegida = opciones.get(opcion)
                                                        mensualidad = mensualidades.get(mensualidad_elegida)
                                                        abonado = Abono(nombre, apellidos, email, tarjeta, dni,
                                                                        mensualidad_elegida, mensualidad.get("Tiempo"),
                                                                        espacio_asignado.numero,
                                                                        (
                                                                            "Coche" if tipo == "1" else "Motocicleta" if tipo == "2" else "VMR"),
                                                                        matricula, r.randint(100000, 999999))
                                                        cobros = RepoCobro.find_all()
                                                        cobros.append(Cobro(abonado, mensualidad.get("Precio"), True))
                                                        RepoCobro.save_all(cobros)
                                                        ImpresionesService.imprimir_abonado(abonado)
                                                        clientes = RepoCliente.find_all()
                                                        clientes.get("Abonado").append(abonado)
                                                        RepoCliente.save_all(clientes)
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
                        ImpresionesService().decision_edicion()
                        decision = str(abs(int(input("-> "))))
                        if decision == "1":
                            print("El viejo DNI es" + abono.dni)
                            print("Configure el nuevo DNI")
                            dni = LogicaNegocio.lectura_dni()
                            print("Configure el nuevo nombre")
                            nombre = str(input("Nuevo nombre: "))
                            print("Configure los nuevos apellidos")
                            apellidos = str(input("Nuevos apelldios: "))
                            print("Configure el nuevo email")
                            email = str(input("Nuevo email: "))
                            print("Configure su tarjeta de credito, con guiones (0123-4567-7890-1234)")
                            tarjeta = str(input("Nuevo numero de tarjeta: "))
                            abono.dni = dni
                            abono.nombre = nombre
                            abono.apellidos = apellidos
                            abono.email = email
                            abono.tarjeta = tarjeta
                            clientes = RepoCliente.find_all()
                            abonados = clientes.get("Abonado")
                            abonados[numero_abono] = abono
                            clientes["Abonado"] = abonados
                            RepoCliente.save_all(clientes)
                            print("Abono modificado correctamente!")
                            loop_abono = False
                        elif decision == "2":
                            print("Respecto al día de hoy, renueva el abono con la mensualidad deseada:")
                            eleccion_mensualidad = True
                            while eleccion_mensualidad:
                                error = False
                                try:
                                    ImpresionesService().tipo_mensualidad()
                                    eleccion = str(abs(int(input("-> "))))
                                    mensualidad = mensualidades.get(list(mensualidades.keys())[int(eleccion) - 1])
                                except IndexError:
                                    print("Ha introducido un valor erroneo")
                                    error = True
                                if not error:
                                    abono.fecha_fin = datetime.datetime.now() + mensualidad.get("Tiempo")
                                    cobros = RepoCobro.find_all()
                                    cobros.append(Cobro(abono, mensualidad.get("Precio"), True))
                                    RepoCobro.save_all(cobros)
                                    print("Se ha actualizado el abono: ")
                                    ImpresionesService.imprimir_abonado(abono)
                                    clientes = RepoCliente.find_all()
                                    abonados = clientes.get("Abonado")
                                    abonados[numero_abono] = abono
                                    clientes["Abonado"] = abonados
                                    RepoCliente.save_all(clientes)
                                    eleccion_mensualidad = False
                                    loop_abono = False
                        elif decision == "0":
                            pass
                        else:
                            print("Error de lectura")

                elif opcion == "3":
                    idx, abono = ServicioAbono.elegir_abono()
                    if abono is not None:
                        print(idx)
                        print(abono)
                        confirmacion = ""
                        while confirmacion != "0":
                            ImpresionesService().decision_baja_abono()
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

            pass
        elif lectura == "5":
            opcion = ""
            loop = True
            while loop:
                ImpresionesService().menu_caducidad_abono()
                try:
                    opcion = str(abs(int(input("-> "))))
                except ValueError:
                    opcion = ""
                if opcion == "0":
                    loop = False
                if opcion == "1":
                    ImpresionesService().meses()
                    try:
                        opcion = str(abs(int(input("-> "))))
                    except ValueError:
                        opcion = ""
                    if opcion != "":
                        abonados = RepoCliente.find_all().get("Abonado")
                        abonos_del_mes_elegido = []
                        for abono in abonados:
                            if str(abono.fecha_fin.month) == opcion:
                                abonos_del_mes_elegido.append(abono)
                        if len(abonos_del_mes_elegido) == 0:
                            print("Ningun abono caduca en ese mes")
                        else:
                            print("Los siguientes abonos caducan en el mes elegido: ")
                            for abono in abonos_del_mes_elegido:
                                ImpresionesService.imprimir_abonado(abono)

                elif opcion == "2":
                    abonados = RepoCliente.find_all().get("Abonado")
                    abonos_prox_diez_dias = []
                    for abono in abonados:
                        if abono.fecha_fin <= (datetime.datetime.now() + timedelta.Timedelta(days=10)):
                            abonos_prox_diez_dias.append(abono)
                    if len(abonos_prox_diez_dias) == 0:
                        print("Ningun abono caducará en los próximos 10 dias")
                    else:
                        print("Los próximos abonos caducarán en los próximos 10 dias")
                        for abono in abonos_prox_diez_dias:
                            ImpresionesService.imprimir_abonado(abono)
                else:
                    print("Error al leer")
    else:
        print("Error al leer")
