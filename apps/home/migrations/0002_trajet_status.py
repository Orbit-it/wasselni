# Generated by Django 5.1.2 on 2024-11-13 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trajet',
            name='status',
            field=models.CharField(default='', max_length=64),
        ),
    ]
