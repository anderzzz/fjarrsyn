'''Simple test script

'''
import sys
import argparse
import random

from infection.propagator import BeakerPropagator
from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment
from core.naturallaw import RandomMutator, ObjectForce 
from simulator.runner import FiniteSystemRunner

SCAFFOLD_INIT_A = {'surface_profile' : 'aaaaa',
                   'molecule_A' : 0.0,
                   'molecule_B' : 0.0,
                   'molecule_C' : 0.0,
                   'poison' : 0.0,
                   'poison_vacuole' : 0.0,
                   'poison_vacuole_max' : 0.2,
                   'generosity' : 0.5,
                   'attacker' : 0.5,
                   'generosity_mag' : 0.5,
                   'attack_mag' : 0.5,
                   'vulnerability_to_poison' : 2.0,
                   'trusting' : 0.5,
                   'trusting_mag' : 0.5,
                   'split_thrs' : 0.9}

SCAFFOLD_INIT_W = {'surface_profile' : 'wwwww',
                   'molecule_A' : 0.0,
                   'molecule_B' : 0.0,
                   'molecule_C' : 0.0,
                   'poison' : 0.0,
                   'poison_vacuole' : 0.0,
                   'poison_vacuole_max' : 0.2,
                   'generosity' : 0.5,
                   'attacker' : 0.5,
                   'generosity_mag' : 0.5,
                   'attack_mag' : 0.5,
                   'vulnerability_to_poison' : 2.0,
                   'trusting' : 0.5,
                   'trusting_mag' : 0.5,
                   'split_thrs' : 0.9}

def parse_(argv):

    parser = argparse.ArgumentParser()

    group_start = parser.add_argument_group('Initial System Setup')
    group_start.add_argument('--n-bacteria-1',
                             dest='n_bacteria_1',
                             default='4',
                             help='Number of initial bacteria of type 1 in cell space')
    group_start.add_argument('--n-bacteria-2',
                             dest='n_bacteria_2',
                             default='4',
                             help='Number of initial bacteria of type 2 in cell space')
    group_start.add_argument('--cell-length',
                             dest='cell_length',
                             default='10',
                             help='Number of grid points along any one dimension ' + \
                                  'of the cubic grid of the cell space')
    group_start.add_argument('--equilibrium-A-B-C',
                             dest='equilibrium',
                             default='0.1',
                             help='Equilibrium content of molecules A, B and C ' + \
                                  'in environment')

    group_force = parser.add_argument_group('Object and Random Force Parameters')
    group_force.add_argument('--env-equilibrate-frac',
                             dest='env_loss',
                             default='0.5',
                             help='Fraction adjustment towards environmental ' + \
                                  'equilibrium per time-step (0.0-1.0)')

    parser.add_argument('--newborn-compete',
                        dest='newborn_compete',
                        default='0.25',
                        help='In case no empty spot available, how likely ' + \
                             'a newborn bacteria can push away established one')

    args = parser.parse_args(argv)

    n_bacteria_1 = int(args.n_bacteria_1)
    n_bacteria_2 = int(args.n_bacteria_2)
    cell_length = int(args.cell_length)
    equilibrium_env = float(args.equilibrium)

    env_loss = float(args.env_loss)

    newborn_compete = float(args.newborn_compete)

    return n_bacteria_1, n_bacteria_2, cell_length, equilibrium_env, env_loss, newborn_compete

def main(args):

    n_bacteria_1, n_bacteria_2, cell_length, equilibrium_env, \
        env_loss, newborn_compete = parse_(args)

    bacterial_agents = []
    for k_bacteria in range(n_bacteria_1):
        bacterial_agents.append(Bacteria('bacteria_A_%s' %(str(k_bacteria)),
                                         SCAFFOLD_INIT_A))

    for k_bacteria in range(n_bacteria_2):
        bacterial_agents.append(Bacteria('bacteria_W_%s' %(str(k_bacteria)),
                                         SCAFFOLD_INIT_W))

    force = RandomMutator('bacterial_drift')
    force.set_force_func('generosity', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('attacker', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('trusting', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('generosity_mag', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('attack_mag', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('trusting_mag', 'force_func_wiener_bounded', 0.05,
                         {'std' : 0.1, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('molecule_A', 'force_func_delta', 0.05,
                         {'increment' : 1.0})
    force.set_force_func('molecule_B', 'force_func_delta', 0.05,
                         {'increment' : 1.0})
    force.set_force_func('molecule_C', 'force_func_delta', 0.05,
                         {'increment' : 1.0})
    force.set_force_func('surface_profile', 'force_func_flip_one_char', 0.01,
                         {'alphabet' : ['a', 'w']})

    SCAFFOLD_ENV = {'molecule_A' : equilibrium_env,
                    'molecule_B' : equilibrium_env,
                    'molecule_C' : equilibrium_env,
                    'poison' : 0.0}
    extracellular = ExtracellEnvironment('extracellular_fluid', SCAFFOLD_ENV)

    age_force = ObjectForce('environmental_time')
    age_force.set_force_func('molecule_A', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('molecule_B', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('molecule_C', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('poison', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : 0.0})

    cell_space = Goo('cell_space', bacterial_agents, extracellular,
                     cell_length, newborn_compete)

    propagator = BeakerPropagator(force, age_force)
    simulator = FiniteSystemRunner(10000, n_sample_steps=500,
                                   imprints_sample=['scaffold_molecule_A', 'scaffold_trusting'],
                                   system_propagator=propagator,
                                   graph_file_name='graph.csv')
    simulator(cell_space)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
