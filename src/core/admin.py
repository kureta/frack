from django.contrib import admin

from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    fields = ["url", "created", "scrape_status", "title", "single_file_html_path", "media_path"]
    readonly_fields = ["title", "created", "scrape_status", "single_file_html_path", "media_path"]


admin.site.register(Bookmark, BookmarkAdmin)
