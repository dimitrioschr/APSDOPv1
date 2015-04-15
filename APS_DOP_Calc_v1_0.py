
class Voyage(object):

    def __init__(self, APS_rate=7000, BB=200000):
        self.APS_rate = APS_rate
        self.BB = BB
        self.voyage_days = 0
        self.income = 0
        self.DOP_rate = 0

    def __repr__(self):
        return ('Voyage(' + 
                ' '.join(['APS:', '{:,.0f}'.format(self.APS_rate) + ' // ',
                          'BB:', '{:,.0f}'.format(self.BB) + ' // ',
                          'days:', '{:,.2f}'.format(self.voyage_days) + ' // ',
                          'income:', '{:,.0f}'.format(self.income) + ' // ',
                          'DOP:', '{:,.0f}'.format(self.DOP_rate)]) +
                ')')

    def perform_leg(self, ship, leg):
        days_taken = leg.distance / (ship.speed * 24)
        self.voyage_days += days_taken
        if leg.on_hire:
            self.income += days_taken * self.APS_rate
        else:
            self.income -= days_taken * ship.consumption * ship.bunker_price
        return self

    def perform_bb(self):
        self.income += self.BB
        return self

    def perform_port(self, port):
        self.voyage_days += port.days
        if port.on_hire:
            self.income += port.days * self.APS_rate
        return self

    def calculate(self):
        self.DOP_rate = self.income / self.voyage_days
        return self


class Leg(object):
    def __init__(self, distance=1000, on_hire=True):
        self.distance = distance
        self.on_hire = on_hire


class Port(object):
    def __init__(self, days=3, on_hire=True):
        self.days = days
        self.on_hire = on_hire


class Ship(object):
    def __init__(self, speed=12, consumption=24, bunker_price=400):
        self.speed = speed
        self.consumption = consumption
        self.bunker_price = bunker_price


v = Voyage()
l1 = Leg(1000, False)
l2 = Leg(10000)
s = Ship()
p1 = Port(3)
p2 = Port(5)


print(v)
v.perform_leg(s, l1)
print(v)
v.perform_bb()
print(v)
v.perform_port(p1)
print(v)
v.perform_leg(s, l2)
print(v)
v.perform_port(p2)
print(v)
v.calculate()
print(v)
print('\n'*3)
print('DOP equivalent is:', v.DOP_rate)

