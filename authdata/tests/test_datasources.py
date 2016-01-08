
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
# pylint: disable=locally-disabled, no-member, protected-access

import mock
import requests
# from pprint import pprint

from django.test import TestCase
from django.test import RequestFactory
from django.test import override_settings

from authdata import models
from authdata.datasources.base import ExternalDataSource
import authdata.datasources.dreamschool
from authdata.datasources.ldap_base import LDAPDataSource
from authdata.datasources.ldap_base import TestLDAPDataSource as LdapTest
from authdata.datasources.oulu import OuluLDAPDataSource


AUTH_EXTERNAL_SOURCES = {
    'ldap_test': ['authdata.datasources.ldap_base', 'TestLDAPDataSource', {
        'host': 'ldaps://1.2.3.4',
        'username': 'uid=foo,ou=Bar,dc=zap,dc=csc,dc=fi',
        'password': 'password'
    }],
    'dreamschool': ['authdata.datasources.dreamschool', 'DreamschoolDataSource', {
        'api_url': 'https://foo.fi/api/2/user/',
        'username': 'username',
        'password': 'password',
    }],
}
AUTH_EXTERNAL_ATTRIBUTE_BINDING = {
    'ldap_test': 'ldap_test',
    'dreamschool': 'dreamschool',
}
AUTH_EXTERNAL_MUNICIPALITY_BINDING = {
    'Foo': 'ldap_test',
    'Bar': 'dreamschool',
}

AUTHDATA_DREAMSCHOOL_ORG_MAP = {
  u'bar': {u'school1': 3, u'äö school': 1},
}


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


