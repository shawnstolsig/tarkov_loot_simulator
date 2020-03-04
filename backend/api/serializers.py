from rest_framework import serializers
from loot.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Item
        fields = '__all__'