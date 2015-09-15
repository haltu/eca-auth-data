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


from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
import django_filters
from roledb.serializers import QuerySerializer, UserSerializer, AttributeSerializer, UserAttributeSerializer, MunicipalitySerializer, SchoolSerializer, RoleSerializer, AttendanceSerializer
from roledb.models import User, Attribute, UserAttribute, Municipality, School, Role, Attendance


class QueryView(generics.RetrieveAPIView):
  """ Returns information about one user.

  The ``username`` is global unique identifier for the user.

  The ``roles`` is a list of roles the user has in different schools.
  User can have multiple roles in one school.

  Possible values for ``role`` are ``teacher`` and ``student``.

  Query is made by GET parameters. Only one parameter is allowed.

  ``Not found`` is returned if:

  * the parameter name is not recognized
  * multiple results would be returned (only one result is allowed)
  * no parameters are specified
  """
  queryset = User.objects.all()
  serializer_class = QuerySerializer
  lookup_field = 'username'

  def get_object(self):
    qs = self.filter_queryset(self.get_queryset())
    filter_kwargs = {}
    for k,v in self.request.GET.iteritems():
      a = get_object_or_404(Attribute.objects.all(), name=k)
      filter_kwargs['attributes__attribute__name'] = a.name
      filter_kwargs['attributes__value'] = v
      break # only handle one GET variable for now
    else:
      raise Http404
    obj = generics.get_object_or_404(qs, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj


class UserFilter(django_filters.FilterSet):
  school = django_filters.CharFilter(name='attendances__school__name')
  group = django_filters.CharFilter(name='attendances__group')

  class Meta:
    model = User
    fields = ['username', 'school', 'group']


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().distinct()
  serializer_class = UserSerializer
  filter_backends = (filters.DjangoFilterBackend,)
  filter_class = UserFilter


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Attribute.objects.all()
  serializer_class = AttributeSerializer


class UserAttributeViewSet(viewsets.ModelViewSet):
  queryset = UserAttribute.objects.all()
  serializer_class = UserAttributeSerializer


class MunicipalityViewSet(viewsets.ModelViewSet):
  queryset = Municipality.objects.all()
  serializer_class = MunicipalitySerializer


class SchoolViewSet(viewsets.ModelViewSet):
  queryset = School.objects.all()
  serializer_class = SchoolSerializer


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Role.objects.all()
  serializer_class = RoleSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer



