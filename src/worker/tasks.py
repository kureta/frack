import subprocess
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import django

from celery import Celery, shared_task
from celery.exceptions import TaskError

django.setup()
from core.models import Bookmark  # noqa: E402

app = Celery('tasks')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.broker_transport_options = {'visibility_timeout': 240}  # 4 minutes

# Make some stuff configurable
DATA_DIR = Path('./data').absolute()
SINGLE_FILE_CMD = ["single-file"]
SINGLE_FILE_ARGUMENTS = ["--browser-executable-path",
                         "/usr/bin/chromium-browser",
                         "--browser-args",
                         "[\"--no-sandbox\"]"]
YT_DLP_CMD = ["yt-dlp"]
YT_DLP_ARGUMENTS = ["-S", "ext"]


def single_file_output(directory):
    return ["--output-directory", directory]


def yt_dlp_output(directory):
    return ["--output", f'{directory}/%(title)s.%(ext)s']


def get_single_file(url, directory):
    return SINGLE_FILE_CMD + SINGLE_FILE_ARGUMENTS + single_file_output(directory) + [url]


def get_yt_dlp(url, directory):
    return YT_DLP_CMD + YT_DLP_ARGUMENTS + yt_dlp_output(directory) + [url]


@shared_task(name="get_media")
def get_media(url):
    with TemporaryDirectory() as temp_dir:
        result = subprocess.run(get_yt_dlp(url, temp_dir), capture_output=True, text=True)

        if result.returncode != 0:
            print(result.stderr)
            bookmark = Bookmark.objects.get(url=url)
            bookmark.media_status = 'Failed'
            bookmark.save()
            raise TaskError('Failed to download media')

        file_path = Path(temp_dir).rglob('*.*').__next__()
        shutil.move(file_path, DATA_DIR / file_path.name)

        media_path = str(DATA_DIR / file_path.name)

        bookmark = Bookmark.objects.get(url=url)
        status = 'Scraped'
        bookmark.media_path = media_path
        bookmark.media_status = status
        bookmark.save()


@shared_task(name="scrape_page")
def scrape_page(url):
    with TemporaryDirectory() as temp_dir:
        result = subprocess.run(get_single_file(url, temp_dir), capture_output=True, text=True)

        if result.stderr != '' or result.returncode != 0:
            bookmark = Bookmark.objects.get(url=url)
            bookmark.scrape_status = 'Failed'
            bookmark.save()
            raise TaskError('Failed to download page')

        file_path = Path(temp_dir).rglob('*.html').__next__()
        shutil.move(file_path, DATA_DIR / file_path.name)

        title = '('.join(file_path.name.split('(')[:-1]).strip()
        status = 'Scraped'
        single_file_html_path = str(DATA_DIR / file_path.name)

        bookmark = Bookmark.objects.get(url=url)
        bookmark.title = title[:100]
        bookmark.scrape_status = status
        bookmark.single_file_html_path = single_file_html_path
        bookmark.save()
