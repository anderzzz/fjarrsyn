'''Simple test script

'''
import sys
from auction.setup import Auction, AuctionParticipant 

def main(args):

    #REWRITE THIS STUFF
    person1 = AuctionParticipant('Steve',
                  items_on_hand={'Ferrari':10}, 
                  true_valuation={'buy_Ferrari':101.0, 'sell_Ferrari':111.0})
    person2 = AuctionParticipant('Sumo',
                  true_valuation={'buy_Ferrari':102.0, 'buy_Volkswagen':48.0})
    person3 = AuctionParticipant('Skurt',
                  true_valuation={'buy_Ferrari':100.0, 'buy_Volkswagen':49.0})
    person4 = AuctionParticipant('Bosse',
                  items_on_hand={'Ferrari':1, 'Volkswagen':15},
                  true_valuation={'sell_Ferrari':105.0, 'sell_Volkswagen':44.0})
    person5 = AuctionParticipant('Brutus',
                  items_on_hand={'Volkswagen':4},
                  true_valuation={'sell_Volkswagen':45.0, 'buy_Volkswagen':42.0})

    agents = [person1, person2, person3, person4, person5]

    auction = Auction('car_auction', agents)
    auction()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
