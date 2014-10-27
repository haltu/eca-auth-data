
from rest_framework import serializers
from roledb.models import User, Attribute, UserAttribute, Municipality, School, Role, Attendance


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
    fields = ('username', 'first_name', 'last_name')


class AttributeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attribute


class UserAttributeSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAttribute


class MunicipalitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Municipality


class SchoolSerializer(serializers.ModelSerializer):
  class Meta:
    model = School


class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role


class AttendanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attendance


