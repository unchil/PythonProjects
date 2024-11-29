from django.urls import path

from . import views

app_name = "dash_sample"

urlpatterns = [
    path("", views.index, name="index")
]