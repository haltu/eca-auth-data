
from rest_framework import serializers
from roledb.models import User


class UserSerializer(serializers.ModelSerializer):
  roles = serializers.RelatedField(many=True)

  class Meta:
    model = User
    fields = ('username', 'roles')


