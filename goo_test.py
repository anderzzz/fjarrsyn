'''Simple test script

'''
import sys
import argparse
import random

from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment
from core.naturallaw import ObjectForce

def parse_(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--n-bacteria-1',
                         dest='n_bacteria_1',
                         default='4',
                         help='Number of initial bacteria of type 1 in cell space')
    parser.add_argument('--n-bacteria-2',
                         dest='n_bacteria_2',
                         default='4',
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
        bacterial_agents.append(Bacteria('bacteria_1_%s' %(str(k_bacteria)),
                                         'aaaaa', [1.0, 1.0, 1.0, 0.0, 0.0]))
    for k_bacteria in range(n_bacteria_2):
        bacterial_agents.append(Bacteria('bacteria_2_%s' %(str(k_bacteria)),
                                         'wwwww', [0.0, 1.0, 0.0, 0.0, 0.0]))

#    force_ = ObjectForce('bacterial_drift')
#    force_.set_force_func('generosity', 'wiener_bounded', 
#                          {'std' : 0.1, 'lower_bound' : 0.0}, 0.1)
#    force_.set_force_func('attacker', 'wiener_bounded', 
#                          {'std' : 0.1, 'lower_bound' : 0.0}, 0.1)
#    force_.set_force_func('generosity_mag', 'wiener_bounded', 
#                          {'std' : 0.1, 'lower_bound' : 0.0}, 0.1)
#    force_.set_force_func('attack_mag', 'wiener_bounded', 
#                          {'std' : 0.1, 'lower_bound' : 0.0}, 0.1)
#    force_.set_force_func('molecule_A', 'stochastic_addition',
#                          {'increment' : 1.0, 'thrs_prob' : 0.2}, 1.0)
#    force_.set_force_func('molecule_B', 'stochastic_addition',
#                          {'increment' : 1.0, 'thrs_prob' : 0.2}, 1.0)
#    force_.set_force_func('molecule_C', 'stochastic_addition',
#                          {'increment' : 1.0, 'thrs_prob' : 0.2}, 1.0)

    extracellular = ExtracellEnvironment('extracellular_fluid',
                              {'molecule_A' : 0.1, 'molecule_B' : 0.1,
                               'molecule_C' : 0.1, 'poison' : 0.0})

    cell_space = Goo('cell_space', 2, bacterial_agents, extracellular)

    for bacteria in cell_space.shuffle_iteritems():
        print ('PING')
        print ('PING')
        print ('PING', bacteria.agent_id_system)
        print (cell_space.agents_graph[bacteria.agent_id_system])
        print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
        print (bacteria.scaffold)
        bacteria()
        print (bacteria.scaffold)
        print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
        print ('ZZZZZ', [n.agent_content for n in cell_space.agents_graph.nodes])

    for bacteria in cell_space.shuffle_iteritems():
        print ('PING')
        print ('PING')
        print ('PING', bacteria.agent_id_system)
        print (cell_space.agents_graph[bacteria.agent_id_system])
        print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
        print (bacteria.scaffold)
        bacteria()
        print (bacteria.scaffold)
        print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
        print ('ZZZZZ', [n.agent_content for n in cell_space.agents_graph.nodes])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
