'''Integration test of agent setup including an interpreter that accepts belief
as input and creates belief as output

'''
from core.agent import Agent

from core.instructor import Interpreter
from core.message import Belief, MessageOperator

REFVALUES = ['Yes', 'Doubt it', 'YES!']

def evaluate(hi, p):
    if hi * p > 0.80:
        return 'YES!'
    elif hi * p > 0.70:
        return 'Yes'
    elif hi * p > 0.5:
        return 'Maybe'
    else:
        return 'Doubt it'
#
# Define Messages
#
belief_input_1 = Belief('hostile_neighbourhood', ['hostility_index'])
belief_input_2 = Belief('i_am_followed', ['probability'])

belief_output = Belief('i_am_about_to_be_mugged', ['best_guess'])

belief_merge_input = MessageOperator([belief_input_1, belief_input_2], extend=True)
#
# Define Organs and their associated messages
#
interpreter = Interpreter('about_to_be_mugged', evaluate, belief_merge_input,
                          belief_output)

#
# Initialize Agent
#
agent = Agent('test_agent', True)
agent.set_organ(interpreter)
agent._set('belief', 'hostile_neighbourhood', belief_input_1)
agent._set('belief', 'i_am_followed', belief_input_2)

belief_input_1.set_values(0.8)
belief_input_2.set_values(0.95)
agent.interpret('about_to_be_mugged')
outcome_1 = agent.belief['i_am_about_to_be_mugged'].values()

belief_input_1.set_values(0.0)
belief_input_2.set_values(0.0)
agent.interpret('about_to_be_mugged')
outcome_2 = agent.belief['i_am_about_to_be_mugged'].values()

belief_input_1.set_values(0.9)
belief_input_2.set_values(1.0)
agent.interpret('about_to_be_mugged')
outcome_3 = agent.belief['i_am_about_to_be_mugged'].values()

assert (outcome_1[0] == REFVALUES[0])
assert (outcome_2[0] == REFVALUES[1])
assert (outcome_3[0] == REFVALUES[2])
