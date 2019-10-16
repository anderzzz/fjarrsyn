==========================
Fjarrsyn System Simulation
==========================

A simulation in ABM executes intentional and non-intentional dynamics
and propagates the modelled system. During the course of the simulation
properties of the system can be sampled and system-level properties
can be studied in the recorded data.

Simulations can take many forms. The agent system is designed without
any specific simulation method being used. Fjarrsyn however includes
a number of specific simulation method implementations for
convenience, though other methods can be developed.

The design of the specific simulation and sampling methods that are
available are described below. The description should also provide
a view into how custom simulation methods can be developed, though
specific details are deferred to subsequent sections.

System State Sampling
---------------------
A system of agents can be sampled and all relevant data of its state
extracted from the various objects and represented for easy analysis.
Three system state sampling classes are available, which can be
initialized without any detailed understanding of how the data is contained
in the various containers. The sampling classes are: *Agent Sampler*,
*Env Sampler* and *Graph Sampler*. In addition a class *System IO* is
available to conveniently write sampled data to disk.

Agent Sampler
^^^^^^^^^^^^^
An Agent has three persistent variables that together with its Instructors
determines any action of the Agent: Belief, Resource and Essence.
These three variables therefore define the state of the Agent. The
Agent Sampler samples the internal state of an Agent. Note that the
transient Buzz and Direction cannot be sampled.

Since Arrays have a defined semantic layer, the Agent Sampler is designed
to be fully initialized providing it with the semantics of the
part of the Agent state that is to be sampled. As long as the ABM was defined
with a clear semantics, the sampling of any Agent is as clearly defined.

Env Sampler
^^^^^^^^^^^
As Environment is designed with few constraints in fjarrsyn. The sampling
is therefore mostly defined by a sampling engine that takes the
environment object for an Agent, however defined, and returns a dictionary
of relevant state of the Environment. The Env Sampler adds meta data on
which Agent and when the sampling was done (assuming it is part of a
simulation), but otherwise relies on the provided engine to handle
the interface between the environment object and the fjarrsyn data
representation.

Graph Sampler
^^^^^^^^^^^^^
The relative position of Agents is defined by the agent network, or the
graph topology more specifically. The Graph Sampler is designed to
create a graph of identical topology to the Agent Network, however with the
nodes of the graph containing the Agent ID string, rather than the full
Agent object. Topological analysis can therefore be performed, or a
string representation for saving on disk created. The graph that the
Graph Sampler returns is a graph defined by the networkx Python library,
and hence any function or transformation of that library can be used.

System Simulation
-----------------
fff

Inverse Problem Simulation
--------------------------
Bla bla
