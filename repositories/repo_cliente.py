import pickle


class RepoCliente:
    @staticmethod
    def save_all(cliente_abonado):
        with open('cliente_abonado.pkl', 'wb') as f:
            pickle.dump(cliente_abonado, f)

    @staticmethod
    def find_all():
        with open("cliente_abonado.pkl", 'rb') as pick:
            return pickle.load(pick)
