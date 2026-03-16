from django.contrib import admin
from .models import Inform, InformRead


@admin.register(Inform)
class InformAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'is_top', 'create_time']
    list_filter = ['is_top']
    search_fields = ['title', 'author__realname']


@admin.register(InformRead)
class InformReadAdmin(admin.ModelAdmin):
    list_display = ['id', 'inform', 'reader', 'read_time']
