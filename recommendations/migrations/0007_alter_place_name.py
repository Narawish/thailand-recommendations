# Generated by Django 5.1.1 on 2024-10-24 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0006_alter_place_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]