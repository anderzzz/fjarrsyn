'''Simple Agent Setup Integration Test

'''
from core.agent import Agent

from core.organ import Moulder, Interpreter 
from core.array import Buzz, Belief, Direction, Resource, ImprintOperator
from core.naturallaw import ResourceMap

REF = [[True, 'yellow'], [True, 'black'], [False, None]]
REF_RESOURCE = [93.0, 88.0, 85.0]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

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
change_energy = ResourceMap('adjust_energy', 'energy', 'delta', ('how_much',))

#
# Define Organs and their associated messages
#
interpreter_1 = Interpreter('will_it_rain', buzz, rain_predictor, belief_1,
                            resource_map=change_energy)
interpreter_2 = Interpreter('am_i_unlucky', belief_1, mood_maker, belief_2,
                            resource_map=change_energy)
total_belief = ImprintOperator([belief_1, belief_2], merger=True).merge
moulder = Moulder('fetch_umbrella_type', total_belief, make_decision, direction,
                   change_energy)

#
# Initialize Agent
#
agent = Agent('test_agent')
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
assert (isclose(agent.resource.values()[0], REF_RESOURCE[0]))

agent.buzz['nerve_endings'].set_values([1.0, 0.6])
agent.interpret('will_it_rain')
agent.interpret('am_i_unlucky')
agent.mould('fetch_umbrella_type')
assert (agent.direction['get_which_umbrella'].values() == REF[1])
assert (isclose(agent.resource.values()[0], REF_RESOURCE[1]))

agent.buzz['nerve_endings'].set_values([1.0, 2.6])
agent.interpret('will_it_rain')
agent.interpret('am_i_unlucky')
agent.mould('fetch_umbrella_type')
assert (agent.direction['get_which_umbrella'].values() == REF[2])
assert (isclose(agent.resource.values()[0], REF_RESOURCE[2]))

