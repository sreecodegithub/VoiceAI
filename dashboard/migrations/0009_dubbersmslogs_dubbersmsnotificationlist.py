# Generated by Django 4.0 on 2022-01-11 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_dubberwebhooknotifications_dubberwebhooknotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='DubberSMSLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('smsNumber', models.BigIntegerField()),
                ('smsStatus', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DubberSMSNotificationList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('smsNumber', models.BigIntegerField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
