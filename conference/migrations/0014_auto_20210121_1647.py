# Generated by Django 3.1.5 on 2021-01-21 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0013_auto_20210121_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesession',
            name='related_speaker',
            field=models.ManyToManyField(blank=True, related_name='conference_sessions', to='conference.Speaker'),
        ),
    ]
