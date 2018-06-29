'''Simple test script

'''
import sys
import argparse
import random

from socialmimicry.setup import AntColony, Ant
from core.graph import Graph

def parse_(argv):

    parser = argparse.ArgumentParser()
    parser.add_arguments('--n-ants',
                         dest='n_ants',
                         default='10',
                         help='Number of ants in colony')
    parser.add_arguments('--rebel-type',
                         dest='rebel_type',
                         default='single_value',
                         help='Type of rebel distribution')
    parser.add_arguments('--rebel-index',
                         dest='rebel_index',
                         default='0.1',
                         help='Rebel index, meaning set by --rebel-type')
    parser.add_arguments('--n-opinions',
                         dest='n_opinions',
                         default='2',
                         help='Number of distinct opinions')

    args = parser.parse_args(argv)

    n_ants = int(args.n_ants)
    rebel_index = float(args.rebel_index)
    n_opinions = int(args.n_opinions)

    return n_ants, rebel_type, rebel_index, n_opinions

def main(args):

    n_ants, rebel_type, rebel_index, n_opinions = parse_(args)

    ants = []
    for k_ant in range(n_ants):
        k_opinion = random.randint(0, n_opinions - 1)
        if rebel_type == 'single_value':
            ant = Ant('dummy', rebel_index, k_opinion)
        else:
            raise RuntimeError('Unknown rebel type: %s' %(rebel_type))

        ants.append(ant)

    colony = AntColony('the_pile', ants)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
