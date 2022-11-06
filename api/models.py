from django.db import models
import datetime
# Create your models here.
class Bet(models.Model):
    
    # progression=models.IntegerField()
    result=models.CharField(max_length=64)
    stake=models.CharField(max_length=64)
    odds=models.CharField(max_length=64)
    # target=models.CharField(max_length=64)
    # profit=models.CharField(max_length=64)
    total_lost=models.CharField(max_length=64)
    # balance=models.CharField(max_length=64)
    date_created=models.DateTimeField(default=datetime.datetime.now())
    
    
    