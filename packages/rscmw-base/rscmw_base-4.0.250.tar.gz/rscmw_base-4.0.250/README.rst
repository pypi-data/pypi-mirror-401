==================================
 rscmw-base
==================================

.. image:: https://img.shields.io/pypi/v/rscmw-base.svg
   :target: https://pypi.org/project/ rscmw-base/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://rscmw-base.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/rscmw-base.svg
   :target: https://pypi.python.org/pypi/rscmw-base/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/rscmw-base.svg
   :target: https://pypi.python.org/pypi/rscmw-base/

Rohde & Schwarz CMW Base System rscmw-base instrument driver.

Basic Hello-World code:

.. code-block:: python

    from rscmw_base import *

    instr = RsCmwBase('TCPIP::192.168.2.101::hislip0')
    idn = instr.utilities.query('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: CMW500, CMW100, CMW270, CMW280

The package is hosted here: https://pypi.org/project/rscmw-base/

Documentation: https://rscmw-base.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

	Latest release notes summary: New package+module name, update for FW 4.0.250

	Version 4.0.250
		- New package and module name 'rscmw_base'
		- Update for FW 4.0.250
