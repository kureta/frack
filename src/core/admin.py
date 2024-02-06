from django.contrib import admin

from .models import Bookmark


# TODO: edit columns shown in the table view
class BookmarkAdmin(admin.ModelAdmin):
    fields = [
        "url",
        "created",
        "scrape_status",
        "title",
        "single_file_html_path",
        "media_path",
        "media_status",
    ]
    readonly_fields = [
        "title",
        "created",
        "scrape_status",
        "single_file_html_path",
        "media_path",
        "media_status",
    ]

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Bookmark, BookmarkAdmin)
