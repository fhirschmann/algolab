=====
Setup
=====

Our project was written in Python and requires the following
dependencies:

Dependencies
============

- Python 2.7 [#f1]_ or higher
- numpy [#f2]_
- scipy [#f3]_
- utm [#f4]_

On debian-based distributions, the dependencies can be installed
by executing::

    apt-get install python-numpy python-scipy python-prettytable python-pip
    pip install utm

Commands
========

The toolbox features several commands, including:

- bin/al_filter

  .. program-output:: al_filter --help

- bin/al_visualize_algo

  .. program-output:: al_visualize_algo --help

- bin/al_visualize_rg

  .. program-output:: al_visualize_rg --help

- bin/al_visualize_data

  .. program-output:: al_visualize_data --help

- bin/al_inspect

  .. program-output:: al_inspect --help

- bin/al_cp

  .. program-output:: al_cp --help

- bin/al_rm

  .. program-output:: al_rm --help



Compiling the documentation
===========================

If you need to recompile the documentation, you'll need
[#f10]_ sphinx. Again, on debian-based distributions, it is::

    apt-get install python-sphinx python-pip
    pip install sphinxcontrib-programoutput

You can then compile the documentation by executing::

    cd doc
    make html

And view it by pointing your browser to :file:`_build/html/index.html`.



.. [#f1] http://www.python.org
.. [#f2] http://www.numpy.org
.. [#f3] http://www.scipy.org
.. [#f4] https://github.com/Turbo87/utm
.. [#f10] http://sphinx.pocoo.org
