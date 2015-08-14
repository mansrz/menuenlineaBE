from rest_framework import serializers
from web.models import *

from push_notifications.models import GCMDevice

class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
        #field = ('name','is_active'.'user','device_id','registration_id')
        field = ('objects','device_id','registration_id')

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Restaurant
        fields = ('id', 'name', 'place', 'longitude', 'latitude', 'image_restaurant')

class RestaurantDishSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    class Meta:
        model = RestaurantDish
        fields = ('id', 'restaurant', 'name', 'price', 'image_dish', 'votes')

    def get_votes(self, obj):
        return str(obj.votes())

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CategoryCriteriaSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CategoryCriteria
        fields = ('id', 'evaluation', 'category', 'name')

    def get_name(self, obj):
        return str(obj.evaluation.name)

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'name')

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = ('id', 'evaluation', 'restaurantdish', 'user', 'points')

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'name')



