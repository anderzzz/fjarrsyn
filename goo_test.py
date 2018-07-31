'''Simple test script

'''
import sys
import argparse
import random

from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment
from core.naturallaw import RandomMutator 

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

    force_ = RandomMutator('bacterial_drift')
    force_.set_force_func('generosity', 'force_func_wiener_bounded', 0.1,
                          {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force_.set_force_func('attacker', 'force_func_wiener_bounded', 0.1,
                          {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force_.set_force_func('generosity_mag', 'force_func_wiener_bounded', 0.1,
                          {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force_.set_force_func('attack_mag', 'force_func_wiener_bounded', 0.1,
                          {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force_.set_force_func('molecule_A', 'force_func_delta', 0.05,
                          {'increment' : 1.0})
    force_.set_force_func('molecule_B', 'force_func_delta', 0.05,
                          {'increment' : 1.0})
    force_.set_force_func('molecule_C', 'force_func_delta', 0.05,
                          {'increment' : 1.0})
    force_.set_force_func('surface_profile', 'force_func_flip_one_char', 0.5,
                          {'alphabet' : ['a', 'w']})

    extracellular = ExtracellEnvironment('extracellular_fluid',
                              {'molecule_A' : 0.1, 'molecule_B' : 0.1,
                               'molecule_C' : 0.1, 'poison' : 0.0})

    cell_space = Goo('cell_space', 2, bacterial_agents, extracellular)

    for k in range(100):
        for bacteria, env in cell_space:
            print ('PING')
            print ('PING')
            # WRITE OVER AGENT WHILE RUNNING BUG
            if bacteria is None:
                continue

            print ('PING', bacteria.agent_id_system)
            print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
            print ('Before', bacteria.scaffold)
            bacteria()
            print ('After', bacteria.scaffold)
            print (cell_space.agents_graph[bacteria.agent_id_system].aux_content.molecule_content)
            print ('ZZZZZ', [n.agent_content for n in cell_space.agents_graph.nodes])
            force_(bacteria)
            print ('Mutated', bacteria.scaffold)
    raise Exception('dummy')

    #raise Exception('dummy')
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for bacteria in cell_space.shuffle_agents(4):
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
