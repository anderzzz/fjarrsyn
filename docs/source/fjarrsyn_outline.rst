============================
Fjarrsyn ABM Library Outline
============================

Fjarrsyn is a library to perform ABM. It is built as a very general and 
flexible tool, such that the nature of the agents or the system they are
part of is unconstrained by any particular domain, such as biology, markets,
orientation and so on.

In this short subsection Fjarrsyn is introduced at the highest level, and
in subsequent sections are specific aspects documented, including tutorials.
The description that follows in particular to Fjarrsyn and may not
always apply to ABM in general.

The agent is constrained with respect to its internal structure,
such that the logic connections between inputs, beliefs, actions etc. can be
clearly defined, analyzed and compared. However, the functional constraints 
implied by the structural constraints are few, therefore the agent 
as defined in Fjarrsyn can model diverse types of domain specific agents. 
In particular, the belief-desire-intention (BDI) type of agent can be
modelled in Fjarrsyn.

A visual representation of key structural features and nomenclature of an
agent is shown in the image below. The details of this image will be
described in later sections. The image conveys how a set of messages and
instructors connect in order to generate an agent that can interact in
meaningful ways with its environment.

.. image:: /_static/fjarrsyn_agent.jpg

The system a set of agents is part of is structurally defined as a network
of arbitrary topology. A system wherein any agents can interact with all other
agents for example, corresponds to a fully connected network. In some 
domains 
