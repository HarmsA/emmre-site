# Generated by Django 3.1.5 on 2021-02-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0039_conferencesession_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pitchslam',
            name='pitch_imgs',
        ),
        migrations.AddField(
            model_name='pitchslam',
            name='pitch_imgs',
            field=models.ManyToManyField(blank=True, null=True, related_name='pitchslam', to='conference.Img'),
        ),
    ]
