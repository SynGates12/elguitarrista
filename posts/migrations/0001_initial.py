# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-09 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apres', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('partitura', models.TextField(null=True)),
                ('video', models.FileField(null=True, upload_to='videos/', verbose_name='')),
                ('votsPositius', models.IntegerField()),
                ('votsNegatius', models.IntegerField()),
            ],
        ),
    ]
