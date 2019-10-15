'''Integration test of belief sharing between agents

'''
import pytest

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Buzz, Belief, Direction, Essence
from fjarrsyn.core.instructor import Sensor, Interpreter, Moulder, Actuator

REF = [['stupid_idea', 20180731],
       ['stupid_idea', 20180731],
       ['dummy_instruction_1', 20180731],
       ['dummy_instruction_1', 20180101]]

class School(AgentManagementSystem):

    def share_to_external(self, label, unit, agent_index):
        my_neighbours = self.neighbours_to(agent_index, agents_only=False)
        for node in my_neighbours:
            node.aux_content = (label, unit)

    def listen(self, agent_index):
        node = self.node_from_agent_id_[agent_index]
        my_env = node.aux_content
        if not my_env is None:
            ret = [my_env]
            my_env = None
        else:
            ret = None

        return ret

    def __init__(self, name, agents):

        super().__init__(name, agents)

        for agent in agents:
            if agent.name == 'Teacher':
                actuator = Actuator('Share', self.share_to_external, 
                                    agent.direction['Share this'],
                                    agent_id_to_engine=True)
                agent.set_organ(actuator)

            if agent.name == 'Student':
                sensor = Sensor('Listen for knowledge', self.listen,
                                agent.buzz['Knowledge feed'],
                                agent_id_to_engine=True)
                agent.set_organ(sensor)

class Teacher(Agent):

    def what_to_share(self, path, time, essence_degree):
        if essence_degree > 90.0:
            label = 'path to water'
            unit_to_share = path 
        elif essence_degree > 75.0:
            label = 'time to sow'
            unit_to_share = time 
        else:
            label = None
            unit_to_share = None

        return label, unit_to_share

    def __init__(self, name):

        super().__init__(name, strict_engine=True)

        essence = Essence('Trusting', ('degree',))
        essence.set_values([100.0])
        belief = Belief('Knowledge', ('path to water', 'time to sow'))
        belief.set_values(['dummy_instruction_1', 20180101])
        direction = Direction('Share this', ('knowledge label', 'knowledge unit'))
        moulder = Moulder('What to share', self.what_to_share, belief, direction,
                          essence_op_input=essence)
        self.set_organ(moulder)
        self.set_scaffold(essence)
        self.set_message(belief)

class Student(Agent):
    
    def what_to_accept(self, words, essence_degree, ptw, tts):
        if essence_degree > 50.0:
            if words[0] == 'path to water':
                ptw_ret = words[1]
            else:
                ptw_ret = ptw

            if words[0] == 'time to sow':
                tts_ret = words[1]
            else:
                tts_ret = tts

            return ptw_ret, tts_ret

        else:
            return ptw, tts

    def __init__(self, name):

        super().__init__(name, True)

        essence = Essence('Trusting', ('degree',))
        essence.set_values([10.0])
        belief = Belief('Knowledge', ('path to water', 'time to sow'))
        belief.set_values(['stupid_idea', 20180731])
        buzz = Buzz('Knowledge feed', ('words',))
        interpreter = Interpreter('Should I accept teaching',
                                  self.what_to_accept, buzz, belief,
                                  essence_op_input=essence,
                                  belief_updater=True)
        self.set_organ(interpreter)
        self.set_scaffold(essence)
        self.set_message(buzz)

def test_main():
    agent_1 = Teacher('Teacher')
    agent_2 = Student('Student')
    school = School('Knowledge Abound', [agent_1, agent_2])

    assert (agent_2.belief['Knowledge'].values() == REF[0])
    agent_1.mould('What to share')
    agent_1.act('Share')
    agent_2.sense('Listen for knowledge')
    agent_2.interpret('Should I accept teaching')
    assert (agent_2.belief['Knowledge'].values() == REF[1])

    agent_2.essence['degree'] = 75.0
    agent_1.mould('What to share')
    agent_1.act('Share')
    agent_2.sense('Listen for knowledge')
    agent_2.interpret('Should I accept teaching')
    assert (agent_2.belief['Knowledge'].values() == REF[2])

    agent_1.essence['degree'] = 80.0
    agent_1.mould('What to share')
    agent_1.act('Share')
    agent_2.sense('Listen for knowledge')
    agent_2.interpret('Should I accept teaching')
    assert (agent_2.belief['Knowledge'].values() == REF[3])
