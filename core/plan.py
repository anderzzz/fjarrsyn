'''Bbla bla

'''
from collections import namedtuple
import networkx as nx

class Plan(object):
    '''Bla bla

    '''
    def from_json(self, filepath):
        '''Bla bla

        '''
        pass

    def to_json(self, filepath):
        '''Bla bla

        '''
        pass

    def _get_root_index(self, t):
        '''Bla bla

        '''
        return [n for n, d in t.in_degree() if d == 0].pop(0)

    def enact_upon(self, agent, current_root_id=None):
        '''Bla bla

        '''
        if current_root_id is None:
            current_root_id = self.tree_root_id

        current_node = self.tree.nodes[current_root_id]
        verb = current_node['verb']
        phrase = current_node['phrase']

        ret_val = getattr(agent, verb)(phrase)

        successors = self.tree.successors(current_root_id)

        for n in successors:
            if self.tree.edges[current_root_id, n]['polarity'] is True and \
                   ret_val is True:

                self.enact_upon(agent, n)

            elif self.tree.edges[current_root_id, n]['polarity'] is False and \
                    ret_val is False:

                self.enact_upon(agent, n)

            else:
                raise RuntimeError('Unmatched verb return and plan edge ' + \
                                   'attribute. Could be caused by missing ' + \
                                   'cargo')

        return 'Leaf reached'

    def add_cargo(self, verb_inp, phrase_inp):
        '''Bla bla

        '''
        self.tree.add_node(self.cargo_counter, verb=verb_inp, phrase=phrase_inp)
        self.cargo_counter += 1

        return self.cargo_counter

    def add_dependency(self, cc_parent, cc_child_true, cc_child_false=None):
        '''Bla bla

        '''
        self.tree.add_edge(cc_parent, cc_child_true, polarity=True)
        if not cc_child_false is None:
            self.tree.add_edge(cc_parent, cc_child_false, polarity=False)

    def make_plan_tree(self):
        '''Bla bla

        '''
        if not nx.is_tree(self.tree):
            raise ValueError('The plan graph is not structured like a tree')
        self.tree_root_id = self._get_root_index(self.tree)

    def __init__(self, name, tree=None):

        self.name = name
        self.tree = nx.DiGraph() 
        self.cargo_counter = 0
