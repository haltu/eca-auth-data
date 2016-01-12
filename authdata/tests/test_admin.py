
# -*- coding: utf-8 -*-

from mock import Mock
from django.test import TestCase
from authdata import admin


class TestAdmin(TestCase):

  def test_municipality(self):
    obj = admin.MunicipalityAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_school(self):
    obj = admin.SchoolAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_attendance(self):
    obj = admin.AttendanceAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_attribute(self):
    obj = admin.AttributeAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_userattribute(self):
    obj = admin.UserAttributeAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_source(self):
    obj = admin.SourceAdmin(Mock(), Mock())
    self.assertTrue(obj)

  def test_user(self):
    obj = admin.UserAdmin(Mock(), Mock())
    self.assertTrue(obj)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

