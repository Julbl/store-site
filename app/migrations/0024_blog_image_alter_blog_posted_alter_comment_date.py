# Generated by Django 4.1.7 on 2023-05-02 21:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_blog_posted_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 3, 0, 28, 41, 542314), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 3, 0, 28, 41, 543314), verbose_name='Дата комментария'),
        ),
    ]
