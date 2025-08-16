from django.contrib import admin
from django.urls import path

from .views import Listproducts ,Detailproduct , CategoryListView ,CategoryDetailView , FileListView ,FileDetailView


urlpatterns = [
    path("Category/" , CategoryListView.as_view() , name="category-list"),
    path("Category/<int:pk>/" , CategoryDetailView.as_view() , name='category-detail'),


    path("List/" , Listproducts.as_view() , name="product-list"),
    path("List/<int:pk>/" , Detailproduct.as_view(), name="product-detail"),
    path("List/<int:product_id>/file/" ,FileListView.as_view() , name='file-list' ),
    path("List/<int:product_id>/file/<int:pk>/" , FileDetailView.as_view() , name="file-detail"),
]

