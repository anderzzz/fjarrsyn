'''Simple test script

'''
import sys
from core.graph import Graph, Node
from core.agent import Agent

def main(args):

    person1 = Agent()
    person1.set_state({'A' : 50, 'B' : 30, 'C' : 10, 'D' : 10})
    person2 = Agent()
    person2.set_state({'A' : 40, 'B' : 30, 'C' : 10, 'D' : 20})
    person3 = Agent()
    person3.set_state({'A' : 20, 'B' : 0, 'C' : 40, 'D' : 40})

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
