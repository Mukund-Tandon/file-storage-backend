# Generated by Django 4.1.3 on 2023-01-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_email_alter_user_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='used_space',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]