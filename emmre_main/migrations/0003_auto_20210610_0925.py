# Generated by Django 3.1.7 on 2021-06-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emmre_main', '0002_auto_20210604_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='folder',
            field=models.SlugField(blank=True, choices=[('admin', 'admin'), ('codemirror', 'codemirror'), ('emmre', 'emmre'), ('fontawesome_free', 'fontawesome_free'), ('fonts', 'fonts'), ('images', 'images'), ('jqueryui', 'jqueryui'), ('tinymce', 'tinymce')], max_length=255, null=True, unique=True, verbose_name='Folder'),
        ),
    ]
