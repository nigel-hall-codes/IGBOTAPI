# Generated by Django 2.0.6 on 2018-06-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_delete_usersettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('memeOn', models.BooleanField(default=True)),
                ('newMenuItemsOn', models.BooleanField(default=True)),
                ('dailyDealsOn', models.BooleanField(default=True)),
                ('igUsername', models.TextField(default='Not given')),
                ('igPassword', models.TextField(default='Not given')),
                ('weedmapsSlug', models.TextField(default='Not given')),
                ('botPID', models.IntegerField(default=0)),
                ('botStatus', models.BooleanField(default=False)),
            ],
        ),
    ]
