from django.db import models

SCRAPE_STATUS_CHOICES = [
    ("Scraping", "Scraping"),
    ("Scraped", "Scraped"),
    ("Failed", "Failed"),
    ("Disabled", "Disabled"),
]


class Bookmark(models.Model):
    # Only URL will be set by the user
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    scrape_status = models.CharField(max_length=100, choices=SCRAPE_STATUS_CHOICES, default="Scraping")

    title = models.CharField(max_length=100, null=True)
    single_file_html_path = models.FilePathField(path="/", recursive=True, null=True)
    media_path = models.FilePathField(path="/", recursive=True, null=True)

    def __str__(self):
        if self.title is not None:
            return self.title
        return self.url
