# Generated by Django 4.0.3 on 2023-03-17 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_alter_user_confirm_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirm_password',
        ),
    ]
