import subprocess

from celery import Celery, shared_task

app = Celery('tasks')
app.conf.broker_url = 'redis://redis:6379/0'


@shared_task(name="test")
def test():
    subprocess.run(
        ["single-file", "--browser-executable-path", "/usr/bin/chromium-browser", "--output-directory", "./data/",
         "--browser-args", "[\"--no-sandbox\"]", "https://kureta.xyz/gunesli-bir-telas-2023/"])
    print('Testing')
