Frequent questions
==================

This section explain some common problems and how to solve it!

Installation and compilation problems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* If you want to change default GCC compiler to version 5, open a terminal and run:

.. code-block:: none

    export CC=/usr/bin/gcc-5
    export CXX=/usr/bin/g++-5

then you can compile using GCC 5.

ROS related problems
^^^^^^^^^^^^^^^^^^^^

under development...

Interface problems
^^^^^^^^^^^^^^^^^^

* When I close a node that uses gazebo, it takes too long before it closes.

Answer: You can close manually the process, run in a separate command window:

.. code-block:: none

    sudo killall gzserver gzclient



