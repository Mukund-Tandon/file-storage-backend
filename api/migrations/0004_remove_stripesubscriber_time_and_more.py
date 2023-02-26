# Generated by Django 4.1.3 on 2023-02-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_stripesubscriber_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stripesubscriber',
            name='time',
        ),
        migrations.AddField(
            model_name='stripesubscriber',
            name='end_time',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AddField(
            model_name='stripesubscriber',
            name='start_time',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
