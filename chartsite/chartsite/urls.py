"""
URL configuration for chartsite project.

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



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from consumer_price import views as consumer_price_views

from dash_sample import views as dash_sample_views


dash_sample_patterns=([
 path("", dash_sample_views.index, name="index"),
],
  "dash_sample"
)

consumer_price_patterns = ([
    path("", consumer_price_views.index, name="index"),
    path("mat_video", consumer_price_views.mat_video, name="mat_video"),
    path("express", consumer_price_views.plotly_express, name="express"),
    path("chart/<int:question_id>", consumer_price_views.get_chart, name="chart"),
    ],
    "consumer_price",
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("consumer/", include(consumer_price_patterns)),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path("dash/", include(dash_sample_patterns)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
