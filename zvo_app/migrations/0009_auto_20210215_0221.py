# Generated by Django 3.1.5 on 2021-02-15 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zvo_app', '0008_auto_20210206_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='file',
            new_name='mp4',
        ),
        migrations.AddField(
            model_name='video',
            name='webm',
            field=models.FileField(default='', upload_to='videos/'),
            preserve_default=False,
        ),
    ]