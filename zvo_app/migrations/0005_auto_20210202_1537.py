# Generated by Django 3.1.5 on 2021-02-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zvo_app', '0004_about_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='about',
            old_name='text',
            new_name='paragraph_1',
        ),
        migrations.AddField(
            model_name='about',
            name='paragraph_2',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]
