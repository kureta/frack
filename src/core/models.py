from pathlib import Path
from django.db import models

from core.tasks import get_controller

SCRAPE_STATUS_CHOICES = [
    ("Initial", "Initial"),
    ("Scraping", "Scraping"),
    ("Scraped", "Scraped"),
    ("Failed", "Failed"),
    ("Disabled", "Disabled"),
]


class Bookmark(models.Model):
    # Only URL will be set by the user
    url = models.URLField(unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    scrape_status = models.CharField(max_length=16, choices=SCRAPE_STATUS_CHOICES, default="Initial")
    media_status = models.CharField(max_length=16, choices=SCRAPE_STATUS_CHOICES, default="Initial")

    title = models.CharField(max_length=100, null=True, db_index=True)
    single_file_html_path = models.FilePathField(max_length=256, path="/", recursive=True, null=True)
    media_path = models.FilePathField(max_length=256, path="/", recursive=True, null=True)

    def __str__(self):
        if self.title is not None:
            return self.title
        return self.url

    def save(self, *args, **kwargs):
        celery = get_controller()
        if self.scrape_status == "Initial":
            celery.send_task('scrape_page', args=[self.url])
            self.scrape_status = "Scraping"
        if self.media_status == "Initial":
            celery.send_task('get_media', args=[self.url])
            self.media_status = "Scraping"

        if self.title is None:
            self.title = self.url
            self.title = self.title[:100]

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        if self.single_file_html_path is not None:
            # TODO: there might be multiple htmls from different dates
            Path(self.single_file_html_path).unlink(missing_ok=True)
        if self.media_path is not None:
            Path(self.media_path).unlink(missing_ok=True)


class Media(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    path = models.FilePathField(max_length=256, path="/", recursive=True)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.url