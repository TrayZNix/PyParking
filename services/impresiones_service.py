import os


class ImpresionesService:
    @staticmethod
    def main_menu():
        os.system("cls")
        print("Elija su rol: ")
        print("-------------------------------------------------------------------")
        print("1. Cliente")
        print("2. Administrador")

    @staticmethod
    def submenu_a():
        os.system("cls")
        print("__ __ __ __ __")
        print("0. Salir")
        print("1. Depositar vehiculo")
        print("2. Retirar vehiculo")
        print("3. Depositar abonados")
        print("4. Retirar abonados")

    @staticmethod
    def submenu_b():
        os.system("cls")
        print("__ __ __ __ __")
        print("0. Atras")
        print("1. Estado del parking")
        print("2. Facturación")
        print("3. Consulta de abonados")
        print("4. Abonos")
        print("5. Caducidad de abonos")
        print("6. Ver todos los tickets")
    @staticmethod
    def print_espacios_libres(espacios_libres):
        os.system("cls")
        print("Espacios libres:")
        print("........................")
        print("Coches: " + str(espacios_libres.get("coches")))
        print("Motos: " + str(espacios_libres.get("motos")))
        print("VMR: " + str(espacios_libres.get("vrm")))
        print("........................")
        print("Introduzca su matrícula, o 0 para salir: ")
    @staticmethod
    def submenuA_FM():
        print("........................")
        print("Elija según corresponda con su vehiculo:")
        print("0. Salir")
        print("1. Coche")
        print("2. Motocicleta")
        print("3. Cliente para personas con movilidad reducida (VMR)")

    @staticmethod
    def imprimir_ticket(ticket):
        print("Su ticket:")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print(str(ticket))
        print("Su pin es: " + str(ticket.pin_validacion))
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Recoja su ticket (Pulse enter)")

    @staticmethod
    def decision_pago():
        print("...................................")
        print("Escriba su decisión")
        print("0. Salir")
        print("1. Pagar")
        print("...................................")

    @staticmethod
    def imprimir_cobro(cobro):
        print("->> ---------------------------------")
        print(str(cobro))
        print("-------------------------------------")

    @staticmethod
    def submenu_b_p4():
        print("........................")
        print("0. Salir")
        print("1. Dar de alta")
        print("2. Modificar abono")
        print("3. Dar de baja")
        print("........................")
        print("Elija una opcion:")

    @staticmethod
    def tipo_mensualidad():
        print("........................")
        print("0. Salir")
        print("1. Mensual")
        print("2. Trimestal")
        print("3. Semestral")
        print("4. Anual")
        print("........................")
        print("Elija una opcion:")

    @staticmethod
    def imprimir_abonado(abonado):
        print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
        print(str(abonado))
        print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")

    @staticmethod
    def decision_edicion():
        print("¿Qué desea editar del abono?")
        print("0. Salir")
        print("1. Datos del cliente")
        print("2. Fecha de fin del abono")

    @staticmethod
    def decision_baja_abono():
        print("-----------------------")
        print("Dar de baja eliminará su reserva y vaciará el espacio")
        print("¿Seguro quiere dar de baja este abono?")
        print("0. No")
        print("1. Sí")

    @staticmethod
    def menu_caducidad_abono():
        print("Comprobar que abonos van a caducar: ----")
        print("0. Salir")
        print("1. Por mes")
        print("2. Proximos diez dias")
        print("----------------------------------")

    @staticmethod
    def meses():
        print("Elija el mes a consultar: ---------------------------")
        print("0. Salir")
        print("1. Enero.  2. Febrero.  3. Marzo.  4. Abril.")
        print("5. Mayo.  6. Junio.  7. Julio.  8. Agosto.")
        print("9. Septiembre.  10. Octubre.  11. Noviembre.  12. Diciembre.")
        print("-------------------------")