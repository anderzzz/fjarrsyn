from core.agent import Agent, Socket
from core.agent_ms import AgentManagementSystem
from core.instructor import Sensor
from core.message import Buzz

class ABC(AgentManagementSystem):

    def f_sense(self, xxx):
        return xxx

    def __init__(self, name, agents, s1, s2):

        super().__init__(name, agents)

        buzz = Buzz('stuff', ('number',))
        agents[0].set_message(buzz)
        agents[0].set_organ(Sensor('S1', self.f_sense, buzz, 
                            sensor_func_kwargs={'xxx':s1}))
        buzz = Buzz('stuff', ('number',))
        agents[1].set_message(buzz)
        agents[1].set_organ(Sensor('S2', self.f_sense, buzz, 
                            sensor_func_kwargs={'xxx':s2}))

a1 = Agent('A1')
a2 = Agent('A2')
ams = ABC('dummy', [a1, a2], 1, 2)

a1.make_socket('tester', 'sense', 'S1', True)
a1.socket_offered['tester'].whitelist.add(a2.agent_id_system)
SOCK1 = [('tester', a1.socket_offered['tester'].token)]

a2.make_socket('tester', 'sense', 'S2', True)
a2.socket_offered['tester'].whitelist.add(a1.agent_id_system)
SOCK2 = [('tester', a2.socket_offered['tester'].token)]

ttt1 = SOCK2[0][1]
conn = a1.connect_to(a2, 'tester', ttt1)
conn.execute()
conn.close()
print (a1.buzz['stuff'])
print (a2.buzz['stuff'])
conn.execute()
