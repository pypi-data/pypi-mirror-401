Examples
========

ctypes Shared Library
---------------------

This demo compiles a tiny C library and loads it via ``ctypes``. It is the
fastest path to understand how Python calls into native code without building
a full extension.

Build the shared library and run the ctypes demo:

.. code-block:: bash

   cd src/new_year_2026/examples/ctypes_shared
   cc -shared -fPIC -o libhello.so hello.c
   python hello_ctypes.py

.. note::

   On macOS, use ``libhello.dylib``. On Windows, build a ``hello.dll`` with MSVC.

C/C++ Extension Package (pybind11)
----------------------------------

This demo builds a standard Python package with a compiled extension module.

Build the extension package and install the wheel:

.. code-block:: bash

   cd src/new_year_2026/examples/extension_pkg
   python -m pip install -U pip build pybind11 wheel
   python -m build
   python -m pip install dist/*.whl

Use the extension:

.. code-block:: bash

   python -c "import hello_ext; print(hello_ext.add(2, 3)); print(hello_ext.mul(3, 4))"
