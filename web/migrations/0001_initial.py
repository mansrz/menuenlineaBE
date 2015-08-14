# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(related_name='evaluations', to='web.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EvaluationCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('evaluation', models.ForeignKey(related_name='restaurantdishes', to='web.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('place', models.CharField(max_length=128)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('image_restaurant', models.ImageField(null=True, upload_to=b'restaurants/')),
                ('description', models.TextField(max_length=512, null=True)),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
            },
        ),
        migrations.CreateModel(
            name='RestaurantDish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('image_dish', models.ImageField(null=True, upload_to=b'restaurants/')),
                ('restaurant', models.ForeignKey(to='web.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='restaurantdish',
            field=models.ForeignKey(related_name='evaluations', to='web.RestaurantDish'),
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='user',
            field=models.ForeignKey(related_name='evaluations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='evaluations',
            field=models.ManyToManyField(to='web.RestaurantDish', through='web.EvaluationCriteria'),
        ),
        migrations.AddField(
            model_name='categorycriteria',
            name='evaluation',
            field=models.ForeignKey(related_name='categorys', to='web.Evaluation'),
        ),
        migrations.AddField(
            model_name='category',
            name='categorys',
            field=models.ManyToManyField(to='web.Evaluation', through='web.CategoryCriteria'),
        ),
    ]
