'''Integration test of agent setup where Interpreter passes message to moulder

'''
import pytest
from fjarrsyn.core.agent import Agent

from fjarrsyn.core.instructor import Moulder, Interpreter
from fjarrsyn.core.message import Buzz, Belief, Direction, Resource, MessageOperator
from fjarrsyn.core.scaffold_map import ResourceMap

REF = [[True, 'yellow'], [True, 'black'], [False, None]]
REF_RESOURCE = [93.0, 88.0, 85.0]

def rain_predictor(n1, n2):
    if n1 + n2 < 1.0:
        return 1.0, -5.0
    elif n1 + n2 < 3.0:
        return 0.5, -2.0
    else:
        return 0.1, -1.0

def mood_maker(p):
    if p > 0.3 and p < 0.7:
        return 'existential_anxiety', -2.0
    else:
        return 'feel_ok', -1.0

def make_decision(p, m):
    get_umbrella = True 
    colour = None
    if p < 0.4:
        get_umbrella = False

    if get_umbrella:
        if m == 'existential_anxiety':
            colour = 'black'
        else:
            colour = 'yellow'

    return get_umbrella, colour, -1.0

def test_main():
    #
    # Define Messages
    #
    buzz = Buzz('nerve_endings', ('first', 'second'))
    belief_1 = Belief('chance_of_rain', ('probability',))
    belief_2 = Belief('ambiguity_kills_me', ('mood',))
    direction = Direction('get_which_umbrella', ('any', 'colour'))

    #
    # Define Scaffold and Map for it
    #
    agent_resources = Resource('internal_resource', ('energy',))
    agent_resources.set_values([100.0])
    change_energy = ResourceMap('adjust_energy', 'delta', 'energy', ('how_much',))

    #
    # Define Organs and their associated messages
    #
    interpreter_1 = Interpreter('will_it_rain', rain_predictor, buzz, belief_1,
                                resource_map_output=change_energy)
    interpreter_2 = Interpreter('am_i_unlucky', mood_maker, belief_1, belief_2,
                                resource_map_output=change_energy)
    total_belief = MessageOperator([belief_1, belief_2], extend=True)
    moulder = Moulder('fetch_umbrella_type', make_decision, total_belief, direction,
                       change_energy)

    #
    # Initialize Agent
    #
    agent = Agent('test_agent', strict_engine=True)
    agent._set('buzz', 'nerve_endings', buzz)
    agent.set_organ(moulder)
    agent.set_organ(interpreter_1)
    agent.set_organ(interpreter_2)
    agent.set_scaffold(agent_resources)

    #
    # Decide on direction and execute action
    #
    agent.buzz['nerve_endings'].set_values([0.2, 0.2])
    agent.interpret('will_it_rain')
    agent.interpret('am_i_unlucky')
    agent.mould('fetch_umbrella_type')
    assert (agent.direction['get_which_umbrella'].values() == REF[0])
    assert (agent.resource.values()[0] == pytest.approx(REF_RESOURCE[0]))

    agent.buzz['nerve_endings'].set_values([1.0, 0.6])
    agent.interpret('will_it_rain')
    agent.interpret('am_i_unlucky')
    agent.mould('fetch_umbrella_type')
    assert (agent.direction['get_which_umbrella'].values() == REF[1])
    assert (agent.resource.values()[0] == pytest.approx(REF_RESOURCE[1]))

    agent.buzz['nerve_endings'].set_values([1.0, 2.6])
    agent.interpret('will_it_rain')
    agent.interpret('am_i_unlucky')
    agent.mould('fetch_umbrella_type')
    assert (agent.direction['get_which_umbrella'].values() == REF[2])
    assert (agent.resource.values()[0] == pytest.approx(REF_RESOURCE[2]))

