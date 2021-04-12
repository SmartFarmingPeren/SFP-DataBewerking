class Auto():
    def __init__(self, Wielen, Passgiers, Multiplier):
        self.wielen = Wielen
        self.mensen = Passgiers
        self.multiplier = Multiplier

    def meerWielen(self):
        self.wielen += self.multiplier
        self.mensen += self.multiplier

    def pasWielenAan(self, wielen):
        self.wielen = wielen

def main():
    auto = Auto(4, 2, 900)
    print(auto.wielen)
    auto.meerWielen()
    print(auto.wielen)
    auto.pasWielenAan(2000)


    auto2 = Auto(4, 2, 450)
    print(auto2.wielen)
    auto2.meerWielen()
    print(auto2.wielen)

if __name__ == '__main__':
    main()
