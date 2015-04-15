
class Voyage(object):
    def __init__(self, aps_rate=7000, bb=200000):
        self.aps_rate = aps_rate
        self.bb = bb
        self.voyage_days = 0
        self.income = 0
        self.dop_rate = 0

    def __repr__(self):
        return ('Voyage(' + 
                ' '.join(['aps_rate:', '{:,.0f}'.format(self.aps_rate) + ' |',
                          'bb:', '{:,.0f}'.format(self.bb) + ' |',
                          'voyage_days:', '{:,.2f}'.format(self.voyage_days) + ' |',
                          'income:', '{:,.0f}'.format(self.income) + ' |',
                          'dop_rate:', '{:,.0f}'.format(self.dop_rate)]) +
                ')')

    def perform_leg(self, ship, leg):
        days_taken = leg.distance / (ship.speed * 24)
        self.voyage_days += days_taken
        ship.rob -= days_taken * ship.sea_consumption
        if leg.on_hire:
            self.income += days_taken * self.aps_rate
        else:
            self.income -= days_taken * ship.sea_consumption * ship.bunker_price
        self.dop_rate = self.income / self.voyage_days
        return self

    def perform_bb(self):
        self.income += self.bb
        self.dop_rate = self.income / self.voyage_days
        return self

    def perform_port(self, ship, port):
        self.voyage_days += port.days
        ship.rob -= port.days * ship.port_consumption
        if port.on_hire:
            self.income += port.days * self.aps_rate
        self.dop_rate = self.income / self.voyage_days
        return self

    def perform_bunkering(self, ship, bunkering):
        ship.bunker_price = (
            (ship.rob * ship.bunker_price + bunkering.quantity * bunkering.price) /
            (ship.rob + bunkering.quantity)
        )
        ship.rob += bunkering.quantity
        self.voyage_days += bunkering.days
        if bunkering.on_hire:
            self.income += bunkering.days * self.aps_rate
        self.dop_rate = self.income / self.voyage_days
        return self


class Leg(object):
    def __init__(self, distance=1000, on_hire=True):
        self.distance = distance
        self.on_hire = on_hire

    def __repr__(self):
        return ('Leg(' +
                ' '.join(['distance:', '{:,.0f}'.format(self.distance) + ' |',
                          'on-hire:', str(self.on_hire)]) +
                ')')


class Port(object):
    def __init__(self, days=3, on_hire=True):
        self.days = days
        self.on_hire = on_hire

    def __repr__(self):
        return ('Port(' +
                ' '.join(['days:', '{:,.2f}'.format(self.days) + ' |',
                          'on-hire:', str(self.on_hire)]) +
                ')')


class Ship(object):
    def __init__(self, speed=12, sea_consumption=24, port_consumption=4, rob=2000, bunker_price=400):
        self.speed = speed
        self.sea_consumption = sea_consumption
        self.port_consumption = port_consumption
        self.rob = rob
        self.bunker_price = bunker_price

    def __repr__(self):
        return ('Ship(' +
                ' '.join(['speed:', '{:,.2f}'.format(self.speed) + ' |',
                          'sea_consumption:', '{:,.2f}'.format(self.sea_consumption) + ' |',
                          'port_consumption:', '{:,.2f}'.format(self.port_consumption) + ' |',
                          'rob:', '{:,.0f}'.format(self.rob) + ' |',
                          'bunker_price:', '{:,.0f}'.format(self.bunker_price)]) +
                ')')


class Bunkering(object):
    def __init__(self, quantity=0, price=0, days=0, on_hire=True):
        self.quantity = quantity
        self.price = price
        self.days = days
        self.on_hire = on_hire

    def __repr__(self):
        return ('Bunkering(' +
                ' '.join(['quantity:', '{:,.0f}'.format(self.quantity) + ' |',
                          'price:', '{:,.0f}'.format(self.price) + ' |',
                          'days:', '{:,.2f}'.format(self.days) + ' |',
                          'on-hire:', str(self.on_hire)]) +
                ')')

###

v = Voyage()
l1 = Leg(1000, False)
l2 = Leg(10000)
s = Ship()
p1 = Port(3)
p2 = Port(5)
b = Bunkering(2000, 200, 1, True)


print(v); print(s); print(99 * '~')
v.perform_bunkering(s, b)
print(v); print(s); print(99 * '~')
v.perform_leg(s, l1)
print(v); print(s); print(99 * '~')
v.perform_bb()
print(v); print(s); print(99 * '~')
v.perform_port(s, p1)
print(v); print(s); print(99 * '~')
v.perform_leg(s, l2)
print(v); print(s); print(99 * '~')
v.perform_port(s, p2)
print(v); print(s); print(99 * '~')
print(v); print(s); print(99 * '~')
print('\n')
print('DOP equivalent is:', v.dop_rate)
print('ROB is:', s.rob)
print('\n')
print(l1)
print(p1)
print(b)

###