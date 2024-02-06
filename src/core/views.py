from django.shortcuts import render

from core.models import Bookmark


def disk_to_url(path):
    if path is None:
        return None
    return path.replace("/app/data", "/static")


def process_bookmark(bookmark):
    single_file_html_path = bookmark.single_file_html_path
    media_path = bookmark.media_path

    url = disk_to_url(single_file_html_path)
    media = disk_to_url(media_path)
    title = bookmark.title

    # TODO: both original url and archived url should be shown
    return {"url": url, "media": media, "title": title}


def index(request):
    items = Bookmark.objects.order_by("-created")[:5]
    items = [process_bookmark(item) for item in items]

    context = {"items": items}
    return render(request, "index.html", context)
