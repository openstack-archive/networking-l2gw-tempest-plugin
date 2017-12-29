Tempest Integration of Networking L2GW
=======================================

Networking L2GW Tempest plugin contains api, cli and clients tests.

There are several ways to run Tempest tests: it is possible to run them using
your Devstack or using Rally.

Run Tempest tests on Devstack
-----------------------------

See how to configure Tempest at
`Tempest Configuration Guide <https://docs.openstack.org/tempest/latest/configuration.html>`_.

Tempest automatically discovers installed plugins. That's why you just need to
install the Python packages that contains the Networking L2GW Tempest plugin in
the same environment where Tempest is installed.

.. sourcecode:: console

  $ git clone https://git.openstack.org/openstack/networking-l2gw-tempest-plugin
  $ cd networking-l2gw-tempest-plugin/
  $ pip install networking-l2gw-tempest-plugin/

..

After that you can run Tempest tests. There you can specify the name of
test (and even run a single test from directory). One way to run Tempest
tests by using ``ostestr`` command, for instance:

.. sourcecode:: console

    $ ostestr networking_l2gw_tempest_plugin.tests.api.test_l2gw_extensions.L2GatewayExtensionTestJSON.test_create_show_list_delete_l2gateway_connection

..

The command ``tempest run`` is another way to run tests. See the additional
information about using this `command <https://docs.openstack.org/tempest/latest/run.html>`_.

For example, the following command will run all the Tempest tests.

.. sourcecode:: console

    $ tempest run

..

Finally, you can use ``testr`` directly to run the tests. For example,
the following command will run all the cli-tests:

.. sourcecode:: console

    $ testr run networking_l2gw_tempest_plugin.tests.api

..

Useful links:

* `Running Tempest tests with testr <https://docs.openstack.org/tempest/latest/overview.html#legacy-run-method>`_.
* `Using Tempest plugins <https://docs.openstack.org/tempest/latest/plugin.html#using-plugins>`_.
* `Tempest Quickstart <https://docs.openstack.org/tempest/latest/overview.html#quickstart>`_.
