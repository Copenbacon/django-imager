# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_auto_20170123_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='album',
            name='published',
            field=models.CharField(choices=[('private', 'Private'), ('shared', 'Shared'), ('public', 'Public')], default='private', max_length=100000),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='photo',
            name='published',
            field=models.CharField(choices=[('private', 'Private'), ('shared', 'Shared'), ('public', 'Public')], default='private', max_length=100000),
        ),
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
