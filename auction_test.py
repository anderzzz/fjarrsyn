'''Simple test script

'''
import sys
from auction.setup import Auction, BuyerAgent, SellerAgent

def main(args):

    person1 = BuyerAgent('Sture')
    person2 = BuyerAgent('Sverker')
    person3 = BuyerAgent('Skurt')
    person4 = SellerAgent('Bjorn')
    person5 = SellerAgent('Borje')

    person1.product_value({'Ferrari':100.0, 'Volkswagen':40.0})
    person2.product_value({'Ferrari':102.0, 'Volkswagen':30.0})
    person3.product_value({'Ferrari':107.0, 'Volkswagen':41.0})
    person4.product_value({'Ferrari':101.0})
    person5.product_value({'Volkswagen':22.0})

    agents = [person1, person2, person3, person4, person5]

    auction = Auction(agents)
    auction()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
