# Generated by Django 4.0.3 on 2022-09-02 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_rename_is_activee_user_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_Active',
            new_name='is_active',
        ),
    ]
