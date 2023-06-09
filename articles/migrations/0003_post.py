# Generated by Django 4.2 on 2023-04-22 07:22

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderator', '0003_user_dark_mode'),
        ('articles', '0002_alter_petition_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moderator.moderator')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': '5. Postlar',
            },
        ),
    ]
