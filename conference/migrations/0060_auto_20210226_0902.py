# Generated by Django 3.1.5 on 2021-02-26 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0059_auto_20210226_0901'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'ordering': ('last_name',)},
        ),
    ]
