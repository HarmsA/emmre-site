# Generated by Django 3.1.5 on 2021-02-02 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0021_travel_travel_imgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
