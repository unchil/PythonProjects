from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from rest_framework.renderers import JSONRenderer

from .serializers import FiveMinuteSDSerializer
from .models import FiveMSupplyDemand, DayFiveMinSupplyDemand

from .forms import FiveMSupplyDemandForm

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

    def getCurrent1Day(self):
        query_cond = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d%H%M%S')
       # queryset = FiveMSupplyDemand.objects.filter(baseDatetime__startswith=query_cond).order_by("baseDatetime")
        queryset = FiveMSupplyDemand.objects.filter(baseDatetime__gte=query_cond).order_by("baseDatetime")
       # queryset = list(FiveMSupplyDemand.objects.order_by("-baseDatetime")[:288])
        #queryset.reverse()
        serializer = FiveMinuteSDSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def getLast1Day(self):
        query_cond = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        queryset = DayFiveMinSupplyDemand.objects.filter(baseDatetime__startswith=query_cond).order_by("baseDatetime")
        #queryset = list(DayFiveMinSupplyDemand.objects.order_by("-baseDatetime")[:288])
        #queryset.reverse()
        serializer = FiveMinuteSDSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


def fiveMinuteSD_create(request):
    if request.method == 'POST':
        form = FiveMSupplyDemandForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.create_date = datetime.timezone.now()
    else:
        form = FiveMSupplyDemandForm()


    return render(request, "supplydemand/sd_form.html", {'form':form} )