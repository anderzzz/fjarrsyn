'''Simple test script

'''
import sys
import argparse
import numpy.random
import logging
import pickle

from infection.propagator import BeakerPropagator
from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment
from core.naturallaw import RandomMutator, ObjectForce 
from simulator.runner import FiniteSystemRunner

SCAFFOLD_INIT_A = {'surface_profile' : 'aaaaaaaa',
                   'molecule_A' : 0.0,
                   'molecule_B' : 0.0,
                   'molecule_C' : 0.0,
                   'poison' : 0.0,
                   'poison_vacuole' : 0.0,
                   'poison_vacuole_max' : 2.0,
                   'generosity' : 0.5,
                   'attacker' : 0.5,
                   'generosity_mag' : 0.5,
                   'attack_mag' : 0.5,
                   'vulnerability_to_poison' : 2.0,
                   'trusting' : 0.5,
                   'trusting_mag' : 0.5,
                   'split_thrs' : 0.9}

SCAFFOLD_INIT_W = {'surface_profile' : 'wwwwwwww',
                   'molecule_A' : 0.0,
                   'molecule_B' : 0.0,
                   'molecule_C' : 0.0,
                   'poison' : 0.0,
                   'poison_vacuole' : 0.0,
                   'poison_vacuole_max' : 2.0,
                   'generosity' : 0.5,
                   'attacker' : 0.5,
                   'generosity_mag' : 0.5,
                   'attack_mag' : 0.5,
                   'vulnerability_to_poison' : 2.0,
                   'trusting' : 0.5,
                   'trusting_mag' : 0.5,
                   'split_thrs' : 0.9}

def parse_(argv):

    parser = argparse.ArgumentParser(description='Script to simulate a ' + \
        'beaker of bacteria that divide to reproduce and which optionally ' + \
        'can evolve strategies to be more fit. There can be two distinct ' + \
        'seed populations, which are differentiated on a superficial feature.')

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
    group_start.add_argument('--coord-init',
                             dest='coord_init',
                             default='random',
                             help='How to initialize the placement of bacterial ' + \
                                  'agents in the grid')

    group_force = parser.add_argument_group('Object and Random Force Parameters')
    group_force.add_argument('--env-equilibrate-frac',
                             dest='env_loss',
                             default='0.5',
                             help='Fraction adjustment towards environmental ' + \
                                  'equilibrium per time-step (0.0-1.0)')
    group_force.add_argument('--mutate-type-std',
                             dest='mutate_type_std',
                             default='0.1',
                             help='Standard deviation of Wiener process that ' + \
                                  'encode random mutation drift of agent type')
    group_force.add_argument('--mutate-type-chance',
                             dest='mutate_type_chance',
                             default='0.05',
                             help='Chance of agent type mutation drift')
    group_force.add_argument('--mutate-resource-increment',
                             dest='mutate_increment',
                             default='1.0',
                             help='Increment of random internal resource molecule')
    group_force.add_argument('--mutate-resource-chance',
                             dest='mutate_resource_chance',
                             default='0.05',
                             help='Chance of agent resource increment')
    group_force.add_argument('--mutate-surface',
                             dest='mutate_surface',
                             default='0.01',
                             help='Chance of mutating surface of agent')

    group_assembly_dynamics = parser.add_argument_group('Assembly Dynamics Parameters')
    group_assembly_dynamics.add_argument('--newborn-compete',
                                         dest='newborn_compete',
                                         default='0.25',
                                         help='In event no empty node to grow ' + \
                                         'into, how likely the newly born ' + \
                                         'wins over incumbent')

    group_simulation = parser.add_argument_group('Simulation Parameters')
    group_simulation.add_argument('--n-steps',
                                  dest='n_steps',
                                  help='Number of steps in the simulation')
    group_simulation.add_argument('--n-sample',
                                  dest='n_sample',
                                  help='Number of simulation steps between ' + \
                                       'sampling of state and graph')
    group_simulation.add_argument('--sample-file-name',
                                  dest='sample_file_name',
                                  default='sample.csv',
                                  help='File name of state sampling')
    group_simulation.add_argument('--graph-file-name',
                                  dest='graph_file_name',
                                  default='graph',
                                  help='Body of file name of graph sampling')
    group_simulation.add_argument('--sample-features',
                                  dest='sample_features',
                                  default='',
                                  help='Comma-separated list of agent ' + \
                                       'features to sample')
    group_simulation.add_argument('--seed',
                                  dest='seed',
                                  default='791204',
                                  help='Random seed')

    group_disk = parser.add_argument_group('Agent System Pickle Save/Load')
    group_disk.add_argument('--pickle-save',
                            dest='pickle_save',
                            default=None,
                            help='Path to output pickle file of the agent ' + \
                                 'system at the end of the simulation')
    group_disk.add_argument('--pickle-load',
                            dest='pickle_load',
                            default=None,
                            help='Path to input pickle file of the agent ' + \
                                 'system to start the simulation with. ' + \
                                 'Overrides all other system definitions')

    parser.add_argument('--debug',
                        default=False,
                        dest='debug_runner',
                        action='store_true',
                        help='Flag to activate debugger printing')

    args = parser.parse_args(argv)

    n_bacteria_1 = int(args.n_bacteria_1)
    n_bacteria_2 = int(args.n_bacteria_2)
    cell_length = int(args.cell_length)
    equilibrium_env = float(args.equilibrium)
    coord_init = args.coord_init

    env_loss = float(args.env_loss)
    mutate_type_std = float(args.mutate_type_std)
    mutate_type_chance = float(args.mutate_type_chance)
    mutate_increment = float(args.mutate_increment)
    mutate_resource_chance = float(args.mutate_resource_chance)
    mutate_surface = float(args.mutate_surface)

    newborn_compete = float(args.newborn_compete)

    n_steps = int(args.n_steps)
    n_sample = int(args.n_sample)
    sample_file_name = args.sample_file_name
    graph_file_name = args.graph_file_name
    sample_features = args.sample_features.split(',')
    seed = int(args.seed)

    pickle_save = args.pickle_save
    pickle_load = args.pickle_load

    debug_runner = args.debug_runner

    return n_bacteria_1, n_bacteria_2, cell_length, equilibrium_env, \
           coord_init, env_loss, \
           mutate_type_std, mutate_type_chance, mutate_increment, \
           mutate_resource_chance, mutate_surface, newborn_compete, n_steps, \
           n_sample, sample_file_name, graph_file_name, sample_features, \
           seed, pickle_save, pickle_load, debug_runner

