from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# coding: utf8


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=500)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(unique=True, max_length=500)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(unique=True, max_length=500)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.BigIntegerField()
    url = models.URLField(null=False, unique=True)
    name = models.CharField(max_length=500)
    nutri_grade = models.CharField(null=True, max_length=1)
    cat = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    energy = models.IntegerField(null=True)
    fat = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    fibers = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    img = models.URLField(null=True)
    img_small = models.URLField(null=True)
    last_modified_t = models.DateTimeField(null=False)
    brands = models.ManyToManyField(Brand, db_table="products_brands")
    stores = models.ManyToManyField(Store, db_table="products_stores")

    def __str__(self):
        return self.name


class Favorite(models.Model):

    substitute = models.ForeignKey(
        Product,
        related_name='products_substitute_set',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        default=0,
    )
