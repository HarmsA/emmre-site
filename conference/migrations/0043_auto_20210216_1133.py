# Generated by Django 3.1.5 on 2021-02-16 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0042_auto_20210215_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='slug',
            field=models.SlugField(blank=True, choices=[('codemirror', 'codemirror'), ('conference', 'conference'), ('images', 'images'), ('novel_writers_digest_conference', 'novel_writers_digest_conference'), ('tinymce', 'tinymce'), ('writers_digest_conference', 'writers_digest_conference')], null=True, unique=True, verbose_name='folder'),
        ),
    ]
