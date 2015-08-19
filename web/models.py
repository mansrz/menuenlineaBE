# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Restaurant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 64)
    place = models.CharField(max_length = 128)
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    image_restaurant = models.ImageField(upload_to='restaurants/',null = True)
    description = models.TextField(max_length = 512, null = True)

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'image_restaurant':
                field.upload_to = 'restaurants/%s' % self.name.replace(' ','')
                super(Restaurant,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name.strip()

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

class Text(models.Model):
    name = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class RestaurantDish(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length = 128)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    image_dish = models.ImageField(upload_to='restaurants/',null = True)
    day = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'image_dish':
                field.upload_to = 'restaurantsdish/%s' % self.name.replace(' ','')
                super(RestaurantDish,self).save(*args, **kwargs)

    def votes(self):
        votes = EvaluationCriteria.objects.filter(restaurantdish = self)
        total = 0
        cont = 0
        for vote in votes:
            cont = cont + 1
            total = total + vote.points
        return str(total)

    def nvotes(self):
        return str(EvaluationCriteria.objects.filter(restaurantdish = self).count())

    def __unicode__(self):
        return self.name+'-'+self.restaurant.name

class Evaluation(Text):
    evaluations = models.ManyToManyField(RestaurantDish, through='EvaluationCriteria', through_fields=( 'evaluation', 'restaurantdish'))

class Category(Text):
    categorys = models.ManyToManyField(Evaluation, through='CategoryCriteria', through_fields=('category', 'evaluation'))

class CategoryCriteria(models.Model):
    category = models.ForeignKey(Category, related_name = 'evaluations')
    evaluation = models.ForeignKey(Evaluation, related_name = 'categorys')

class EvaluationCriteria(models.Model):
    evaluation = models.ForeignKey(Evaluation, related_name = 'restaurantdishes')
    restaurantdish = models.ForeignKey(RestaurantDish, related_name = 'evaluations')
    user = models.ForeignKey(User, related_name = 'evaluations')
    points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])


