'''Simple test script

'''
import sys
import argparse
import random

from socialmimicry.ant import Ant
from socialmimicry.antcolony import AntColony, AntColonySummarizer
from core.graph import Graph

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

    ants = []
    for k_ant in range(n_ants):
        k_opinion = random.randint(0, n_opinions - 1)
        if rebel_type == 'single_value':
            ant = Ant('dummy', rebel_index, k_opinion, range(n_opinions))
        else:
            raise RuntimeError('Unknown rebel type: %s' %(rebel_type))

        ants.append(ant)

    colony = AntColony('the_pile', ants)

    n_iterations = n_ants * n_step_factor
    k_iteration = 0
    while k_iteration < n_iterations:
        agent_selected = random.choice(colony)
        agent_selected()

        k_iteration += 1

    summy = AntColonySummarizer(colony)
    out = summy.natures()
    print (out)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
