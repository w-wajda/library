# Generated by Django 4.0 on 2022-01-25 09:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0017_alter_book_publication_year_alter_borrowedbook_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2022, 2, 24, 9, 40, 55, 603127, tzinfo=utc), verbose_name='Date return'),
        ),
    ]
