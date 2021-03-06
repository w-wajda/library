# Generated by Django 4.0 on 2021-12-17 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_review',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='libraries.book', verbose_name='Book'),
        ),
    ]
