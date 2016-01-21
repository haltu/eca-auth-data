
Auth Data service
*****************

Auth Data service is part of Educloud Alliance reference implementation
of the Educloud Alliance Standard.

See http://docs.educloudalliance.org for more information what is
the purpose of this service and how it integrates to other services.

This documentation is meant for the developer working with the source
code of this service.

.. automodule:: authdata

Data model
==========

.. automodule:: authdata.models

The API
=======

Authentication to the API is based on tokens. You should send ``Authorization: Token abcd1234`` header. For example::

  curl -H "Authorization: Token 9c5d6df27105387b586286b06684ac2dcdbf09d3"  http://foo.example.com/api/1/user/

For debugging purposes you can also use session based authentication if
you have credentials to access the admin pages. So if you can log into admin you can access the API with the same browser.

.. automodule:: authdata.views
.. automodule:: authdata.serializers

External data sources
=====================

.. automodule:: authdata.datasources

Base for all data sources
-------------------------

.. automodule:: authdata.datasources.base

LDAP
----

.. automodule:: authdata.datasources.ldap_base

Oulu LDAP
---------

.. automodule:: authdata.datasources.oulu

Dreamschool
-----------

.. automodule:: authdata.datasources.dreamschool

Admin
=====

.. automodule:: authdata.admin

Forms
=====

.. automodule:: authdata.forms

Tests
=====

.. automodule:: authdata.tests

.. automodule:: authdata.tests.test_admin
  :undoc-members:
  :no-private-members:

.. automodule:: authdata.tests.test_datasources
  :undoc-members:
  :no-private-members:

.. automodule:: authdata.tests.test_forms
  :undoc-members:
  :no-private-members:

.. automodule:: authdata.tests.test_models
  :undoc-members:
  :no-private-members:

.. automodule:: authdata.tests.test_serializers
  :undoc-members:
  :no-private-members:

.. automodule:: authdata.tests.test_views
  :undoc-members:
  :no-private-members:

Factories
---------

.. automodule:: authdata.tests.factories
  :undoc-members:





