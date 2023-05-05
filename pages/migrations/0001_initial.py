# Generated by Django 4.2 on 2023-04-20 07:57

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Eslatma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Eslatma',
                'verbose_name_plural': 'Eslatma',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/icon')),
            ],
            options={
                'verbose_name': 'Ikonka',
                'verbose_name_plural': '1. Ikonka',
            },
        ),
        migrations.CreateModel(
            name='IjtimoiyTarmoqlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon', models.ImageField(upload_to='images/tarmoq/icon')),
            ],
            options={
                'verbose_name': 'Ijtimoiy tarmoq',
                'verbose_name_plural': '2. Ijtimoiy tarmoqlar',
            },
        ),
        migrations.CreateModel(
            name='Manzili',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manzil', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Manzil',
                'verbose_name_plural': 'Manzil',
            },
        ),
        migrations.CreateModel(
            name='MaqolaJoylash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/info')),
                ('body', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Maqola joylash',
                'verbose_name_plural': 'Maqola joylash',
            },
        ),
        migrations.CreateModel(
            name='Narxlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/narxlar')),
                ('body', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Narxlar',
                'verbose_name_plural': 'Narxlar',
            },
        ),
    ]