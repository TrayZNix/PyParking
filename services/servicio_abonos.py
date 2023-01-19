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
                    indice = numero_abono - 1
                except ValueError:
                    # print("Error de lectura")
                    numero_abono = None
                    pass
                if numero_abono == "0":
                    return None, None
                elif numero_abono is not None:
                    try:
                        abono = abonos[numero_abono - 1]
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
        abonos = []
            # RepoAbono.find_all()
        del abonos[idx]
        # RepoAbono.save_all(abonos)
