# Generated by Django 3.1.5 on 2021-02-23 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0050_remove_menuitem_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='site',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='sitemenuitem', to='conference.site'),
            preserve_default=False,
        ),
    ]
