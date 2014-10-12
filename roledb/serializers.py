
from rest_framework import serializers
from roledb.models import User


class UserSerializer(serializers.ModelSerializer):
  roles = serializers.SerializerMethodField('role_data')

  class Meta:
    model = User
    fields = ('username', 'roles')

  def role_data(self, obj):
    data = []
    for a in obj.attendances.all():
      d = {}
      d['school'] = a.school.school_id
      d['group'] = a.group
      d['role'] = a.role.name
      data.append(d)
    return data


