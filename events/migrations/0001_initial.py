# Generated by Django 4.1.2 on 2022-10-19 12:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Campuses',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField(default=datetime.datetime.now)),
                ('end_at', models.DateTimeField(default=datetime.datetime.now)),
                ('capacity', models.IntegerField(default=10)),
                ('user_id', models.CharField(help_text='Id of the Event creator', max_length=20, verbose_name='Event Creator')),
            ],
        ),
        migrations.CreateModel(
            name='EventMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Id of the Meal creator', max_length=20, verbose_name='Meal Creator')),
                ('meal_id', models.CharField(help_text='Id of the Global Meal', max_length=20, verbose_name='Meal Id')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventShoppingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Id of the Shopping item creator', max_length=20, verbose_name='Item Creator')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('amount', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('bringer_id', models.CharField(blank=True, help_text='Id user who will bring the shopping item', max_length=20, verbose_name='Item Bringer')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_items', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to='events.event')),
                ('food_preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='users.foodpreference')),
            ],
        ),
        migrations.CreateModel(
            name='EventMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Id of the Message creator', max_length=20, verbose_name='Message Creator')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.CharField(blank=True, help_text='Id of the Event creator', max_length=20, verbose_name='Event Location Creator')),
                ('campus', models.ForeignKey(blank=True, help_text='Campus of the University', null=True, on_delete=django.db.models.deletion.CASCADE, to='events.campus')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventlocation'),
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Id of the Event participant', max_length=20, verbose_name='Event Member')),
                ('is_creator', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='events.event')),
            ],
            options={
                'verbose_name': 'Event Member',
                'unique_together': {('event', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='EventMealVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Id of the Meal creator', max_length=20, verbose_name='Meal Creator')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='events.eventmeal')),
            ],
            options={
                'unique_together': {('user_id', 'meal')},
            },
        ),
    ]
