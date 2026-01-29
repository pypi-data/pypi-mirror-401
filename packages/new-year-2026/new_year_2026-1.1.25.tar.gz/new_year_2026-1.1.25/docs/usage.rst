Usage
=====

Install
-------

.. code-block:: bash

   python -m pip install 2026-new-year

Run modules
-----------

TCP echo:

.. code-block:: bash

   python -m new_year_2026.tcp_tls.tcp_server
   python -m new_year_2026.tcp_tls.tcp_client

TLS echo:

.. code-block:: bash

   python -m new_year_2026.tcp_tls.tls_echo_server
   python -m new_year_2026.tcp_tls.tls_echo_client

HTTP demo:

.. code-block:: bash

   python -m new_year_2026.tcp_tls.get_or_post

Minimal SSH banner:

.. code-block:: bash

   python -m new_year_2026.tcp_tls.ssh_minimal_client

Import from Python
------------------

.. code-block:: python

   import new_year_2026.tcp_tls.tcp_server
   import new_year_2026.tcp_tls.tls_echo_client

.. tip::

   The demos use simple defaults (localhost and fixed ports). Open the source
   files to see how to tweak host/port values.
