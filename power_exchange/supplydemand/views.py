from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.renderers import JSONRenderer

from .serializers import FiveMinuteSDSerializer
from .models import FiveMSupplyDemand, DayFiveMinSupplyDemand

# Create your views here.

class FiveMinuteSD(APIView):

    def getLast1HR(self):
        queryset = list(FiveMSupplyDemand.objects.order_by("-baseDatetime")[:12])
        queryset.reverse()
        serializer = FiveMinuteSDSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def getLast2HR(self):
        queryset = list(FiveMSupplyDemand.objects.order_by("-baseDatetime")[:24])
        queryset.reverse()
        serializer = FiveMinuteSDSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def getLast1Day(self):
        queryset = DayFiveMinSupplyDemand.objects.order_by("baseDatetime")
        serializer = FiveMinuteSDSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
