# Generated by Django 3.0.3 on 2020-04-28 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0003_auto_20200424_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha',
            field=models.DateField(default=datetime.date(2020, 4, 28)),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='hora',
            field=models.TimeField(default=datetime.time(15, 31, 11, 628845)),
        ),
    ]
