
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

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from authdata import views
from authdata.tests.factories import UserFactory


class TestQueryView(APITestCase):

  def setUp(self):
    self.request_factory = APIRequestFactory()
    self.user = UserFactory.create()

  def test_get_user_does_not_exist(self):
    request = self.request_factory.get('/api/1/users')
    force_authenticate(request, user=self.user)
    view = views.QueryView.as_view()

    response = view(request, username='foo')

    self.assertEqual(response.status_code, 404)

  def test_get_user_exists(self):
    request = self.request_factory.get('/api/1/users')
    force_authenticate(request, user=self.user)
    view = views.QueryView.as_view()

    UserFactory.create(username='foo')
    response = view(request, username='foo')

    self.assertEqual(response.status_code, 200)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

