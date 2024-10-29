from django.db import models

# Create your models here.

class FiveMSupplyDemand(models.Model):
    baseDatetime = models.TextField(primary_key=True)
    suppAbility = models.FloatField(default=0.0)
    currPwrTot = models.FloatField(default=0.0)
    forecastLoad = models.FloatField(default=0.0)
    suppReservePwr = models.FloatField(default=0.0)
    suppReserveRate = models.FloatField(default=0.0)
    operReservePwr = models.FloatField(default=0.0)
    operReserveRate = models.FloatField(default=0.0)

