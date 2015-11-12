
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


import ldap
from authdata.models import ExternalDataSource


class LDAPDataSource(ExternalDataSource):
  """
  Abstract base class for implementing external LDAP data sources.

  Implementations must provide values for:
    ldap_server: address of the server
    ldap_username: name for binding
    ldap_password: password for binding
    ldap_base_dn: base distinguished name for the queries

  KWARGS dictionary in configuration should be in the format:
    {
      'host': connection string for ldap server,
      'username': name to bind as,
      'password': password
    }
  """
  ldap_server = None
  ldap_username = None
  ldap_password = None
  ldap_base_dn = None

  connection = None

  def __init__(self, host, username, password, *args, **kwargs):
    self.ldap_server = host
    self.ldap_username = username
    self.ldap_password = password
    super(LDAPDataSource, self).__init__(*args, **kwargs)

  def connect(self):
    """
    Initialize connection the the LDAP server.
    After this method is executed, self.connection is ready for executing
    queries.
    """
    # TODO: error handling
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    self.connection = ldap.initialize(self.ldap_server)
    self.connection.set_option(ldap.OPT_REFERRALS, 0)
    self.connection.simple_bind_s(self.ldap_username, self.ldap_password)

  def query(self, query_filter):
    """
    query ldap with the provided filter string
    """
    if not self.connection:
      self.connect()
    # TODO: LDAP error handling
    # TODO: must get exactly one result
    return self.connection.search_s(self.ldap_base_dn, filterstr=query_filter, scope=ldap.SCOPE_SUBTREE)[0]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

