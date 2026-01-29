Packaging
=========

Main package
------------

.. code-block:: bash

   python -m pip install -U build
   python -m build

This produces ``dist/*.whl`` and ``dist/*.tar.gz`` for the main package.

Extension demo package
----------------------

.. code-block:: bash

   cd src/new_year_2026/examples/extension_pkg
   python -m pip install -U build pybind11 wheel
   python -m build

For manylinux and macOS wheels (CI uses this), run ``cibuildwheel``:

.. code-block:: bash

   python -m pip install -U cibuildwheel
   CIBW_BUILD="cp39-*" CIBW_SKIP="pp* *musllinux*" \
     python -m cibuildwheel --output-dir dist

Notes:

- The extension demo builds native binaries (.so/.pyd).
- A C/C++ compiler is required on the build machine.

Release tagging
---------------

When you create a git tag (for example, ``v1.0.0``), the CI workflow builds
packages, publishes them to PyPI, and attaches artifacts to the GitHub Release.

PyPI
----

This project publishes to PyPI on tag builds. You can also publish manually:

.. code-block:: bash

   python -m pip install -U twine
   python -m twine upload dist/*

Use a PyPI API token for authentication.
