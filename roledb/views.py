
from rest_framework import generics
from roledb.serializers import UserSerializer
from roledb.models import User


class UserGetView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'username'


