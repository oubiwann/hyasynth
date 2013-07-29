==========
star-music
==========


Set Up
------

All instructions below as well as examples, tutorials, etc., assume that you
are running star-music in a Python virtua environment. For example:

.. code:: bash

    $ virtualenv .venv --python=`which python2.7`
    $ . .venv/bin/activate
    (.venv) $


Dependencies
------------

star-music requires the pyo project to be installed. It is easiest to do this
via the binary packages available here:

http://code.google.com/p/pyo/downloads/list

For the rest of the dependencies, simply execute the following:

.. code:: bash

    (.venv) $ pip install -r requirements.txt