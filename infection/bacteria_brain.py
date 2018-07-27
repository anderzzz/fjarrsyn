'''All internal cognition of bacteria agent contained here

'''
import random
from core.helper_funcs import sigmoid, sigmoid_10, linear_step_10
from core.naturallaw import ObjectForce
from core.organs import MoulderReturn

class BacteriaBrain(object):
    '''Bla bla

    '''
    def _interpret_selfsimilarity_neighbourhood(self, surface_profile):
        '''Interpret how similar a neighbour surface profile is to the current
        agent's own surface profile.

        Parameters
        ----------
        surface_profile : str
            The string of characters defining the surface profile

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
            self.belief['my_neighbour'] = None

        else:
            my_profile = self.scaffold['surface_profile']

            if len(my_profile) != len(surface_profile):
                raise ValueError('The surface profile of neighbour ' + \
                                 '(%s) is not same ' %(surface_profile) + \
                                 'size as current profile (%s)' %(my_profile))

            n_same = 0
            for char_me, char_other in zip(my_profile, surface_profile):
                if char_me == char_other:
                    n_same += 1

            frac_same = float(n_same) / float(len(my_profile))
            self.belief['my_neighbour'] = frac_same

        return ('my_neighbour',)

    def _mould_supply_molecules_to_env(self, my_neighbour):
        '''Determine amount of various molecules to add to environment

        Parameters
        ----------
        my_neighbour : float
            Belief about similarity of neighbour

        Returns
        -------
        params : dict
            Dictionary of parameter values needed to populate the relevant
            actuator

        '''
        scaffold_shift = ObjectForce('shift_broth')

        share_percentage = sigmoid_10(self.scaffold['generosity_mag'], 
                                      self.scaffold['generosity'], False, 
                                      my_neighbour)
        poison_percentage = sigmoid_10(self.scaffold['attack_mag'],
                                       self.scaffold['attacker'], True,
                                       my_neighbour)
        
        compounds = [key for key in self.scaffold if 'molecule_' in key]
        compounds.append('poison_vacuole')

        ret_env = {}
        for molecule in compounds:
            current_amount = self.scaffold[molecule]
            dx_amount = share_percentage * current_amount

            # Poison is taken from the vacuole of the agent, but put into
            # general poison category of environment
            if molecule == 'poison_vacuole':
                env_compond_key = 'poison'

            else:
                env_compound_key = molecule

            ret_env[env_compound_key] = dx_amount

            scaffold_shift.set_force_func(molecule, 'delta', 
                                          {'increment' : -1.0 * dx_amount})

        actuator_pop = {'dx_molecules_poison' : ret_env}

        return MoulderReturn(actuator_pop, scaffold_shift)

    def _mould_contemplate_suicide(self):
        '''Determine if the bacteria should kill itself or not

        Notes
        -----
        The decision is a function of scaffold properties only, no belief, as
        well as a stochastic component.

        Returns
        -------
        params : dict
            Dictionary of parameter values needed to populate the relevant
            actuator

        '''
        x_poison = self.scaffold['poison']
        m_point = self.scaffold['vulnerability_to_poison']
        probability = sigmoid(1.0, 5.0, m_point, False, x_poison)

        if probability > random.random():
            ret = {'do_it' : True}
        
        else:
            ret = {'do_it' : False}

        return MoulderReturn(ret, None)

    def _mould_gulp_molecules_from_env(self, my_neighbour):
        '''Bla bla

        '''
        gulp_percentage = linear_step_10(self.scaffold['trusting_mag'], 0.0,
                                         self.scaffold['trusting'], False,
                                         my_neighbour)

        ret = {'how_much' : gulp_percentage}
        
        return MoulderReturn(ret, None)

    def _mould_make_poison(self):
        '''Convert a certain amount of useful molecules to poison to store in
        the vacuole. The method generates no actuator population instruction

        Returns
        -------
        mould_output : MoulderReturn
            Named tuple with output from moulding. No actuator population
            instruction. The object force recomputes molecular content and
            poison content upon execution

        '''
        scaffold_shift = ObjectForce('shift_broth')

        #
        # Compute fraction of molecules to turn into poison
        #
        p = self.scaffold['poison_vacuole']
        p_max = self.scaffold['poison_vacuole_max']
        d = self.scaffold['attacker']
        f = min(1.0, max(0.0, d - p * d / p_max))

        #
        # Generate the ObjectForce to apply to adjust compound content
        #
        ret_delta = {}
        total_molecule = 0.0
        compounds = [key for key in self.scaffold if 'molecule_' in key]
        n_compounds = len(compounds)
        for compound in compounds:
            deduct_compound = self.scaffold[compound] * f / float(n_compounds)
            total_molecule += deduct_compound

            scaffold_shift.set_force_func(compound, 'delta', 
                                          {'increment' : -1.0 * deduct_compound})

        scaffold_shift.set_force_func('poison_vacuole', 'delta',
                                      {'increment' : total_molecule})

        return MoulderReturn(None, scaffold_shift)

    def _mould_cell_division(self):
        '''Bla bla

        '''
        pass

    def __init__(self, scaffold, belief):
        
        self.scaffold = scaffold
        self.belief = belief
