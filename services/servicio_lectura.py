from repositories.repo_cliente import RepoCliente


class Lectura:
    @staticmethod
    def leer_pin(pin_desafio):
        while True:
            print("Introduzca el PIN de validación")
            pin = str(input("-> "))
            if pin != str(pin_desafio):
                print("Pin incorrecto!")
            elif pin == "0":
                return False
            else:
                return True
    @staticmethod
    def leer_matricula():
        clientes = RepoCliente.find_all()
        error = True
        matricula = ""
        while error:
            matricula = str(input("-> ")).upper()
            if matricula == "0":
                return None
            else:
                error = False
            for cliente in clientes.get("Cliente"):
                if cliente.matricula == matricula:
                    print("Esa matricula ya se encuentra en el parking!")
                    error = True
            for cliente_abon in clientes.get("Abonado"):
                if cliente_abon.matricula == matricula:
                    print("Esa matrícula ya está registrada en un cliente abonado!")
                    error = True
        return matricula