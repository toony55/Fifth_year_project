# Generated by Django 4.0.3 on 2022-09-02 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_delete_toto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_active',
            new_name='is_activee',
        ),
    ]