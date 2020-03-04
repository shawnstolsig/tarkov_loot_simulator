from django.db import models
import uuid


class Item(models.Model):
    '''
    '   An item represents one object from the game.  Storing everything that is available 
    '   from Tarkov Markets website.
    '''
    uuid = models.CharField(max_length=36, null=True, blank=True)
    long_name = models.CharField(max_length=200, null=True, blank=True)

    # allowing these fields to be null since each item will be created with long name, then info pulled from Tarkov Market later
    short_name = models.CharField(max_length=50, null=True, blank=True)
    market_price = models.IntegerField(null=True, blank=True)  
    trader_price = models.IntegerField(null=True, blank=True)  
    trader_name = models.CharField(max_length=50, null=True, blank=True)
    trader_currency = models.CharField(max_length=10, null=True, blank=True)
    slots = models.IntegerField(null=True, blank=True)  # total num slots occupied
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    rotated = models.BooleanField(default=0)
    image_url = models.URLField(max_length=400, null=True, blank=True)
    wiki_url = models.URLField(max_length=400, null=True, blank=True)
    market_url = models.URLField(max_length=400, null=True, blank=True)



