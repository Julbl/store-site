# Generated by Django 4.1.7 on 2023-05-01 13:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_blog_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 1, 16, 6, 54, 680796), verbose_name='Опубликована'),
        ),
    ]
