# serializer takes care of converting the model data into python code
from dataclasses import field
from django.forms import IntegerField, ValidationError
from rest_framework import serializers
from api.models import Bet


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bet
        fields = '__all__'
   
    
