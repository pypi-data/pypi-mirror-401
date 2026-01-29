Overview
========

Goals
-----

- Learn how basic TCP sockets behave.
- Understand how TLS wraps a TCP connection.
- See simple HTTP and SSH protocol examples.
- Explore native extensions in Python with ctypes and pybind11.

Repository layout
-----------------

.. code-block:: text

   src/
     new_year_2026/
       tcp_tls/
         tcp_server.py
         tcp_client.py
         tls_echo_server.py
         tls_echo_client.py
         mini_tls_server.py
         get_or_post.py
         ssh_minimal_client.py
         cert.pem
         key.pem
       ctypes_shared/
       hello_ext/
   docs/
   .github/workflows/

Design principles
-----------------

- Keep demos small and readable.
- Prefer standard library APIs where possible.
- Show practical TLS and native extension usage without heavy frameworks.
