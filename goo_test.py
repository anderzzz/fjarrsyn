'''Simple test script

'''
import sys
import argparse
import random

from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment

def parse_(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--n-bacteria-1',
                         dest='n_bacteria_1',
                         default='5',
                         help='Number of initial bacteria of type 1 in cell space')
    parser.add_argument('--n-bacteria-2',
                         dest='n_bacteria_2',
                         default='5',
                         help='Number of initial bacteria of type 2 in cell space')
    parser.add_argument('--cell-length',
                        dest='cell_length',
                        default='10',
                        help='Number of grid points along any one dimension ' + \
                             'of the cubic grid of the cell space')

    args = parser.parse_args(argv)

    n_bacteria_1 = int(args.n_bacteria_1)
    n_bacteria_2 = int(args.n_bacteria_2)
    cell_length = int(args.cell_length)

    return n_bacteria_1, n_bacteria_2, cell_length

def main(args):

    n_bacteria_1, n_bacteria_2, cell_length = parse_(args)

    bacterial_agents = []
    for k_bacteria in range(n_bacteria_1):
        bacterial_agents.append(Bacteria('bacteria_1_%s' %(str(k_bacteria)), 'aaaaa'))
    for k_bacteria in range(n_bacteria_2):
        bacterial_agents.append(Bacteria('bacteria_2_%s' %(str(k_bacteria)), 'wwwww'))

    extracellular_env_agent = ExtracellEnvironment('extracell',
                              {'nutrients':0.2, 'poison_A':0.0, 'poison_B':0.0})

    cell_space = Goo('cell_space', 10, bacterial_agents, extracellular_env_agent)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
