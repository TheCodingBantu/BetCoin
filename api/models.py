from django.db import models
import datetime
# Create your models here.
class Bet(models.Model):
    
    progression=models.IntegerField()
    result=models.CharField(max_length=64)
    stake=models.FloatField()
    odds=models.FloatField()
    # target=models.CharField(max_length=64)
    # profit=models.CharField(max_length=64)
    total_lost=models.FloatField()
    # balance=models.CharField(max_length=64)
    date_created=models.DateTimeField(default=datetime.datetime.now())
    
    
    