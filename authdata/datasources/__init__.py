
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


"""
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
:py:class:`authdata.datasources.base.ExternalDataSource` which must be inherited
by external data source implementations.

External sources are configured in Auth Data settings.

In user list query :py:class:`authdata.views.UserViewSet` the municipality
search term is used to forward the query to the external source implementation.

In the attribute query :py:class:`authdata.views.QueryView` Auth Data finds the
user in it's local database based on attribute or username the local User
object contains the external source name and external source unique id which
are used for querying the actual user data from the source.
"""

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

