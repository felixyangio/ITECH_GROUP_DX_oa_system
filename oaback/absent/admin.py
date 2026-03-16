from django.contrib import admin
from .models import AbsentType, Absent


@admin.register(AbsentType)
class AbsentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Absent)
class AbsentAdmin(admin.ModelAdmin):
    list_display = ['id', 'applicant', 'absent_type', 'start_date', 'end_date', 'status', 'create_time']
    list_filter = ['status', 'absent_type']
    search_fields = ['applicant__realname', 'applicant__email']
