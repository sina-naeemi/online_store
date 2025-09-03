from django.contrib import admin
from django.urls import path

from .views import bank_gate_view , payment


urlpatterns = [
    path("all-gate/" , bank_gate_view.as_view()),
    path("to-pay/" , payment.as_view()),
]



