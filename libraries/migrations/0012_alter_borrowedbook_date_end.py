# Generated by Django 4.0 on 2021-12-29 13:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0011_borrowedbook_date_end_borrowedbook_date_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2022, 1, 28, 13, 14, 32, 212565, tzinfo=utc), verbose_name='Date return'),
        ),
    ]