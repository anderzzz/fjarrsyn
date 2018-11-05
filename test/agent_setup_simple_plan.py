'''Simple Agent Setup with Plan 

'''
from core.agent import Agent
from core.organs import Sensor, Interpreter, Moulder, Actuator
from core.array import Buzz, Belief, Direction

from core.propagate import Chain, AutoBeliefCondition

class SlimAgent(Agent):

    def __call__(self):
        while self.heartbeat():
            if self.chain['sound_trigger'].execute():
                self.chain['response_formation'].execute()
                

    def __init__(self, name):
        super().__init__(name)

# Define Messages
#
buzz = Buzz('audio_trigger', (['a' + str(n) for n in range(1, 20)],))
belief = Belief('trigger_spoken', ['probability'])
direction = Direction('say_this', ['sentence'])

#
# Define Organs and their associated messages
#
sensor = Sensor('listen', 'sound_around_me', ear, buzz)
interpreter = Interpreter('was_trigger_word_spoken', buzz, trigger_word, belief)
moulder = Moulder('follow_up_question', belief, question_maker, direction)
actuator = Actuator('speak', direction, mouth, 'speak_to_the_world')

#
# Autonomous constraints
#
belief_condition = AutoBeliefConstraint('heard_it', belief, lambda x: x > 0.9)

#
# Plan
#
chain_1 = Chain('sound_trigger', ('listen', 'was_trigger_word_spoken'),
                belief_condition) 
chain_2 = Chain('response_formation', ('follow_up_question', 'speak'))
#
# Initialize Agent
#
agent = SlimAgent('test_agent')
agent.set_organ(sensor)
agent.set_organ(interpreter)
agent.set_organ(moulder)
agent.set_organ(actuator)

agent()
