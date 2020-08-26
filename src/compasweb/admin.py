from django.contrib import admin

from .models import COMPASJob, Keyword

@admin.register(COMPASJob)
class COMPASJobAdmin(admin.ModelAdmin):
    pass

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass
