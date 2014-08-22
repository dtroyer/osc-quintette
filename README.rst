===================
python-oscquintette
===================

**Yet a glint of sunlight on the horizon**

OpenStackClient plugin

**oscquintette** is an OpenStackClient (OSC) plugin that performs a number
of composite commands based on common operations. It isn't as big as
orchestration, but it does more than one thing at a time...

Commands
========

``qserver create`` - Creates a Quintette-configured server

The first step is to add flavor selection options (``--ram``, ``--disk``, ``--vcpus``)
to specify minimum flavor requirements rather than know the flavor name or ID up front.

``flavor find`` - Find a flavor based on minimum criteria

The prototype of the find process turns out to be useful itself,
although it should eventually be rolled into ``flavor list``.

----
The badly spelled **Quintette** is borrowed from the name of Raymond Scott's
group from the 1930's.  You may know parts of his __Powerhouse__ or __Dinner
Music For A Pack of Hungry Cannibals__ from Warner Bros. cartoons of the mid
20th century.
