# Generated by Django 4.1.7 on 2023-05-02 16:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_blog_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 2, 19, 57, 57, 777779), verbose_name='Опубликована'),
        ),
    ]
