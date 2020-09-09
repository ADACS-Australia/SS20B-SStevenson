from django.contrib import admin

from .models import COMPASJob, Keyword, Upload

@admin.register(COMPASJob)
class COMPASJobAdmin(admin.ModelAdmin):
    list_display = ('dataset_info', 'dataset_keywords',)
    search_fields = ['title', 'year', 'journal', 'author', 'keywords__tag']

    def dataset_info(self, obj):
        return f"{obj.author} - {obj.title} - {obj.journal} {obj.year}"
    dataset_info.short_description = "Dataset"

    def dataset_keywords(self, obj):
        return (", ".join([keyword.tag for keyword in obj.keywords.all()]))
    dataset_keywords.short_description = 'Tags'


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    pass
