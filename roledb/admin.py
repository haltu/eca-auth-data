
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from roledb.forms import UserCreationForm, UserChangeForm
from roledb.models import Municipality
from roledb.models import School
from roledb.models import Role
from roledb.models import Attendance
from roledb.models import Source
from roledb.models import User
from roledb.models import Attribute
from roledb.models import UserAttribute


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'role', 'group', 'data_source')
    list_filter = ('role', 'data_source')
    search_fields = ('school__school_id', 'school__name', 'school__municipality__name', 'user__username', 'group',)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserAttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('user__username', 'value')


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserAttributeInline(admin.TabularInline):
    model = UserAttribute
    extra = 0


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [UserAttributeInline, AttendanceInline]
    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(UserAttribute, UserAttributeAdmin)

