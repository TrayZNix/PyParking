# from repositories.repo_abono import RepoAbono
from repositories.repo_cliente import RepoCliente


class ServicioAbono:
    @staticmethod
    def elegir_abono():
        abonos = RepoCliente().find_all()["Abonado"]
        if not len(abonos) == 0:
            print("__ __ __ __ Abonos: ")
            indice = 0
            for idx, abono in enumerate(abonos):
                print("")
                print("-- Abono nº" + str(idx + 1) + " -- -- -- -- -- -- -- -- -- --")
                print(str(abono))
                print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                print("")
            print("__ __ __ __")
            loop_abono = True
            while loop_abono:
                print("¿Qué abono desea editar? (Escriba 0 para volver atras)")
                try:
                    numero_abono = abs(int(input("-> ")))
                    print(str(numero_abono))
                except ValueError:
                    # print("Error de lectura")
                    numero_abono = None
                    pass
                if numero_abono == "0":
                    return None, None
                elif numero_abono is not None:
                    indice = numero_abono - 1
                    if indice < 0:
                        return 0, None
                    try:
                        abono = abonos[indice]
                        print("Ha elegido el siguiente abono: ")
                        print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                        print(str(abono))
                        print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
                        return indice, abono
                    except IndexError:
                        print("Ha elegido un abono que no existe")
                else:
                    print("Error de lectura")
        else:
            print("No hay abonos guardados")
            return None, None
    @staticmethod
    def eliminar_abono_existente_por_index(idx):
        clientes = RepoCliente.find_all()
        abonos = clientes.get("Abonado")
        del abonos[idx]
        clientes["Abonado"] = abonos
        RepoCliente.save_all(clientes)

    @staticmethod
    def encontrar_abono_por_dni(dni, matricula):
        abonados = RepoCliente.find_all().get("Abonado")
        for abonado in abonados:
            if (abonado.dni == dni) & (abonado.matricula == matricula):
                return abonado
        return None

    @staticmethod
    def checkear_abono_activo(dni):
        abonados = RepoCliente.find_all().get("Abonado")
        for abono in abonados:
            if abono.dni == dni:
                return True
        return False