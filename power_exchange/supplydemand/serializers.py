from rest_framework import serializers
from .models import FiveMSupplyDemand


class FiveMinuteSDSerializer(serializers.Serializer):

    baseDatetime = serializers.CharField()
    suppAbility = serializers.CharField()
    currPwrTot = serializers.CharField()
    forecastLoad = serializers.CharField()
    suppReservePwr = serializers.CharField()
    suppReserveRate = serializers.CharField()
    operReservePwr = serializers.CharField()
    operReserveRate = serializers.CharField()


