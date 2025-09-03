from django.contrib import admin
from django.urls import path


from .views import plans_View , subscription_View

urlpatterns = [
    path("all-plans/" , plans_View.as_view()),
    path("subscription/" , subscription_View.as_view())
    
]