# Generated by Django 3.1.5 on 2021-02-15 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zvo_app', '0009_auto_20210215_0221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='mp4',
            new_name='file',
        ),
        migrations.RemoveField(
            model_name='video',
            name='webm',
        ),
    ]