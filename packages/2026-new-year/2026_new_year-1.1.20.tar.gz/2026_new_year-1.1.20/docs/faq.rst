FAQ
===

Why does TLS warn about certificates?
------------------------------------

The demo uses a self-signed certificate for local learning. Browsers and
clients will warn because it is not signed by a trusted CA.

Why are there native examples inside the package?
-------------------------------------------------

The examples are included so the wheel can ship a complete learning kit. The
extension package demo is still a standalone package under the examples path.

Can I run the examples without installing?
------------------------------------------

Yes. You can run modules directly from the source tree, for example:

.. code-block:: bash

   python -m new_year_2026.tcp_server
