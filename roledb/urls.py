from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from roledb.views import QueryView
from roledb.views import UserViewSet, AttributeViewSet, UserAttributeViewSet, MunicipalityViewSet, SchoolViewSet, RoleViewSet, AttendanceViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'attribute', AttributeViewSet)
router.register(r'userattribute', UserAttributeViewSet)
router.register(r'municipality', MunicipalityViewSet)
router.register(r'school', SchoolViewSet)
router.register(r'role', RoleViewSet)
router.register(r'attendance', AttendanceViewSet)


urlpatterns = patterns('',
    url(r'^api/1/user$', QueryView.as_view()), # This should be removed as "/user" and "/user/" are now different which is confusing. User "/query/" instead
    url(r'^api/1/query$', QueryView.as_view()),
    url(r'^api/1/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
