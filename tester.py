'''Simple test script

'''
import sys
from core.graph import Graph, Node

def main(args):

    nn = [Node(), Node(), Node(), Node()]
    xx = Graph()
    xx.build_complete_nondirectional(nn)
    print (xx)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
