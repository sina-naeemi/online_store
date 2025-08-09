from django.contrib import admin
from django.urls import path

from .views import Listproducts


urlpatterns = [
    path("List/" , Listproducts.as_view())
]

