# Generated by Django 3.2.7 on 2024-01-31 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zvo_app', '0012_about_header'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='backup_url',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='video',
            name='file',
        ),
    ]
