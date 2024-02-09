# Generated by Django 5.0.2 on 2024-02-09 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_index=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('scrape_status', models.CharField(choices=[('Initial', 'Initial'), ('Scraping', 'Scraping'), ('Scraped', 'Scraped'), ('Failed', 'Failed'), ('Disabled', 'Disabled')], default='Initial', max_length=16)),
                ('media_status', models.CharField(choices=[('Initial', 'Initial'), ('Scraping', 'Scraping'), ('Scraped', 'Scraped'), ('Failed', 'Failed'), ('Disabled', 'Disabled')], default='Initial', max_length=16)),
                ('title', models.CharField(db_index=True, max_length=100, null=True)),
                ('single_file_html_path', models.FilePathField(max_length=256, null=True, path='/', recursive=True)),
                ('media_path', models.FilePathField(max_length=256, null=True, path='/', recursive=True)),
            ],
        ),
    ]
