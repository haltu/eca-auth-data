# -*- encoding: utf-8 -*-

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


from rest_framework import serializers
from roledb.models import User, Attribute, UserAttribute, Municipality, School, Role, Attendance, Source


class QuerySerializer(serializers.ModelSerializer):
  roles = serializers.SerializerMethodField('role_data')
  attributes = serializers.SerializerMethodField('attribute_data')

  class Meta:
    model = User
    fields = ('username','first_name','last_name','roles','attributes')

  def role_data(self, obj):
    data = []
    for a in obj.attendances.all():
      d = {}
      d['school'] = a.school.school_id
      d['group'] = a.group
      d['role'] = a.role.name
      data.append(d)
    return data

  def attribute_data(self, obj):
    data = []
    for a in obj.attributes.all():
      d = {}
      d['name'] = a.attribute.name
      d['value'] = a.value
      data.append(d)
    return data


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    lookup_field = 'username'
    fields = ('username', 'first_name', 'last_name')


class AttributeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attribute
    lookup_field = 'name'


class UserAttributeSerializer(serializers.ModelSerializer):
  data_source = serializers.PrimaryKeyRelatedField(read_only=True)
  attribute = serializers.SlugRelatedField(slug_field='name', queryset=Attribute.objects.all())
  user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

  class Meta:
    model = UserAttribute

  def save(self, *args, **kwargs):
    username = self.context['request'].user.username
    data_source_obj, _ = Source.objects.get_or_create(name=username)
    self.object.data_source = data_source_obj
    return super(UserAttributeSerializer, self).save(*args, **kwargs)


class MunicipalitySerializer(serializers.ModelSerializer):
  data_source = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Municipality

  def save(self, *args, **kwargs):
    username = self.context['request'].user.username
    data_source_obj, _ = Source.objects.get_or_create(name=username)
    self.object.data_source = data_source_obj
    return super(MunicipalitySerializer, self).save(*args, **kwargs)


class SchoolSerializer(serializers.ModelSerializer):
  data_source = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = School

  def save(self, *args, **kwargs):
    username = self.context['request'].user.username
    data_source_obj, _ = Source.objects.get_or_create(name=username)
    self.object.data_source = data_source_obj
    return super(SchoolSerializer, self).save(*args, **kwargs)


class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role


class AttendanceSerializer(serializers.ModelSerializer):
  data_source = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Attendance

  def save(self, *args, **kwargs):
    username = self.context['request'].user.username
    data_source_obj, _ = Source.objects.get_or_create(name=username)
    self.object.data_source = data_source_obj
    return super(AttendanceSerializer, self).save(*args, **kwargs)

