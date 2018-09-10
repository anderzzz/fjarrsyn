'''All internal cognition of bacteria agent contained here

'''
import logging
import numpy as np
import numpy.random

from core.helper_funcs import sigmoid, sigmoid_10, linear_step_10
from core.organs import MoulderReturn

class BacteriaBrain(object):
    '''Bla bla

    '''
    def _interpret_selfsimilarity_neighbourhood(self, surface_profile,
                                                neighbour_id):
        '''Interpret how similar a neighbour surface profile is to the current
        agent's own surface profile.

        Parameters
        ----------
        surface_profile : str
            The string of characters defining the surface profile
        neighbour_id : str
            The neighbour id of agent that was sensed and created the buzz

        Returns
        -------
        belief_label 
            Container of labels of the beliefs the interpretation updated or
            created.

        Raises
        ------
        ValueError
            In case there is a surface profile of neighbour, but its length is
            not the same as the profile of current agent

        '''
        if surface_profile is None:
            self.belief['neighbour_same'] = None
            self.belief['neighbour_id'] = None

        else:
            my_profile = self.scaffold['surface_profile']

            if len(my_profile) != len(surface_profile):
                raise ValueError('The surface profile of neighbour ' + \
                                 '(%s) is not same ' %(surface_profile) + \
                                 'size as current profile (%s)' %(my_profile))

            n_same = 0
            for c1, c2 in zip(my_profile, surface_profile):
                if c1 == c2:
                    n_same += 1

            frac_same = float(n_same) / float(len(my_profile))
            self.belief['neighbour_same'] = frac_generosity_gene
            self.belief['neighbour_id'] = neighbour_id

        return ('neighbour_same', 'neighbour_id')

    def _interpret_generosity_neighbourhood(self, surface_profile,
                                            neighbour_id):
        '''Interpret how generous a neighbour is based on signal

        Parameters
        ----------
        surface_profile : str
            The string of characters defining the surface profile
        neighbour_id : str
            The neighbour id of agent that was sensed and created the buzz

        Returns
        -------
        belief_label 
            Container of labels of the beliefs the interpretation updated or
            created.

        '''
        if surface_profile is None:
            self.belief['neighbour_generous'] = None
            self.belief['neighbour_id'] = None

        else:
            n_generous_gene = surface_profile.count('a')

            frac_generous = float(n_generous_gene) / float(len(surface_profile))
            self.belief['neighbour_generous'] = frac_generous
            self.belief['neighbour_id'] = neighbour_id

        return ('neighbour_generous', 'neighbour_id')

    def _mould_supply_molecules_to_env(self, my_neighbour, my_neighbour_id,
                                       induction):
        '''Determine amount of various molecules to add to environment

        Parameters
        ----------
        my_neighbour : float
            Belief about similarity of neighbour

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. Actuator parameters to
            push onto the surrounding molecules and poison, as well as an
            object force to adjust internal amounts of same compounds

        Raises
        ------
        RuntimeError
            In case the moulder is called without a belief about the
            neighbourhood

        '''
        if my_neighbour is None:
            raise RuntimeError('The supply moulder should only be ' + \
                               'executed with belief about neighbours')

        share_percentage = sigmoid_10(self.scaffold['generosity_mag'], 
                                      1.0 - self.scaffold['generosity'], False, 
                                      my_neighbour)
        poison_percentage = sigmoid_10(self.scaffold['attack_mag'],
                                       self.scaffold['attacker'], True,
                                       my_neighbour)
        
        compounds = [key for key in self.scaffold if 'molecule_' in key]
        compounds.append('poison_vacuole')

        ret_env = {}
        for molecule in compounds:
            current_amount = self.scaffold[molecule]

            # Poison is taken from the vacuole of the agent, but put into
            # general poison category of environment
            if molecule == 'poison_vacuole':
                dx_amount = poison_percentage * current_amount
                env_compound_key = 'poison'

            else:
                dx_amount = share_percentage * current_amount
                env_compound_key = molecule

            ret_env[env_compound_key] = dx_amount

            induction.set_map_func(molecule, 'force_func_delta', 
                                   {'increment' : -1.0 * dx_amount})

        actuator_pop = {'dx_molecules_poison' : ret_env}

        return MoulderReturn(actuator_pop, induction)

    def _mould_supply_molecules_to_one(self, my_neighbour, my_neighbour_id,
                                       induction):
        '''Bla bla

        '''
        share_data = self._mould_supply_molecules_to_env(my_neighbour,
                                             my_neighbour_id, induction)
        
        param_plus = {'dx_molecules_poison' : 
                      share_data.actuator_params['dx_molecules_poison'],
                      'give_to_id' : my_neighbour_id}

        return MoulderReturn(param_plus, share_data.object_map)

    def _mould_contemplate_suicide(self):
        '''Determine if the bacteria should kill itself or not

        Notes
        -----
        The decision is a function of scaffold properties only, no belief, as
        well as a stochastic component.

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. Actuator parameters to
            instruct death of agent, no object force reaction onto the agent
            otherwise

        '''
        x_poison = self.scaffold['poison']
        m_point = self.scaffold['vulnerability_to_poison']

        if x_poison > m_point:
            ret = {'do_it' : True}
        
        else:
            ret = {'do_it' : False}

        return MoulderReturn(ret, None)

    def _mould_gulp_molecules_from_env(self, my_neighbour):
        '''Take a fraction of environemtn content into bacteria, based on the
        current belief about the environment

        Parameters
        ----------
        my_neighbour : float
            Belief about similarity of neighbour

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. Actuator parameters for how
            much to gulp, No object force from this moulding

        '''
        if my_neighbour is None:
            trust = 1.0

        else:
            trust = my_neighbour

        gulp_percentage = sigmoid_10(self.scaffold['trusting_mag'], 
                                     1.0 - self.scaffold['trusting'], False, 
                                     trust)

        ret = {'how_much' : gulp_percentage}
        
        return MoulderReturn(ret, None)

    def _mould_make_poison(self, induction):
        '''Convert a certain amount of useful molecules to poison to store in
        the vacuole. The method generates no actuator population instruction

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. No actuator population
            instruction. The object force recomputes molecular content and
            poison content upon execution

        '''
        #
        # Compute fraction of molecules to turn into poison
        #
        p = self.scaffold['poison_vacuole']
        p_max = self.scaffold['poison_vacuole_max']
        d = self.scaffold['attack_mag']
        f = min(1.0, max(0.0, d * (p_max - p) / p_max))

        #
        # Compute the object map that is induced to apply to adjust compound content
        #
        ret_delta = {}
        total_molecule = 0.0
        compounds = [key for key in self.scaffold if 'molecule_' in key]
        n_compounds = len(compounds)
        for compound in compounds:
            poison_contribution = self.scaffold[compound] * f / float(n_compounds)
            total_molecule += poison_contribution 

            deduct_compound = poison_contribution / self.scaffold['poison_stoichometry']  
            induction.set_map_func(compound, 'force_func_delta', 
                                   {'increment' : -1.0 * deduct_compound})

        induction.set_map_func('poison_vacuole', 'force_func_delta',
                               {'increment' : total_molecule})

        return MoulderReturn(None, induction)

    def _mould_cell_division(self, induction):
        '''Method to attempt cell division and if successful instruct how
        resources are to be divided

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. The actuator is one Boolean
            to instruct if division should be done. The object force is present
            only in case division is done, in which relevant resources are cut
            in half

        '''
        compounds = [name for name in self.scaffold if 'molecule_' in name]
        thrs_compounds = [self.scaffold[x] >= self.scaffold['split_thrs'] for x in compounds]
        do_it = all(thrs_compounds)
        ret_params = {'do_it' : do_it}

        if not do_it:
            induction = None

        else:
            logging.debug('ALL MOLS')

            for compound in compounds:
                induction.set_map_func(compound, 
                                       'force_func_delta_scale',
                                       {'increment' : -1.0 * self.scaffold['split_thrs'],
                                        'factor' : 0.5})

            induction.set_map_func('poison_vacuole', 'force_func_scale', {'factor' : 0.5})
            induction.set_map_func('poison', 'force_func_scale', {'factor' : 0.5})

        return MoulderReturn(ret_params, induction)
            

    def __init__(self, scaffold, belief):
        
        self.scaffold = scaffold
        self.belief = belief
