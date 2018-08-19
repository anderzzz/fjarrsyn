'''Simple test script

'''
import sys
import argparse
import numpy as np
import numpy.random
import pandas as pd
import logging
import pickle

from infection.propagator import BeakerPropagator
from infection.goo import Goo
from infection.bacteria import Bacteria, ExtracellEnvironment
from core.naturallaw import ObjectMapCollection 
from simulator.runner import FiniteSystemRunner

def parse_(argv):

    parser = argparse.ArgumentParser(description='Script to simulate a ' + \
        'beaker of bacteria that divide to reproduce and which optionally ' + \
        'can evolve strategies to be more fit. There can be two distinct ' + \
        'seed populations, which are differentiated on a superficial feature.')

    group_start = parser.add_argument_group('Initial System Setup')
    group_start.add_argument('--bacteria-init-file',
                             dest='bacteria_init_file',
                             required=True,
                             help='Path to file containing initial values ' + \
                                  'keyed on bacterial type')
    group_start.add_argument('--types-to-simulate',
                             dest='types_to_simulate',
                             required=True,
                             help='Comma-separated string of bacterial ' + \
                                  'types to include in simulation')
    group_start.add_argument('--n-bacteria',
                             dest='n_bacteria',
                             default='1',
                             help='Comma-separated string of number of ' + \
                                  'each bacterial type to initialize')
    group_start.add_argument('--cell-length',
                             dest='cell_length',
                             default='10',
                             help='Number of grid points along any one dimension ' + \
                                  'of the cubic grid of the cell space')
    group_start.add_argument('--periodic-grid',
                             dest='periodic',
                             default=False,
                             action='store_true',
                             help='If flag give, the grid in which agents ' + \
                                  'operate is periodic')
    group_start.add_argument('--equilibrium-A-B-C',
                             dest='equilibrium',
                             default='0.0',
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
    group_force.add_argument('--mutate-phenotype-midpoint',
                             dest='mutate_phenotype_midpoint',
                             default='0.1',
                             help='Standard deviation of Wiener process that ' + \
                                  'encode random mutation drift of midpoint')
    group_force.add_argument('--mutate-phenotype-magnitude',
                             dest='mutate_phenotype_magnitude',
                             default='0.1',
                             help='Standard deviation of Wiener process that ' + \
                                  'encode random mutation drift of magnitude')
    group_force.add_argument('--mutate-generosity-chance',
                             dest='mutate_generosity_chance',
                             default='0.0',
                             help='Chance of agent generosity phenotype mutation drift')
    group_force.add_argument('--mutate-trust-chance',
                             dest='mutate_trust_chance',
                             default='0.0',
                             help='Chance of agent trust phenotype mutation drift')
    group_force.add_argument('--mutate-attack-chance',
                             dest='mutate_attack_chance',
                             default='0.0',
                             help='Chance of agent attack phenotype mutation drift')
    group_force.add_argument('--mutate-resource-increment',
                             dest='mutate_increment',
                             default='1.0',
                             help='Increment of random internal resource molecule')
    group_force.add_argument('--mutate-resource-chance',
                             dest='mutate_resource_chance',
                             default='0.0',
                             help='Chance of agent resource increment')
    group_force.add_argument('--mutate-poison-increment',
                             dest='poison_increment',
                             default='5.0',
                             help='Increment of internal poison')
    group_force.add_argument('--mutate-poison-chance',
                             dest='mutate_poison_chance',
                             default='0.0',
                             help='Chance of agent poison leading to death')

    group_assembly_dynamics = parser.add_argument_group('Assembly Dynamics Parameters')
    group_assembly_dynamics.add_argument('--newborn-compete',
                                         dest='newborn_compete',
                                         default='0.20',
                                         help='In event no empty node to grow ' + \
                                         'into, how likely the newly born ' + \
                                         'wins over incumbent')

    group_simulation = parser.add_argument_group('Simulation Parameters')
    group_simulation.add_argument('--n-steps',
                                  dest='n_steps',
                                  required=True,
                                  help='Number of steps in the simulation')
    group_simulation.add_argument('--n-sample',
                                  dest='n_sample',
                                  required=True,
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

    bacteria_init_file = args.bacteria_init_file
    types_to_simulate = args.types_to_simulate.split(',')
    n_bacteria = args.n_bacteria.split(',')
    ntypes = {} 
    for n_bact, type_bact in zip(n_bacteria, types_to_simulate):
        ntypes[type_bact] = int(n_bact)
    cell_length = int(args.cell_length)
    periodic = args.periodic
    equilibrium_env = float(args.equilibrium)
    coord_init = args.coord_init

    env_loss = float(args.env_loss)
    mutate_phenotype_midpoint = float(args.mutate_phenotype_midpoint)
    mutate_phenotype_magnitude = float(args.mutate_phenotype_magnitude)
    mutate_generosity_chance = float(args.mutate_generosity_chance)
    mutate_trust_chance = float(args.mutate_trust_chance)
    mutate_attack_chance = float(args.mutate_attack_chance)
    mutate_increment = float(args.mutate_increment)
    mutate_resource_chance = float(args.mutate_resource_chance)
    poison_increment = float(args.poison_increment)
    mutate_poison_chance = float(args.mutate_poison_chance)

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

    return bacteria_init_file, ntypes, cell_length, periodic, \
           equilibrium_env, \
           coord_init, env_loss, \
           mutate_phenotype_midpoint, mutate_phenotype_magnitude, \
           mutate_generosity_chance, \
           mutate_trust_chance, mutate_attack_chance, \
           mutate_increment, mutate_resource_chance, \
           poison_increment, mutate_poison_chance, \
           newborn_compete, \
           n_steps, n_sample, sample_file_name, graph_file_name, \
           sample_features, seed, pickle_save, pickle_load, \
           debug_runner

def main(args):

    #
    # Parse the command-line
    #
    bacteria_init_file, ntypes, cell_length, periodic, \
        equilibrium_env, \
        coord_init, env_loss, \
        mutate_phenotype_midpoint, mutate_phenotype_magnitude, \
        mutate_generosity_chance, \
        mutate_trust_chance, mutate_attack_chance, \
        mutate_increment, mutate_resource_chance, \
        poison_increment, mutate_poison_chance, \
        newborn_compete, \
        n_steps, n_sample, sample_file_name, graph_file_name, \
        sample_features, seed, pickle_save, pickle_load, \
        debug_runner = parse_(args)

    #
    # Rudimentary initializations
    #
    numpy.random.seed(seed)
    if debug_runner:
        logging.basicConfig(filename='logger.log', filemode='w', 
                            level=logging.DEBUG)

    #
    # Set up the agent management system. If a pickle file is available use it,
    # if not initialize a system according to specification
    #
    if pickle_load is None:

        with open(bacteria_init_file) as fin:
            df = pd.read_csv(fin)

        bacterial_agents = []
        for bact_type, n_bact in ntypes.items():
            df_type = df.loc[df['bacteria_name'] == bact_type]
            df_data = df_type[['scaffold_name', 'value']]

            scaffold_init = {}
            for row_id, datum in df_data.iterrows():
                key = datum['scaffold_name']
                if key == 'share_generally':
                    if datum['value'] == 'True':
                        value = True
                    elif datum['value'] == 'False':
                        value = False
                    else:
                        raise RuntimeError('Unknown setting for ' + \
                                'share_generally: %s' %(datum['value']))
                elif key == 'profile_length':
                    value = int(datum['value'])
                else:
                    value = float(datum['value'])

                scaffold_init[key] = value

            if len(scaffold_init) == 0:
                raise RuntimeError('Scaffold for type %s empty. ' %(bact_type) + \
                                   'Possible key error on command-line')

            for k_bacteria in range(n_bact):
                bacterial_agents.append(Bacteria('bacteria', scaffold_init))

        SCAFFOLD_ENV = {'molecule_A' : equilibrium_env,
                        'molecule_B' : equilibrium_env,
                        'molecule_C' : equilibrium_env,
                        'poison' : 0.0}
        extracellular = ExtracellEnvironment('extracellular_fluid', SCAFFOLD_ENV)

        coords = []
        if coord_init == 'random':
            while len(set(coords)) < len(bacterial_agents):
                tup = (np.random.randint(cell_length), \
                       np.random.randint(cell_length), \
                       np.random.randint(cell_length))
                coords.append(tup)
            coords = list(set(coords))

        elif coord_init == 'diagonal':
            coords.append((0,0,0))
            coords.append((cell_length - 1, cell_length - 1, cell_length - 1))

        elif coord_init == 'corners':
            coords.append((0,0,0))
            coords.append((0, 0, cell_length - 1))
            coords.append((0, cell_length - 1, 0))
            coords.append((0, cell_length - 1, cell_length - 1))
            coords.append((cell_length - 1, 0, 0))
            coords.append((cell_length - 1, cell_length - 1, cell_length - 1))
            coords.append((cell_length - 1, cell_length -1, 0))
            coords.append((cell_length - 1, 0, cell_length - 1))

        cell_space = Goo('cell_space', bacterial_agents, extracellular,
                         cell_length, periodic, newborn_compete, coords)

    else:
        with open(pickle_load, 'rb') as fin:
            cell_space = pickle.load(fin)

    #
    # Set up the object forces to apply from above onto the agent management
    # system, random and deterministic
    #
    force = ObjectMapCollection(['generosity', 'attacker', \
                                'trusting', 'generosity_mag', 'attack_mag', \
                                'trusting_mag', 'molecule_A', 'molecule_B', \
                                'molecule_C', 'poison'], 
                                standard_funcs=True, stochastic_decoration=True)
    force.set_map_func('generosity', 
                       'force_func_wiener_bounded', 
                       {'std' : mutate_phenotype_midpoint}, 
                       apply_p=mutate_generosity_chance)
    force.set_map_func('attacker', 
                       'force_func_wiener_bounded', 
                       {'std' : mutate_phenotype_midpoint},
                       apply_p=mutate_attack_chance)
    force.set_map_func('trusting', 
                       'force_func_wiener_bounded', 
                       {'std' : mutate_phenotype_midpoint},
                       apply_p=mutate_trust_chance)
    force.set_map_func('generosity_mag', 
                       'force_func_wiener_bounded',
                       {'std' : mutate_phenotype_magnitude, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
                       apply_p=mutate_generosity_chance)
    force.set_map_func('attack_mag', 
                       'force_func_wiener_bounded',
                       {'std' : mutate_phenotype_magnitude, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
                       apply_p=mutate_attack_chance)
    force.set_map_func('trusting_mag', 
                       'force_func_wiener_bounded',
                       {'std' : mutate_phenotype_magnitude, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
                       apply_p=mutate_trust_chance)
    force.set_map_func('molecule_A', 
                       'force_func_delta',
                       {'increment' : mutate_increment},
                       apply_p=mutate_resource_chance)
    force.set_map_func('molecule_B', 
                       'force_func_delta',
                       {'increment' : mutate_increment},
                       apply_p=mutate_resource_chance)
    force.set_map_func('molecule_C', 
                       'force_func_delta',
                       {'increment' : mutate_increment},
                       apply_p=mutate_resource_chance)
    force.set_map_func('poison', 
                       'force_func_delta',
                       {'increment' : poison_increment},
                       apply_p=mutate_poison_chance)

    age_force = ObjectMapCollection(['molecule_A', 'molecule_B', 'molecule_C', 'poison'], 
                                    standard_funcs=True)
    age_force.set_map_func('molecule_A', 
                           'force_func_exponential_convergence',
                           {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_map_func('molecule_B', 
                           'force_func_exponential_convergence',
                           {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_map_func('molecule_C', 
                           'force_func_exponential_convergence',
                           {'loss' : env_loss, 'target' : equilibrium_env})
    age_force.set_map_func('poison', 
                           'force_func_exponential_convergence',
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
