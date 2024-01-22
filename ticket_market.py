class User:
    def __init__(self, name):
        self.name = name
        self.tickets = []
        self.balance = 0.0


class Event:
    def __init__(self, name, initial_price, total_tickets, event_date):
        self.name = name
        self.initial_price = initial_price
        self.total_tickets = total_tickets
        self.event_date = event_date
        self.available_tickets = total_tickets


class Ticket:
    def __init__(self, event, price, owner):
        self.event = event
        self.price = price
        self.owner = owner


class Aptos:
    def __init__(self):
        self.events = []
        self.tickets = []

    def create_event(self, name, initial_price, total_tickets, event_date):
        event = Event(name, initial_price, total_tickets, event_date)
        self.events.append(event)

    def buy_ticket(self, event, buying_price, buyer):
        if event.available_tickets > 0:
            if buying_price >= event.initial_price:
                ticket = Ticket(event, buying_price, buyer)
                self.tickets.append(ticket)
                event.available_tickets -= 1
                buyer.tickets.append(ticket)  # Add ticket to the buyer's list of tickets
                return ticket
            else:
                return "The buying price should be equal to or higher than the initial price."
        else:
            return "There are no tickets available for this event."

    def sell_ticket(self, ticket, selling_price):
        if ticket.owner == self:
            ticket.price = selling_price
            return True
        else:
            return "You can only sell tickets that you own."


    def match_buyers_sellers(self):
        for event in self.events:
            event_tickets = [ticket for ticket in self.tickets if ticket.event == event]
            event_tickets.sort(key=lambda x: x.price)  # Sort tickets by price
            buyers = [ticket for ticket in event_tickets]
            sellers = [ticket for ticket in event_tickets]

            while buyers and sellers:
                buyer = buyers[0]
                seller = sellers[-1]

                if buyer.price >= seller.price:
                    commission = 0.01 * (buyer.price + seller.price)
                    buyer.owner.balance -= 0.005 * buyer.price
                    seller.owner.balance -= 0.005 * seller.price
                    buyer.owner.tickets.remove(buyer)  # Remove the specific ticket from the buyer's list
                    seller.owner.tickets.remove(seller)
                    buyer.owner.tickets.append(seller)
                    seller.owner.tickets.append(buyer)
                    buyer.owner.balance += commission
                    seller.owner.balance += commission
                    event.available_tickets -= 1

                if buyer in buyers:
                    buyers.remove(buyer)
                if seller in sellers:
                    sellers.remove(seller)


# Example usage
dapp = Aptos()

# Create an event
dapp.create_event("Concert", 100, 1000, "2024-01-30")

# Create users (representing event organizer, buyers, and sellers)
organizer = User("Organizer")
buyer1 = User("Buyer1")
buyer2 = User("Buyer2")
seller1 = User("Seller1")
seller2 = User("Seller2")

# Event organizer sets initial price
event = dapp.events[0]
event.initial_price = 150

# Buyers purchase tickets
ticket1 = dapp.buy_ticket(event, 200, buyer1)
ticket2 = dapp.buy_ticket(event, 180, buyer2)

# Sellers sell tickets
dapp.sell_ticket(ticket1, 250)
dapp.sell_ticket(ticket2, 220)

# Match buyers and sellers
dapp.match_buyers_sellers()
