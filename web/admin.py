from django.contrib import admin

from models import *

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(RestaurantDish)
admin.site.register(Category)
admin.site.register(Evaluation)
admin.site.register(EvaluationCriteria)
