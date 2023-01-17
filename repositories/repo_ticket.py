import pickle


class RepoTicket:
    @staticmethod
    def save_all(tickets):
        with open('ticket.pkl', 'wb') as f:
            pickle.dump(tickets, f)

    @staticmethod
    def find_all():
        with open("ticket.pkl", 'rb') as pick:
            return pickle.load(pick)

    @staticmethod
    def update_ticket(ticket_editado):
        tickets = RepoTicket.find_all()
        for idx, ticket in enumerate(tickets):
            if (ticket.plaza == ticket_editado.plaza) & (ticket.hora_entrada == ticket_editado.hora_entrada):
                tickets[idx] = ticket_editado
        RepoTicket.save_all(tickets)
