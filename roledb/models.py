
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Source(models.Model):
  name = models.CharField(max_length=2048)

  def __unicode__(self):
    return self.name


class Municipality(models.Model):
  name = models.CharField(max_length=2048)

  def __unicode__(self):
    return self.name


class School(models.Model):
  name = models.CharField(max_length=2048)
  school_id = models.CharField(max_length=2048)
  municipality = models.ForeignKey(Municipality, related_name='schools')

  def __unicode__(self):
    return "%s / %s" % (self.name, self.municipality)


class User(AbstractUser):
  pass


class Attribute(models.Model):
  name = models.CharField(max_length=2048, blank=True, null=True, default=None)

  def __unicode__(self):
    return self.name


class UserAttribute(models.Model):
  user = models.ForeignKey(User, related_name='attributes')
  attribute = models.ForeignKey(Attribute)
  value = models.CharField(max_length=2048, blank=True, null=True, default=None)
  source = models.ForeignKey(Source)

  def __unicode__(self):
    return "%s: %s" % (self.attribute, self.value)


class Role(models.Model):
  name = models.CharField(max_length=2048)

  def __unicode__(self):
    return self.name


class Attendance(models.Model):
  user = models.ForeignKey(User, related_name='attendances')
  school = models.ForeignKey(School, related_name='users')
  role = models.ForeignKey(Role)
  group = models.CharField(max_length=2048, blank=True, default='')
  source = models.ForeignKey(Source, related_name='attendances')

  def __unicode__(self):
    return "%s: %s / %s" % (self.role, self.school.name, self.school.municipality.name)


