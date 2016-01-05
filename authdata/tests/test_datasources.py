
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
# pylint: disable=locally-disabled, no-member

import mock
import requests

from django.test import TestCase
from django.test import RequestFactory

from authdata import models
from authdata.datasources.base import ExternalDataSource
import authdata.datasources.dreamschool_source
from authdata.datasources.ldap_base import LDAPDataSource
from authdata.datasources.ldap_sources import TestLDAPDataSource as LdapTest
from authdata.datasources.ldap_sources import OuluLDAPDataSource


class TestExternalDataSource(TestCase):

  def setUp(self):
    self.o = ExternalDataSource()

  def test_init(self):
    self.assertTrue(self.o)

  def test_provision_user(self):
    obj = self.o
    obj.external_source = 'foo'
    obj.provision_user(oid='oid', external_id='foo')
    self.assertEqual(models.User.objects.filter(username='oid').count(), 1)
    self.assertEqual(models.Source.objects.filter(name='local').count(), 1)
    self.assertEqual(models.Attribute.objects.count(), 1)
    self.assertEqual(models.UserAttribute.objects.count(), 1)

  def test_oid(self):
    with self.assertRaises(NotImplementedError):
      self.o.get_oid(username='foo')

  def test_data(self):
    with self.assertRaises(NotImplementedError):
      self.o.get_data(external_id='foo')

  def test_user_data(self):
    with self.assertRaises(NotImplementedError):
      self.o.get_user_data(request='foo')


class TestDreamschoolDataSource(TestCase):

  def setUp(self):
    self.o = authdata.datasources.dreamschool_source.DreamschoolDataSource(api_url='mock://foo',
        username='foo', password='bar')

    authdata.datasources.dreamschool_source.requests = mock.Mock()
    authdata.datasources.dreamschool_source.requests.codes = requests.codes

    data = {'objects': [
      {'id': 123,
      'username': 'user',
      'first_name': 'first',
      'last_name': 'last'}]}

    response_mock = mock.Mock()
    response_mock.status_code = requests.codes.ok
    response_mock.json.return_value = data

    authdata.datasources.dreamschool_source.requests.get.return_value = response_mock
    self.factory = RequestFactory()

  def test_init(self):
    self.assertTrue(self.o)

  def test_oid(self):
    oid = self.o.get_oid(username='foo')
    self.assertTrue(oid.startswith('MPASSOID'))

  def test_user_data(self):
    d = {'municipality': 'muni'}
    request = self.factory.get('/foo', d)
    self.o.get_user_data(request=request)


class TestLDAPDataSource(TestCase):

  def test_init(self):
    obj = LDAPDataSource(host='host', username='foo', password='bar')
    self.assertTrue(obj)


class TestLdapTest(TestCase):

  def test_init(self):
    obj = LdapTest(host='host', username='foo', password='bar')
    self.assertTrue(obj)


class TestOuluLDAPDataSource(TestCase):

  def test_init(self):
    obj = OuluLDAPDataSource(host='host', username='foo', password='bar', base_dn='foo')
    self.assertTrue(obj)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

