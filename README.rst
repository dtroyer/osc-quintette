===================
python-oscquintette
===================

**Yet a glint of sunlight on the horizon**

OpenStackClient plugin

**oscquintette** is an OpenStackClient (OSC) plugin that demonstrates a
number of command-altering techniques and composite commands based on
common operations. It isn't as big as orchestration, but it does more
than one thing at a time...

Commands
========

``flavor find`` - Find a flavor based on minimum criteria

The prototype of the find process turns out to be useful itself,
although it should eventually be rolled into ``flavor list``.

``server create`` - Creates a Quintette-configured server

* Add flavor selection options (``--ram``, ``--disk``, ``--vcpus``) to
  specify minimum flavor requirements rather than know the flavor name or ID up front.

``server show`` - wrap the show command to munge the output

``qserver list`` - A server list powered entirely via code contained inside
oscquintette.

``show flavor`` - Demonstrate aliasing commands in other namespaces


----
The badly spelled **Quintette** is borrowed from the name of Raymond Scott's
group from the 1930's.  You may know parts of his __Powerhouse__ or __Dinner
Music For A Pack of Hungry Cannibals__ from Warner Bros. cartoons of the mid
20th century.
