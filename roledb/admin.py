
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from roledb.models import Municipality, School, Role, UserRole, Service, User, Attribute, UserAttribute

class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'school')
    list_filter = ('role',)
    search_fields = ('school__name', 'user__username')


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserAttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value')
    list_filter = ('name',)
    search_fields = ('user__username',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserAttributeInline(admin.TabularInline):
    model = UserAttribute
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
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [UserAttributeInline]    


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(UserAttribute, UserAttributeAdmin)

