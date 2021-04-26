# Generated by Django 3.1.7 on 2021-04-23 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_auto_20210311_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceaddon',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessiontopic',
            name='name',
            field=models.CharField(blank=True, max_length=75, null=True, unique=True, verbose_name='Genra'),
        ),
        migrations.AlterField(
            model_name='site',
            name='folder',
            field=models.SlugField(blank=True, choices=[('admin', 'admin'), ('codemirror', 'codemirror'), ('conference', 'conference'), ('fontawesome_free', 'fontawesome_free'), ('images', 'images'), ('jqueryui', 'jqueryui'), ('novel_writers_digest_conference', 'novel_writers_digest_conference'), ('tinymce', 'tinymce'), ('writers_digest_conference', 'writers_digest_conference')], max_length=255, null=True, unique=True, verbose_name='Folder'),
        ),
    ]