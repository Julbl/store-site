﻿"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from tabnanny import verbose
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    image = models.FileField(default='temp.jpg', verbose_name="Путь к картинке")

    # Методы класса:
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    # Метаданные:
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Cтатья блога"
        verbose_name_plural = "Cтатьи блога"


admin.site.register(Blog)


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментарий")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Авторк Комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    # Методы класса:
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    # Метаданные:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статье блога"


admin.site.register(Comment)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default='temp.jpg', verbose_name="Путь к картинке")

    def __str__(self):
        return self.name


admin.site.register(Product)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
