README
======

This is a simple script used to permanently delete Google Sites. It was created
from a need to delete Sites programmatically despite an API deliberately not
being exposed for the function.


Installation
------------

This isn't yet on PyPi, so install it directly with ``pip``::

   $ pip install -e git://github.com/tdavis/goog-rmsite.git 

You will also likely need to install ``xephyr`` and ``xvfb``, used for managing
the virtual display which removes the need for a visible browser. How you
install these depends on your operating system. Ubuntu users should install the
``xvfb`` and ``xserver-xephyr`` packages; Fedora users should do something
like::

   $ yum install xorg-x11-server-Xephyr xorg-x11-server-Xvfb
   $ daemonize -p /tmp/xvfb100 `which Xvfb` :100 -ac
   $ DISPLAY=:100.0 rmsite [...]

This daemonizes a new virtual display and then instructs ``rmsite`` to use it.
You may kill the display with ``kill `cat /tmp/xvfb100```.


Usage
-----

The script works by logging in as a specified Google user, finding sites, and
first soft then hard deleting them one by one up to a maximum number, or until
it runs out of sites. An average removal takes 15 seconds.

Features:

* Uses virtual display via ``PyVirtualDisplay``; no desktop browser necessary
* "Safe" password input option (via ``getpass()``)
* Ability to specify delete count
* Some error recovery

Run ``rmsite --help`` and enjoy!
