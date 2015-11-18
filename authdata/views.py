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


import datetime
import importlib
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from django.conf import settings
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
import django_filters
from authdata.serializers import QuerySerializer, UserSerializer, AttributeSerializer, UserAttributeSerializer, MunicipalitySerializer, SchoolSerializer, RoleSerializer, AttendanceSerializer
from authdata.models import User, Attribute, UserAttribute, Municipality, School, Role, Attendance


class QueryView(generics.RetrieveAPIView):
  """ Returns information about one user.

  The ``username`` is global unique identifier for the user.

  The ``roles`` is a list of roles the user has in different schools.
  User can have multiple roles in one school.

  Possible values for ``role`` are ``teacher`` and ``student``.

  Query is made by GET parameters. Only one parameter is allowed. The parameter
  consists of an attribute name and an attribute value.

  ``Not found`` is returned if:

  * the parameter name is not recognized
  * multiple results would be returned (only one result is allowed)
  * no parameters are specified
  """
  queryset = User.objects.all()
  serializer_class = QuerySerializer
  lookup_field = 'username'

  def get(self, request, *args, **kwargs):
    for attr in request.GET.keys():
      if attr in settings.AUTH_EXTERNAL_ATTRIBUTE_BINDING:
        source = settings.AUTH_EXTERNAL_SOURCES[settings.AUTH_EXTERNAL_ATTRIBUTE_BINDING[attr]]
        try:
          handler_module = importlib.import_module(source[0])
          handler = getattr(handler_module, source[1])(**source[2])
          return Response(handler.get_data(attr, request.GET.get(attr)))
        except ImportError as e:
          # TODO: log this, error handling
          # flow back to normal implementation most likely return empty
          pass

    return super(QueryView, self).get(request, *args, **kwargs)

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
  municipality = django_filters.CharFilter(name='attendances__school__municipality__name', lookup_type='iexact')
  school = django_filters.CharFilter(name='attendances__school__name', lookup_type='iexact')
  group = django_filters.CharFilter(name='attendances__group', lookup_type='iexact')
  changed_at = django_filters.MethodFilter(action='timestamp_filter')

  def timestamp_filter(self, queryset, value):
    # TODO: this is unaware of removed UserAttributes
    try:
      tstamp = datetime.datetime.fromtimestamp(float(value))
    except ValueError:
      return queryset.none()
    by_user = Q(modified__gte=tstamp)
    by_user_attribute = Q(attributes__modified__gte=tstamp)
    by_attribute_name = Q(attributes__attribute__modified__gte=tstamp)
    by_attendance = Q(attendances__modified__gte=tstamp)
    by_role_name = Q(attendances__role__modified__gte=tstamp)
    # SELECT DISTINCT ON ("authdata_user"."id") - makes this query perform a lot faster,
    # but is ONLY compatible with PostgreSQL!
    return queryset.filter(by_user | by_user_attribute | by_attribute_name | by_attendance | by_role_name).distinct('id')

  class Meta:
    model = User
    fields = ['username', 'school', 'group', 'changed_at']


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all().distinct()
  serializer_class = UserSerializer
  filter_backends = (filters.DjangoFilterBackend,)
  filter_class = UserFilter

  def list(self, request, *args, **kwargs):
    print request.GET
    if 'municipality' in request.GET and request.GET['municipality'].lower() in [binding_name.lower() for binding_name in settings.AUTH_EXTERNAL_MUNICIPALITY_BINDING.keys()]:
      for binding_name, binding in settings.AUTH_EXTERNAL_MUNICIPALITY_BINDING.iteritems():
        if binding_name.lower() == request.GET['municipality'].lower():
          source = settings.AUTH_EXTERNAL_SOURCES[binding]
      try:
        handler_module = importlib.import_module(source[0])
        handler = getattr(handler_module, source[1])(**source[2])
        return Response(handler.get_user_data(request))
      except ImportError as e:
        # TODO: log this, error handling
        # flow back to normal implementation most likely return empty
        pass

    return super(UserViewSet, self).list(request, *args, **kwargs)


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



