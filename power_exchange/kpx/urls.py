"""
URL configuration for kpx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from supplydemand.views import FiveMinuteSD



supplydemand_patterns=([
    path("one_hr/", FiveMinuteSD.getLast1HR, name="one_hr"),
    path("two_hr/", FiveMinuteSD.getLast2HR, name="two_hr"),
    path("one_day/", FiveMinuteSD.getLast1Day, name="one_day"),
], "supplydemand" )


urlpatterns = [
    path('SD/', include(supplydemand_patterns) ),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
]

