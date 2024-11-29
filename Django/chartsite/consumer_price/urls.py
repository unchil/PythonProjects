from django.urls import path

from . import views


app_name = "consumer_price"

urlpatterns = [
    path("", views.index, name="index")
]