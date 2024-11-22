# Generated by Django 5.1.2 on 2024-11-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_trip_confirmed_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajet',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='destination',
            field=models.CharField(db_index=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='heure',
            field=models.TimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='source',
            field=models.CharField(db_index=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='trip',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='destination',
            field=models.CharField(db_index=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='trip',
            name='source',
            field=models.CharField(db_index=True, default='', max_length=64),
        ),
        migrations.AddIndex(
            model_name='trajet',
            index=models.Index(fields=['source', 'destination', 'date'], name='home_trajet_source_0c782c_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['source', 'destination', 'date'], name='home_trip_source_ee43a3_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['is_confirmed'], name='home_trip_is_conf_168101_idx'),
        ),
    ]
