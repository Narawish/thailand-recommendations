# Generated by Django 5.1.1 on 2024-10-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0007_alter_place_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]