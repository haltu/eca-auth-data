
Auth Data database for EduCloud
*******************************

The Auth Data component does not have visible UI, only an API which can be queried the contents
of the database.

The Auth Data component is an abstraction of actual data store, or multiple datastores, which contain user
identity and role information.


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
        "attribute1_id": "attribute1_data",
        "attribute2_id": "attribute2_data"
      }
    ]
  }

User can have multiple roles, and also multiple roles in one school. As the Auth Data service tries to model the real situation
where one user can be teacher and student in different shools this has to be here. It is also possible to decide that
only one role object per user is acceptable when the data is imported to the database.

General fields:

username
  This is the OID. It follows the OID specification.

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

User search query
-----------------

User objects can be searched by ``school``, ``group``, ``username`` and ``changed_at`` attributes.

* ``school``, ``group`` and ``username`` are string parameters
* ``changed_at`` is a POSIX timestamp parameter. Only records changed after
  this timestamp will be returned

Example query: ``/api/1/user/?school=Keskustan%20koulu&group=7A&changed_at=1444398009``

This returns all matches. The data returned is in the same format as the
Attribute query data, with the exception that only attributes from the querying
user's source are returned.


Data as SAML attributes
=======================

Data coming from Auth Data should be directly visible to all service providers as SAML attributes. There are two attributes:

educloud.oid
  This is same as the username field in the API.
educloud.data
  Contains whole JSON document coming from the API. It is base64 encoded.


Sequence diagram for Educloud Pilot
===================================

.. image:: diagram.png

The sequence diagram shows basic use cases in the Educloud pilot. It begins from a state where the user
is already registered to the central Identity Provider (IdP) which is maintained by the Educloud.

The Django project found in this repository is the Auth Data in the diagram. It provides the database for
the attributes which are returned with SAML assertions to Service Providers (SP). It emulates
the Opintopolku database which is shown in the diagram as optional step. Some day hopefully this Auth Data service 
can be replaced with Opintopolku.

The IdP uses several authentication sources. For example Facebook and other LMS services. These auth sources
all use different identifiers for users. Auth Data converts these identifiers to OppijaIDs or OIDs. OID is
used by all SPs to identify the users. This is made possible by returning the OID in SAML assertions
to SPs when they request authentication.


Other notes
===========

The auth source selection can be made automatic or SP can pre-select it. More info from IdP admins.

The LMS SSO auth source method is a special case. When used like described in the diagram the user is
authenticated from the same LMS which initiated the SAML authentication query. This seems counter-intuitive
but it serves a special purpose: it demonstrates how the system could work when full blown federated SAML
based system is used. Here the LMS implements really simple API which is queried for the user identifier.
It should not actually cause login or open a session to the LMS. It should just show login prompt for the
user, check the credentials, and then return the user identifier to the IdP.

Source for the image
====================

Generated with www.websequencediagrams.com

::

  title Data exchange in Educloud pilot
  
  note left of User
    User has already registered to LMS A and IdP.
    No active session anywhere.
  end note
  
  User ->+ LMS A: Initiate login
  LMS A -> IdP: SAML
  IdP -> User: Ask which source
  User --> IdP: Choice
  
  alt LMS JWT SSO
    IdP -> LMS A: JWT SSO
    LMS A -> User: Login prompt
    User --> LMS A: Credential submit
    note over LMS A: Credential check\nno open session
    LMS A --> IdP: Returns auth info
  else Facebook
    IdP -> Facebook: Auth query
    Facebook -> User: Login prompt
    User --> Facebook: Credential submit
    Facebook --> IdP: Auth info
  end
  
  IdP -> Auth Data: Query attributes
  
  opt New user registration or query data from Opinpolku
    Auth Data -> Opinpolku: Query data
    Opinpolku --> Auth Data: Return data
  end opt
  
  Auth Data --> IdP: Return attributes
  IdP -> LMS A: SAML assertion
  LMS A ->- User: Access granted
  
  note left of User
    User has open session in LMS A and IdP
    Next user buys material from Bazaar
  end note
  
  User ->+ LMS A: Add and assign material
  LMS A ->+ Bazaar: Browse
  Bazaar -> IdP: SAML
  IdP -> Auth Data: Query attributes
  
  opt New user registration or query data from Opinpolku
    Auth Data -> Opinpolku: Query data
    Opinpolku --> Auth Data: Return data
  end opt
  
  Auth Data --> IdP: Return attributes
  IdP --> Bazaar: SAML assertion
  
  note over Bazaar
    Browse and byuing is little sketchy
    Not relevant to this diagram :)
  end note
  
  Bazaar -> User: Show cart
  User --> Bazaar: Accept/Buy cart
  
  Bazaar ->- LMS A: User returns to LMS
  
  LMS A -> Bazaar: Server-to-server query of materials
  Bazaar --> LMS A: List of materials
  
  LMS A ->- User: Material in use
  
  note left of User
    Material is in LMS.
    Session is open in Bazaar.
    Next user opens the material in LMS
    and then uses it in CMS
  end note
  
  User -> LMS A: Open material
  LMS A --> User: Redirect link to CMS
  
  User ->+ CMS: Open material
  CMS -> IdP: SAML
  IdP -> Auth Data: Query attributes
  
  opt New user registration or query data from Opinpolku
    Auth Data -> Opinpolku: Query data
    Opinpolku --> Auth Data: Return data
  end opt
  
  Auth Data --> IdP: Return attributes
  IdP --> CMS: SAML assertion
  
  CMS -> User: Show material
  note over CMS
    Using material is little sketchy
    Not relevant to this diagram :)
  end note
  User --> CMS: Use material
  
  CMS ->- User: All done :)
  
  note left of User
    Lastly user tries to login to another LMS
  end note
  
  User ->+ LMS B: Initiate login
  LMS B -> IdP: SAML
  IdP -> Auth Data: Query attributes
  
  opt New user registration or query data from Opinpolku
    Auth Data -> Opinpolku: Query data
    Opinpolku --> Auth Data: Return data
  end opt
  
  Auth Data --> IdP: Return attributes
  IdP --> LMS B: SAML assertion
  LMS B ->- User: Access denied