def main(args):

    #
    # Parse the command-line
    #
    n_bacteria_1, n_bacteria_2, cell_length, equilibrium_env, coord_init, \
        env_loss, mutate_type_std, mutate_type_chance, mutate_increment, \
        mutate_resource_chance, mutate_surface, newborn_compete, n_steps, \
        n_sample, sample_file_name, graph_file_name, sample_features, \
        seed, pickle_save, pickle_load, debug_runner = parse_(args)

    #
    # Rudimentary initializations
    #
    numpy.random.seed(seed)
    if debug_runner:
        logging.basicConfig(filename='logger.log', filemode='w', 
                            level=logging.DEBUG)

    #
    # Set up the agent management system
    #
    if pickle_load is None:
        bacterial_agents = []
        for k_bacteria in range(n_bacteria_1):
            bacterial_agents.append(Bacteria('bacteria_A_%s' %(str(k_bacteria)),
                                             SCAFFOLD_INIT_A))

        for k_bacteria in range(n_bacteria_2):
            bacterial_agents.append(Bacteria('bacteria_W_%s' %(str(k_bacteria)),
                                             SCAFFOLD_INIT_W))

        SCAFFOLD_ENV = {'molecule_A' : equilibrium_env,
                        'molecule_B' : equilibrium_env,
                        'molecule_C' : equilibrium_env,
                        'poison' : 0.0}
        extracellular = ExtracellEnvironment('extracellular_fluid', SCAFFOLD_ENV)

        coords = []
        if coord_init == 'random':
            for k_agent in range(len(bacterial_agents)):
                tup = (np.random.randint(cell_length), \
                       np.random.randint(cell_length), \
                       np.random.randint(cell_length))
                coords.append(tup)

        elif coord_init == 'diagonal':
            coords.append((0,0,0))
            coords.append((cell_length - 1, cell_length - 1, cell_length - 1))

        elif coord_init == 'corners':
            coords.append((0,0,0))
            coords.append((0,0,cell_length - 1))
            coords.append((0,cell_length - 1,0))
            coords.append((cell_length - 1,0,0))
            coords.append((cell_length - 1, cell_length - 1, cell_length - 1))
            coords.append((cell_length - 1, cell_length -1, 0))
            coords.append((cell_length - 1, 0,cell_length - 1))
            coords.append((0, cell_length - 1, cell_length - 1))

        print (coords)
        cell_space = Goo('cell_space', bacterial_agents, extracellular,
                         cell_length, newborn_compete, coords)

    else:
        with open(pickle_load, 'rb') as fin:
            cell_space = pickle.load(fin)

    #
    # Set up the object forces to apply from above onto the agent management
    # system, random and deterministic
    #
    force = RandomMutator('bacterial_drift')
    force.set_force_func('generosity', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std})
    force.set_force_func('attacker', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std})
    force.set_force_func('trusting', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std})
    force.set_force_func('generosity_mag', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('attack_mag', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('trusting_mag', 
                         'force_func_wiener_bounded', mutate_type_chance,
                         {'std' : mutate_type_std, 'lower_bound' : 0.0, 'upper_bound' : 1.0})
    force.set_force_func('molecule_A', 
                         'force_func_delta', mutate_resource_chance,
                         {'increment' : mutate_increment})
    force.set_force_func('molecule_B', 
                         'force_func_delta', mutate_resource_chance,
                         {'increment' : mutate_increment})
    force.set_force_func('molecule_C', 
                         'force_func_delta', mutate_resource_chance,
                         {'increment' : mutate_increment})
    force.set_force_func('surface_profile', 
                         'force_func_flip_one_char', mutate_surface,
                         {'alphabet' : ['a', 'w']})

    age_force = ObjectForce('environmental_time')
    age_force.set_force_func('molecule_A', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('molecule_B', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('molecule_C', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_force_func('poison', 'force_func_exponential_convergence',
                             {'loss' : env_loss, 'target' : 0.0})

    propagator = BeakerPropagator(force, age_force)

    #
    # Define the simulator
    #
    simulator = FiniteSystemRunner(n_steps, n_sample_steps=n_sample,
                                   sample_file_name=sample_file_name,
                                   imprints_sample=sample_features,
                                   system_propagator=propagator,
                                   graph_file_name_body=graph_file_name,
                                   graph_file_format='csv')

    #
    # Simulate the propagation of the agent management system
    #
    simulator(cell_space)

    #
    # Optional save of agent manageent system
    #
    if not pickle_save is None:
        with open(pickle_save, 'wb') as fout:
            pickle.dump(cell_space, fout)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
