# Generated by Django 3.1.5 on 2021-02-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0054_auto_20210223_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
