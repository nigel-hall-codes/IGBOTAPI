# Generated by Django 2.0.6 on 2018-06-14 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_auto_20180613_0400'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSettings',
        ),
    ]