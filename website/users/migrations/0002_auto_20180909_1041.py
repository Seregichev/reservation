# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-09 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Сompanies'},
        ),
        migrations.AlterField(
            model_name='company',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='Full name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='short_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='Short name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='tax',
            field=models.DecimalField(decimal_places=1, default=18.0, max_digits=3, verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='company',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Company', verbose_name='Company'),
        ),
    ]
