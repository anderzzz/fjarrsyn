'''Simple test script

'''
import sys
import argparse
import random

from infection.goo import Goo

def parse_(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--n-ants',
                         dest='n_ants',
                         default='10',
                         help='Number of ants in colony')
    parser.add_argument('--rebel-type',
                         dest='rebel_type',
                         default='single_value',
                         help='Type of rebel distribution')
    parser.add_argument('--rebel-index',
                         dest='rebel_index',
                         default='0.1',
                         help='Rebel index, meaning set by --rebel-type')
    parser.add_argument('--n-opinions',
                         dest='n_opinions',
                         default='2',
                         help='Number of distinct opinions')
    parser.add_argument('--n-steps-per-ant',
                        dest='n_step_factor',
                        default='1',
                        help='Average number of steps per ant in simulation')

    args = parser.parse_args(argv)

    n_ants = int(args.n_ants)
    rebel_index = float(args.rebel_index)
    n_opinions = int(args.n_opinions)
    n_step_factor = int(args.n_step_factor)

    return n_ants, args.rebel_type, rebel_index, n_opinions, n_step_factor

def main(args):

    n_ants, rebel_type, rebel_index, n_opinions, n_step_factor = parse_(args)

    Goo('hello', [])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
