import pickle


class RepoAbono:
    @staticmethod
    def save_all(cliente_abonado):
        with open('abono.pkl', 'wb') as f:
            pickle.dump(cliente_abonado, f)

    @staticmethod
    def find_all():
        with open("abono.pkl", 'rb') as pick:
            return pickle.load(pick)
