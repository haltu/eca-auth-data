
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Haltu Oy, http://haltu.fi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
External data source implementations
"""

from external_ldap.source import LDAPDataSource


class TestLDAPDataSource(LDAPDataSource):
  """
  Example result from test_ldap

   ('cn=bar,ou=Opettajat,ou=People,ou=LdapKoulu1,ou=KuntaYksi,dc=mpass-test,dc=csc,dc=fi',
    {'cn': ['bar'],
     'givenName': ['Ldap'],
     'mail': ['bar@mpass-test.invalid'],
     'objectClass': ['top', 'inetOrgPerson'],
     'sn': ['Opettaja10013'],
     'title': ['Opettaja'],
     'uid': ['bar'],
     'userPassword': ['foo']})

   ('cn=bar,ou=Oppilaat,ou=People,ou=LdapKoulu1,ou=KuntaYksi,dc=mpass-test,dc=csc,dc=fi',
    {'cn': ['bar'],
     'departmentNumber': ['6C'],
     'givenName': ['Ldap'],
     'mail': ['bar@mpass-test.invalid'],
     'objectClass': ['top', 'inetOrgPerson'],
     'sn': ['Oppilas352'],
     'title': ['Oppilas'],
     'uid': ['bar'],
     'userPassword': ['foo']}),

  """

  def __init__(self, *args, **kwargs):
    self.ldap_base_dn = 'ou=KuntaYksi,dc=mpass-test,dc=csc,dc=fi'
    self.ldap_filter = "(&(uid={value})(objectclass=inetOrgPerson))"
    """
    ldap_filter = Filter for finding the required user in an LDAP query,
                  for example "(&(attribute={value})(objectclass=inetOrgPerson))"
                  Query will substitue {value} with Auth Proxy's attribute query value.
    """
    super(TestLDAPDataSource, self).__init__(*args, **kwargs)

  def get_data(self, attribute, value):
    query_result = self.query(self.ldap_filter.format(value=value))
    dn_parts = query_result[0].split(',')
    username = query_result[1]['cn'][0]
    first_name = query_result[1]['givenName'][0]
    last_name = query_result[1]['sn'][0]
    attributes = [{
      attribute: value
    }]
    roles = [{
      'school': dn_parts[3].strip("ou="),
      'role': query_result[1]['title'][0],
      'municipality': dn_parts[4].strip("ou="),
      'group': query_result[1].get('departmentNumber', [''])[0]
    }]
    return {
      'username': username,
      'first_name': first_name,
      'last_name': last_name,
      'roles': roles,
      'attributes': attributes
    }


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

