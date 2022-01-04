# Generated by Django 4.0 on 2022-01-02 21:12

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0012_alter_borrowedbook_date_end'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-entry',)},
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='libraries.author', verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='libraries.Category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='libraries.publisher', verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2022, 2, 1, 21, 12, 1, 639190, tzinfo=utc), verbose_name='Date return'),
        ),
    ]
