from django.contrib import admin
from .models import Department, Staff


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'intro']
    search_fields = ['name']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_realname', 'get_email', 'department', 'status', 'join_date']
    list_filter = ['status', 'department']
    search_fields = ['user__realname', 'user__email']

    @admin.display(description='Full Name')
    def get_realname(self, obj):
        return obj.user.realname

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
