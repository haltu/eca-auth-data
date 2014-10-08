
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
  name = models.ForeignKey(Attribute)
  value = models.CharField(max_length=2048, blank=True, null=True, default=None)

  def __unicode__(self):
    return "%s: %s" % (self.name, self.value)


class Role(models.Model):
  name = models.CharField(max_length=2048)

  def __unicode__(self):
    return self.name


class UserRole(models.Model):
  role = models.ForeignKey(Role)
  school = models.ForeignKey(School, related_name='users')
  user = models.ForeignKey(User, related_name='roles')

  def __unicode__(self):
    return "%s: %s / %s" % (self.role, self.school.name, self.school.municipality.name)


class Service(models.Model):
  name = models.CharField(max_length=2048)
  roles = models.ManyToManyField(School, related_name='services')


