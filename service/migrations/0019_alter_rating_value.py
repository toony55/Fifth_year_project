# Generated by Django 4.0.3 on 2023-03-29 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0018_alter_rating_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
