from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ItemSerializer, ContainerSerializer, SpawnSerializer
from loot.models import Item, Container, Spawn

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class SpawnViewSet(viewsets.ModelViewSet):
    queryset = Spawn.objects.all()
    serializer_class = SpawnSerializer

    

