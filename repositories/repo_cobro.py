import pickle


class RepoCobro:
    @staticmethod
    def save_all(cobros):
        with open('cobros.pkl', 'wb') as f:
            pickle.dump(cobros, f)

    @staticmethod
    def find_all():
        with open("cobros.pkl", 'rb') as pick:
            return pickle.load(pick)
