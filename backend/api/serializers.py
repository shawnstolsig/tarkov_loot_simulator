from rest_framework import serializers
from loot.models import Item, Container, Spawn

class ItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Item
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Container
        fields = '__all__'

class SpawnSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Spawn
        fields = '__all__'