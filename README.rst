========
Hyasynth
========

.. image:: resources/logos/hyasynth-logo-192.png


Dependencies
------------

Hyasynth requires `SuperCollider`_ to be installed (and for now, running). You
can download the appropriate binary for your system at the
`SuperCollider downloads page`_:

The rest of the dependencies will be automatically installed by the ``make``
targets. The ``make`` target that installs the deps can, of course, be called
directly:

.. code:: bash

    $ make deps


Getting Started
---------------

To get Hyasynth up and running quickly, simply do this:

.. code:: bash

  $ make start

You will be greeted with a banner like the following:

.. code:: text

  :>
  : Welcome to
  :  _  _                       _   _
  : | || |_  _ __ _ ____  _ _ _| |_| |_
  : | __ | || / _` (_-< || | ' \  _| ' \
  : |_||_|\_, \__,_/__/\_, |_||_\__|_||_|
  :       |__/         |__/
  :
  : You have logged onto a Hyasynth Server; you are currently at a Hy
  : command prompt. Hy is a Lisp dialect of Python of which you can
  : learn more about here:
  :   https://github.com/hylang/hy
  : Information on Hyasynth is available here:
  :   http://github.com/oubiwann/hyasynth
  :
  :
  : Type '(ls)' or '(dir)' to see the objects in the current namespace.
  : Use (help ...) to get API docs for available objects.
  :
  : Enjoy!
  :
  :>

You can check the status of your running SuperCollider server with the commend:

.. code:: lisp

  :> (status)
  {'status': {'synths': 0, 'groups': 1, 'peak cpu': 0.06004318222403526,
  'average cpu': 0.02159080281853676, 'loaded synths': 0,
  'nominal sample rate': 7.17291259765625, 'unit generators': 0,
  'actual sample rate': 0.0}}

If you haven't started the SuperCollider server, then you'll get a message like
this:

.. code:: lisp

  :> (status)
  {'status': 'connection refused'}
  
.. Links
.. -----
.. _SuperCollider: http://supercollider.sourceforge.net/
.. _SuperColler downloads page: http://supercollider.sourceforge.net/downloads/
