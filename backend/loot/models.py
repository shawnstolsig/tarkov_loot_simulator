from django.db import models
import uuid


class Item(models.Model):
    '''
    '   An item represents one object from the game.  Storing everything that is available 
    '   from Tarkov Markets website.
    '''
    long_name = models.CharField(max_length=200)

    # allowing these fields to be null since each item will be created with long name, then info pulled from Tarkov Market later
    uuid = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    market_price = models.IntegerField(null=True, blank=True)  
    trader_price = models.IntegerField(null=True, blank=True)  
    slots = models.IntegerField(null=True, blank=True)  # total num slots occupied
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    rotated = models.BooleanField(default=0)
    image = models.URLField(max_length=400, null=True, blank=True)
    wiki_url = models.URLField(max_length=400, null=True, blank=True)
    market_url = models.URLField(max_length=400, null=True, blank=True)



