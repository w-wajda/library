# Generated by Django 4.0 on 2022-01-04 20:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0014_alter_borrowedbook_date_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2022, 2, 3, 20, 46, 58, 896873, tzinfo=utc), verbose_name='Date return'),
        ),
    ]