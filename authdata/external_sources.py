
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

import hashlib
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

  municipality_id_map = {
    'KuntaYksi': '1234567-8'
  }

  class _schoolid_generator():
    """
    generator for fake school ids
    """
    @classmethod
    def get(cls, name, default=None):
      import string
      num = name.strip(string.ascii_letters)
      num = int(num)
      return '%05d' % num

  school_id_map = _schoolid_generator

  #'LdapKoulu1': '00001',
  #'LdapKoulu2': '00002',
  #'LdapKoulu3': '00003',
  #'LdapKoulu4': '00004',
  #'LdapKoulu5': '00005',
  #'LdapKoulu6': '00006',
  #'LdapKoulu7': '00007',
  #'LdapKoulu8': '00008',
  #'LdapKoulu9': '00009',
  #'LdapKoulu10': '00010',
  #'LdapKoulu11': '00011',
  # etc...

  def __init__(self, *args, **kwargs):
    self.ldap_base_dn = 'ou=KuntaYksi,dc=mpass-test,dc=csc,dc=fi'
    self.ldap_filter = "(&(uid={value})(objectclass=inetOrgPerson))"
    """
    ldap_filter = Filter for finding the required user in an LDAP query,
                  for example "(&(attribute={value})(objectclass=inetOrgPerson))"
                  Query will substitue {value} with Auth Proxy's attribute query value.
    """
    super(TestLDAPDataSource, self).__init__(*args, **kwargs)

  def get_oid(self, username):
    """
    There is no OID information in this external source. Generate fake OID
    from username.
    """
    return 'MPASSOID.%s' % hashlib.sha1('ldap_test' + username).hexdigest()

  def get_data(self, attribute, value):
    query_result = self.query(self.ldap_filter.format(value=value))[0]
    dn_parts = query_result[0].split(',')
    username = query_result[1]['cn'][0]
    first_name = query_result[1]['givenName'][0]
    last_name = query_result[1]['sn'][0]
    attributes = [{
      'name': attribute,
      'value': value
    }]
    roles = [{
      'school': dn_parts[3].strip("ou="),
      'role': query_result[1]['title'][0],
      'municipality': dn_parts[4].strip("ou="),
      'group': query_result[1].get('departmentNumber', [''])[0]
    }]
    return {
      'username': self.get_oid(username),
      'first_name': first_name,
      'last_name': last_name,
      'roles': roles,
      'attributes': attributes
    }

  def get_user_data(self, request):
    ldap_filter = "objectclass=inetOrgPerson"
    query_base = self.ldap_base_dn
    if 'school' in request.GET:
      self.ldap_base_dn = 'ou=%s,%s' % (request.GET['school'], query_base)
    if 'group' in request.GET and request.GET['group'] != '':
      ldap_filter = '(&(departmentNumber=%s)(%s))' % (request.GET['group'], ldap_filter)
    print "query_base", self.ldap_base_dn, "ldap_filter", ldap_filter
    query_results = self.query(ldap_filter)
    response = []

    for result in query_results:
      dn_parts = result[0].split(',')
      username = result[1]['cn'][0]
      first_name = result[1]['givenName'][0]
      last_name = result[1]['sn'][0]
      attributes = [
        # TODO: what attributes should be returned from LDAP?
      ]
      roles = [{
        'school': self.get_school_id(dn_parts[3].strip("ou=")),
        'role': result[1]['title'][0],
        'municipality': self.get_municipality_id(dn_parts[4].strip("ou=")),
        'group': result[1].get('departmentNumber', [''])[0]
      }]
      response.append({
        'username': self.get_oid(username),
        'first_name': first_name,
        'last_name': last_name,
        'roles': roles,
        'attributes': attributes
      })
    # TODO: support actual paging via SimplePagedResultsControl

    return {
      'count': len(response),
      'next': None,
      'previous': None,
      'results': response,
    }

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

