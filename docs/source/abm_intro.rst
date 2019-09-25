#####################################
What is Agent-Based Modelling
#####################################
 
This page introduces Agent-Based Modelling (ABM) and what it enables.

==================================
Purpose of Agent-Based Modelling 
==================================
Agent-Based Modelling (ABM) is a means to investigate a system of interacting 
agents. Each agent can take actions. These actions are chosen independently by
each agent on basis of information and resources said agent has at any
given moment.
The information can reflect one or more properties of the
system the agent is part of. The properties of the system can in turn depend on
the accumulated outcomes of actions by other agents of the system.
 
Under these conditions, the system of agents evolves and macroscopic or 
system-wide patterns can emerge that are not straight-forward reflections of 
the intentions or actions of any single agent. ABM enables
the study and design of these emergent phenomena as complex functions of agent and
agent interaction properties.

Examples of real-world systems that can be modelled with ABM include: 

* **Car traffic.** Each driver decides what actions to take on basis of an
  objective and incomplete information about the state of the roads, including
  what other drivers are choosing to do.

* **Housing market.** The buyers and sellers are agents in the market each 
  seeking to meet some objective in an environment of incomplete, possibly asymmetric,
  information about a given real-estate property as well as the intentions
  of other buyers and sellers in the market.

* **Evolution of predator and prey.** The agents are organisms that relate to each
  other through death and survival, where survival strategies can proliferate as
  agents mutate and procreate.

* **Geopolitics.** The agents are nations or political institutions with potentially
  conflicting objectives that each seek to exploit its information and resources
  in order to attain their respective objectives.

Neither of these systems have an all-knowing, omnipotent agent that decides the
actions of all agents. A housing market, for example, may have rules that constrain it,
but no single agent decides all outcomes. Evolution through natural selection
is the archetypical system in which intricate and durable structure and 
function exist without any single ruler that determines all.

Under these circumstances a system design objective can be: what rules and 
constraints would lead to the maximum collective utility or benefit given
that the system is populated by agents that each attempts to maximize its
own utility or benefit, not that of the system as a whole. Or conversely,
given a system design, what properties of an agent lead to what emergent
outcomes.

Finally it is noted that ABM is related to game theory. 
The latter is a theory of strategy in an
environment of self-interested agents with potentially conflicting objectives.
The Prisoner's Dilemma is the best known outcome of a type of game
between two agents, where the optimal outcome for both self-interested and
rational agents eludes them. Game theory is by design built on very
simple agents and agent interactions. ABM enables diverse agents that are
internally complicated engaged in a wide variety of interactions. ABM can
therefore be used to quantitatively explore more types of systems that
correspond better with the real-world of agents, information and 
intentional actions.

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
