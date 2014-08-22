===================
python-oscquintette
===================

**Yet a glint of sunlight on the horizon**

OpenStackClient plugin

**oscquintette** is an OpenStackClient (OSC) plugin that performs a number
of composite commands based on common operations. It isn't as big as
orchestration, but it does more than one thing at a time...

A ``qserver`` is a set of attributes describing a server and some additional
resources to accompany it.

Commands
========

``qserver create`` - Creates a Quintette-configured server

* if only a qserver name is given, and it exists, the qserver will be created
* if --define is included the server configuration will be saved under the
specified name

Qserver definitions are saved in a local config file.
If we get really fancy we'll put them in the object store!

``qserver delete`` - Delete a configured server and optionally its
associated variable resources.

* basically volumes may be be deleted, the remaining resources are likely to be re-used

Objects
=======

The resource objects available for inclusion in a qserver definition are a subset
of those already defined in OSC.

* flavor: a flavor name/id, or a list of primary flavor attributes used to locate the closes flavor available
* key-name: a key pair name, or a filename to upload
* image: an image name/id, or a list of image properties used to locate the closest image available
* security-group: a security group
* volume: a volume name/id, or a list of volume attributes used to create a new one

----
The badly spelled **Quintette** is borrowed from the name of Raymond Scott's
group from the 1930's.  You may know parts of his __Powerhouse__ or __Dinner
Music For A Pack of Hungry Cannibals__ from Warner Bros. cartoons of the mid
20th century.
