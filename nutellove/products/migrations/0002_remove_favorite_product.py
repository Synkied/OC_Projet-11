# Generated by Django 2.0.3 on 2018-03-26 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='product',
        ),
    ]
