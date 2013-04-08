.. _setup:

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
- pymongo (mongoDB driver) [#f4]_

On debian-based distributions, the dependencies can be installed
by executing::

    apt-get install python-numpy python-scipy python-prettytable

And additionally for pymongo::

    apt-get install python-pip
    pip install pymongo

Compiling the documentation
===========================

If you need to recompile the documentation, you'll need
[#f10]_ sphinx. Again, on debian-based distributions, it is::

    apt-get install python-pip python-matplotlib
    pip install sphinx sphinxcontrib-programoutput

You can then compile the documentation by executing::

    cd doc
    export PYTHONPATH=$PYTHONPATH:/path/to/algolab
    make html

And view it by pointing your browser to :file:`_build/html/index.html`.



.. [#f1] http://www.python.org
.. [#f2] http://www.numpy.org
.. [#f3] http://www.scipy.org
.. [#f4] http://docs.mongodb.org/ecosystem/drivers/python/
.. [#f10] http://sphinx.pocoo.org
