=======================
flake8-unused-fstrings
=======================

.. start short_desc

**Flake8 plugin to catch f-strings with no fields.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/python-formate/flake8-unused-fstrings/workflows/Linux/badge.svg
	:target: https://github.com/python-formate/flake8-unused-fstrings/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-formate/flake8-unused-fstrings/workflows/Windows/badge.svg
	:target: https://github.com/python-formate/flake8-unused-fstrings/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-formate/flake8-unused-fstrings/workflows/macOS/badge.svg
	:target: https://github.com/python-formate/flake8-unused-fstrings/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-formate/flake8-unused-fstrings/workflows/Flake8/badge.svg
	:target: https://github.com/python-formate/flake8-unused-fstrings/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-formate/flake8-unused-fstrings/workflows/mypy/badge.svg
	:target: https://github.com/python-formate/flake8-unused-fstrings/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-unused-fstrings/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-unused-fstrings/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-formate/flake8-unused-fstrings/master?logo=coveralls
	:target: https://coveralls.io/github/python-formate/flake8-unused-fstrings?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-formate/flake8-unused-fstrings?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-formate/flake8-unused-fstrings
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/flake8-unused-fstrings
	:target: https://pypi.org/project/flake8-unused-fstrings/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flake8-unused-fstrings?logo=python&logoColor=white
	:target: https://pypi.org/project/flake8-unused-fstrings/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flake8-unused-fstrings
	:target: https://pypi.org/project/flake8-unused-fstrings/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/flake8-unused-fstrings
	:target: https://pypi.org/project/flake8-unused-fstrings/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/python-formate/flake8-unused-fstrings
	:target: https://github.com/python-formate/flake8-unused-fstrings/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-formate/flake8-unused-fstrings
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-formate/flake8-unused-fstrings/v2.0.0
	:target: https://github.com/python-formate/flake8-unused-fstrings/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-formate/flake8-unused-fstrings
	:target: https://github.com/python-formate/flake8-unused-fstrings/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2026
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/flake8-unused-fstrings
	:target: https://pypi.org/project/flake8-unused-fstrings/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``flake8-unused-fstrings`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install flake8-unused-fstrings

.. end installation


Rules
------

* **NUF001**: f-string without interpolation.