@override_settings(AUTH_EXTERNAL_SOURCES=AUTH_EXTERNAL_SOURCES)
@override_settings(AUTH_EXTERNAL_ATTRIBUTE_BINDING=AUTH_EXTERNAL_ATTRIBUTE_BINDING)
@override_settings(AUTH_EXTERNAL_MUNICIPALITY_BINDING=AUTH_EXTERNAL_MUNICIPALITY_BINDING)
@override_settings(AUTHDATA_DREAMSCHOOL_ORG_MAP=AUTHDATA_DREAMSCHOOL_ORG_MAP)
class TestDreamschoolDataSource(TestCase):

  def setUp(self):
    self.o = authdata.datasources.dreamschool.DreamschoolDataSource(api_url='mock://foo',
        username='foo', password='bar')

    authdata.datasources.dreamschool.requests = mock.Mock()
    authdata.datasources.dreamschool.requests.codes = requests.codes

    data = {'objects': [
      {'id': 123,
      'username': 'user',
      'first_name': 'first',
      'last_name': 'last',
      'roles': [
        {
         'permissions': [{
           'code': authdata.datasources.dreamschool.TEACHER_PERM,
         }],
         'organisation': {'id': 1},
        },
      ],
      'user_groups': [
        {
          'organisation': {
              'id': 1,
              'title': 'Äö school',
          },
          'title': 'Group1',
        },
      ],
      }]
    }
    self.data = data

    response_mock = mock.Mock()
    response_mock.status_code = requests.codes.ok
    response_mock.json.return_value = data

    authdata.datasources.dreamschool.requests.get.return_value = response_mock
    self.factory = RequestFactory()

  def test_init(self):
    self.assertTrue(self.o)

  def test_oid(self):
    oid = self.o.get_oid(username='foo')
    self.assertTrue(oid.startswith('MPASSOID'))
    self.assertEqual(len(oid), 30)

  def test_user_data(self):
    d = {'municipality': 'Bar', 'school': 'school1', 'group': 'Group1'}
    request = self.factory.get('/foo', d)

    data = self.o.get_user_data(request=request)
    self.assertEqual(data['count'], 1)
    self.assertEqual(data['next'], None)
    self.assertEqual(data['previous'], None)
    self.assertEqual(data['results'][0]['attributes'], [])
    self.assertEqual(data['results'][0]['first_name'], 'first')
    self.assertEqual(data['results'][0]['last_name'], 'last')
    self.assertEqual(data['results'][0]['username'], 'MPASSOID.ea5f9ca03f6edf5a0409d')
    roles = list(data['results'][0]['roles'])
    expected_roles = [
      {
        'school': 'Äö school',
        'role': 'teacher',
        'group': 'Group1',
        'municipality': u'Bar'
      },
    ]
    self.assertEqual(roles, expected_roles)

  def test_user_data_api_fail(self):
    response_mock = mock.Mock()
    response_mock.status_code = 500
    response_mock.json.return_value = self.data
    authdata.datasources.dreamschool.requests.get.return_value = response_mock

    d = {'municipality': 'Bar', 'school': 'school1', 'group': 'Group1'}
    request = self.factory.get('/foo', d)

    data = self.o.get_user_data(request=request)
    self.assertEqual(data['count'], 0)
    self.assertEqual(data['next'], None)
    self.assertEqual(data['previous'], None)
    self.assertEqual(data['results'], [])

  def test_user_data_api_parse_json_fail(self):
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.json.side_effect = ValueError('foo')
    authdata.datasources.dreamschool.requests.get.return_value = response_mock

    d = {'municipality': 'Bar', 'school': 'school1', 'group': 'Group1'}
    request = self.factory.get('/foo', d)

    data = self.o.get_user_data(request=request)
    self.assertEqual(data['count'], 0)
    self.assertEqual(data['next'], None)
    self.assertEqual(data['previous'], None)
    self.assertEqual(data['results'], [])

  def test_get_municipality_by_org_id(self):
    org_id = 1
    municipality = self.o._get_municipality_by_org_id(org_id)
    self.assertEqual(municipality, u'Bar')

  @override_settings(AUTHDATA_DREAMSCHOOL_ORG_MAP={})
  def test_get_municipality_by_org_id_not_in_settings(self):
    org_id = 1
    municipality = self.o._get_municipality_by_org_id(org_id)
    self.assertEqual(municipality, u'')

  def test_get_roles_from_userdata_student(self):
    userdata = {
        'roles': [
          {
           'permissions': [{'code': 'foo'}],
           'organisation': {'id': 1},
          },
        ],
        'user_groups': [
          {
            'organisation': {
                'id': 1,
                'title': 'Äö school',
            },
            'title': 'Group1',
          },
        ],
    }
    roles = list(self.o._get_roles(userdata))
    expected_roles = [
      {
          "school": "Äö school",
          "role": "student",
          "group": "Group1",
          "municipality": u"Bar"
      },
    ]
    self.assertEqual(roles, expected_roles)

  def test_get_roles_from_userdata_teacher(self):
    userdata = {
        'roles': [
          {
           'permissions': [{
             'code': authdata.datasources.dreamschool.TEACHER_PERM,
           }],
           'organisation': {'id': 1},
          },
        ],
        'user_groups': [
          {
            'organisation': {
                'id': 1,
                'title': 'Äö school',
            },
            'title': 'Group1',
          },
        ],
    }
    roles = list(self.o._get_roles(userdata))
    expected_roles = [
      {
        'school': 'Äö school',
        'role': 'teacher',
        'group': 'Group1',
        'municipality': u'Bar'
      },
    ]
    self.assertEqual(roles, expected_roles)

  def test_get_org_id_not_configured(self):
    municipality = ''
    school = ''
    self.assertFalse(self.o._get_org_id(municipality, school))

  def test_get_org_id(self):
    municipality = u'Bar'
    school = u'äö school'
    expected_org_id = 1
    org_id = self.o._get_org_id(municipality=municipality, school=school)
    self.assertEqual(org_id, expected_org_id)

    municipality = u'Foo'
    school = u'äö school'
    org_id = self.o._get_org_id(municipality=municipality, school=school)
    self.assertEqual(org_id, None)

    municipality = u'Bar'
    school = u'school1'
    expected_org_id = 3
    org_id = self.o._get_org_id(municipality=municipality, school=school)
    self.assertEqual(org_id, expected_org_id)

  def test_get_data(self):
    external_id = '123'
    data = {
        'id': 123,
        'username': 'User',
        'first_name': 'First',
        'last_name': 'Last',
        'roles': [
          {
           'permissions': [{
             'code': authdata.datasources.dreamschool.TEACHER_PERM,
           }],
           'organisation': {'id': 1},
          },
        ],
        'user_groups': [
          {
            'organisation': {
                'id': 1,
                'title': 'Äö school',
            },
            'title': 'Group1',
          },
        ],
    }
    response_mock = mock.Mock()
    response_mock.status_code = requests.codes.ok
    response_mock.json.return_value = data

    authdata.datasources.dreamschool.requests.get.return_value = response_mock
    data = self.o.get_data(external_id=external_id)
    data['roles'] = list(data['roles'])
    expected_data = {
      'attributes': [],
      'username': 'MPASSOID.08153889bda7b8ffd5a4d',
      'first_name': 'First',
      'last_name': 'Last',
      'roles': [{
        'school': 'Äö school',
        'role': 'teacher',
        'group': 'Group1',
        'municipality': u'Bar'
      }],
    }
    self.assertEqual(data, expected_data)

  def test_get_data_api_fail(self):
    external_id = '123'
    data = {
        'id': 123,
        'username': 'User',
        'first_name': 'First',
        'last_name': 'Last',
        'roles': [
          {
           'permissions': [{
             'code': authdata.datasources.dreamschool.TEACHER_PERM,
           }],
           'organisation': {'id': 1},
          },
        ],
        'user_groups': [
          {
            'organisation': {
                'id': 1,
                'title': 'Äö school',
            },
            'title': 'Group1',
          },
        ],
    }
    response_mock = mock.Mock()
    response_mock.status_code = 500
    response_mock.json.return_value = data

    authdata.datasources.dreamschool.requests.get.return_value = response_mock
    data = self.o.get_data(external_id=external_id)
    self.assertEqual(data, None)

  def test_get_data_json_parse_fail(self):
    external_id = '123'
    data = {
        'id': 123,
        'username': 'User',
        'first_name': 'First',
        'last_name': 'Last',
        'roles': [
          {
           'permissions': [{
             'code': authdata.datasources.dreamschool.TEACHER_PERM,
           }],
           'organisation': {'id': 1},
          },
        ],
        'user_groups': [
          {
            'organisation': {
                'id': 1,
                'title': 'Äö school',
            },
            'title': 'Group1',
          },
        ],
    }
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.json.side_effect = ValueError('foo')

    authdata.datasources.dreamschool.requests.get.return_value = response_mock
    data = self.o.get_data(external_id=external_id)
    self.assertEqual(data, None)


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

