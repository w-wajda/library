# Generated by Django 4.0 on 2021-12-13 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('date_birth', models.DateField(verbose_name='Date of birth')),
            ],
            options={
                'unique_together': {('name', 'surname')},
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('publication_year', models.PositiveSmallIntegerField(verbose_name='Publication year')),
                ('description', models.TextField(verbose_name='Description')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraries.author', verbose_name='Author')),
                ('categories', models.ManyToManyField(to='libraries.Category', verbose_name='Categories')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraries.publisher', verbose_name='Publisher')),
            ],
        ),
    ]