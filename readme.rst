
Role database for EduCloud
**************************

The purpose of the RoleDB is to emulate national centralized Opintopolku database.

.. image:: diagram.png

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
  
  IdP -> RoleDB: Query attributes
  
  opt New user registration or query data from Opinpolku
    RoleDB -> Opinpolku: Query data
    Opinpolku --> RoleDB: Return data
  end opt
  
  RoleDB --> IdP: Return attributes
  IdP -> LMS A: SAML assertion
  LMS A ->- User: Access granted
  
  note left of User
    User has open session in LMS A and IdP
    Next user buys material from Bazaar
  end note
  
  User ->+ LMS A: Add and assign material
  LMS A ->+ Bazaar: Browse
  Bazaar -> IdP: SAML
  IdP -> RoleDB: Query attributes
  
  opt New user registration or query data from Opinpolku
    RoleDB -> Opinpolku: Query data
    Opinpolku --> RoleDB: Return data
  end opt
  
  RoleDB --> IdP: Return attributes
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
  IdP -> RoleDB: Query attributes
  
  opt New user registration or query data from Opinpolku
    RoleDB -> Opinpolku: Query data
    Opinpolku --> RoleDB: Return data
  end opt
  
  RoleDB --> IdP: Return attributes
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
  IdP -> RoleDB: Query attributes
  
  opt New user registration or query data from Opinpolku
    RoleDB -> Opinpolku: Query data
    Opinpolku --> RoleDB: Return data
  end opt
  
  RoleDB --> IdP: Return attributes
  IdP --> LMS B: SAML assertion
  LMS B ->- User: Access denied


