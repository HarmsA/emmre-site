# Generated by Django 3.1.5 on 2021-02-18 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0046_auto_20210216_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='child_intro',
            new_name='excerpt',
        ),
    ]
