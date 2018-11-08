'''Simple Agent Setup with Plan 

'''
import numpy as np
import numpy.random
np.random.seed(79)

from core.agent import Agent
from core.organs import Sensor, Interpreter, Moulder, Actuator
from core.array import Buzz, Belief, Direction

from core.policy import Clause, AutoBeliefCondition

REF = ['ear','mouth','ear','ear','ear','ear','ear','mouth',
       'ear','mouth','ear','ear','mouth','ear']

class Env(object):
    def ear(self, agent_index):
        self.env_interactions.append('ear')
        ret = [np.sin(np.sqrt(x))**2 for x in np.random.random_integers(0,50,19)]
        return (ret,)

    def mouth(self, words, agent_index):
        self.env_interactions.append('mouth')

    def __init__(self):
        self.env_interactions = []

def trigger_word(nerves):
    if nerves[0] > 0.5:
        yup = 0.99
    else:
        yup = 0.01
    return yup

def question_maker(p):
    question = 'Well hello, what can I do for you?'
    return question

N_HEARTS = 10
class SlimAgent(Agent):

    def __call__(self):
        while self.heartbeat(N_HEARTS):
            if self.clause['sound_trigger'].apply_to(self):
                self.clause['response_formation'].apply_to(self)

    def __init__(self, name):
        super().__init__(name)

# Define Messages
#
buzz = Buzz('audio_trigger', (tuple(['a' + str(n) for n in range(1, 20)]),))
belief = Belief('trigger_spoken', ['probability'])
direction = Direction('say_this', ['sentence'])

#
# Define Organs and their associated messages
#
env = Env()
sensor = Sensor('listen', 'sound_around_me', env.ear, buzz)
interpreter = Interpreter('was_trigger_word_spoken', buzz, trigger_word, belief)
moulder = Moulder('follow_up_question', belief, question_maker, direction)
actuator = Actuator('speak', direction, env.mouth, 'speak_to_the_world')

#
# Autonomous constraints
#
belief_condition = AutoBeliefCondition('heard_it', belief, lambda x: x > 0.9)

#
# Plan
#
clause_1 = Clause('sound_trigger', verbs=('listen', 'was_trigger_word_spoken'),
                condition=belief_condition) 
clause_2 = Clause('response_formation', verbs=('follow_up_question', 'speak'))
#
# Initialize Agent
#
agent = SlimAgent('test_agent')
agent.set_organ(sensor)
agent.set_organ(interpreter)
agent.set_organ(moulder)
agent.set_organ(actuator)
agent.set_policy(clause_1)
agent.set_policy(clause_2)

agent()

assert (env.env_interactions == REF)
