# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 15:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_eventlocation_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='eventlocation',
            name='campus',
            field=models.ForeignKey(blank=True, help_text='Campus of the University', null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Campus'),
        ),
    ]
