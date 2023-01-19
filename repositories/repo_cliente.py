import pickle


class RepoCliente:
    @staticmethod
    def save_all(cliente_abonado):
        with open('clientes.pkl', 'wb') as f:
            pickle.dump(cliente_abonado, f)

    @staticmethod
    def find_all():
        with open("clientes.pkl", 'rb') as pick:
            return pickle.load(pick)
