
Auth Data service
*****************

Auth Data service is part of Educloud Alliance reference implementation
of the Educloud Alliance Standard. It is an abstraction of actual
data store, or multiple datastores, which contain user
identity and role information.

The Auth Data service does not have visible UI, only an API which can be queried the contents
of the database.

See http://docs.educloudalliance.org for more information what is
the purpose of this service and how it integrates to other services.

This documentation is meant for the developer working with the source
code of this service.

.. toctree::

  modules
  external_sources


The API
=======

Data returned from the API looks like this::

  {
    "username": "123abc",
    "first_name": "Teppo",
    "last_name": "Testaaja",
    "roles": [
      {
        "school": "17392",
        "role": "teacher",
        "group": "7A",
        "municipality": "1234567-8"
      },
      {
        "school": "17392",
        "role": "teacher",
        "group": "7B",
        "municipality": "1234567-8"
      }
    ]
    "attributes": [
      {
        "name": "attribute1_id",
        "value": "attribute1_data"
      },
      {
        "name": "attribute2_id",
        "value": "attribute2_data"
      }
    ]
  }

The Auth Data service tries to model the real situation
where one user can be teacher and student in different schools.
User can have multiple roles, and also multiple roles in one school.

General fields:

username
  This is unique identifier for the user.

Fields in the ``roles`` dict are defined as follows:

school
  Official school ID.
role
  Either ``"teacher"`` or ``"student"``.
group
  The class or group for the user.

In addition to role data custom attributes can be added at runtime. These are installation specific and defined in
the database.


Authentication to the API
-------------------------

Authentication to the API is based on tokens. You should send ``Authorization: Token abcd1234`` header. For example::

  curl -H "Authorization: Token 9c5d6df27105387b586286b06684ac2dcdbf09d3"  http://foo.example.com/api/1/user/

For debugging purposes you can also use session based authentication if
you have credentials to access the admin pages. So if you can log into admin you can access the API with the same browser.


Attribute query
---------------

The attribute query endpoint is meant to be used by the SAML IdP to query for the attributes of single user.

Auth Data has endpoint ``/api/1/query?name=value`` which can be queried for the attributes. The result is JSON dict of data.

Query is made by GET parameters. Only one parameter is allowed. ``Not found`` is returned if:

  * the parameter name is not recognized
  * multiple results would be returned (only one result is allowed)
  * no parameters are specified

In the query ``name`` is the parameter name used to filter users from the database. Name of the parameter is defined when new auth
sources are registered to the IdP. Name of the parameter can contain only a-z chars.
The list of valid filter names is available from IdP admins.
The value for the filter parameter is UTF-8 as urlencoded string.

For example, query could be: ``/api/1/query?facebook_id=foo``

User attributes can be queried with username also. For example:
``/api/1/query/[username]``


User search query
-----------------

User objects can be searched by ``municipality``, ``school``, ``group``, ``username`` and ``changed_at`` attributes.

* ``municipality`` is a mandatory search parameter
* ``school``, ``group`` and ``username`` are string parameters
* ``changed_at`` is a POSIX timestamp parameter. Only records changed after
  this timestamp will be returned. When used with external datasources this
  parameter has no effect on results.

Example query: ``/api/1/user/?municipality=Esimerkkikunta&school=Keskustan%20koulu&group=7A&changed_at=1444398009``

This returns all matches. The data returned is in the same format as the
Attribute query data, with the exception that only attributes from the querying
user's source are returned.


External Sources
================

Auth Data can act as a proxy for external user data sources. In this case user
data is stored only in the external source and not in Auth Data. Auth Data will
however maintain a record of the user identity, storing the external source
name, user unique identifier in the external source and any attributes that are
associated to the user account.

Each external source is a unique case, for example an LDAP database requiring
credentials and having a specific schema where the information about users is
stored. Each external source has a middleware implementation which is
responsible for reading data and presenting it to Auth Data using a specific
interface. This interface is specified in the abstract interface class
ExternalDataSource (in models.py) which must be inherited by external data
source implementations.

External sources are configured in Auth Data settings. In user list query (``/api/1/user/``) the
municipality search term is used to forward the query to the external source
implementation. In the attribute query (``/api/1/query``) Auth Data finds the
user in it's local database based on attribute or username the local User
object contains the external source name and external source unique id which
are used for querying the actual user data from the source.


