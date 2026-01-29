Quickstart
==========

Environment
-----------

Create and activate a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate

Install the package (from a wheel or local source):

.. code-block:: bash

   python -m pip install -U pip
   python -m pip install .

Run a TCP echo demo
-------------------

Start the server:

.. code-block:: bash

   python -m new_year_2026.tcp_server

In another terminal, run the client:

.. code-block:: bash

   python -m new_year_2026.tcp_client

Run a TLS echo demo
-------------------

.. code-block:: bash

   python -m new_year_2026.tls_echo_server
   python -m new_year_2026.tls_echo_client

.. note::

   The bundled certificate is self-signed and intended for local learning.
