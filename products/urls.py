from django.contrib import admin
from django.urls import path

from .views import Listproducts ,Detailproduct , CategoryListView ,AllGenre , FileListView ,FileDetailView , ProductByGenre ,ProductByCategory


urlpatterns = [
    path("Category/" , CategoryListView.as_view() , name="category-list"),
    path("Category/<int:pk>/" , AllGenre.as_view() , name='product_genre'),

    path("List/" , Listproducts.as_view() , name="product-list"),
    path("List/<int:pk>/" , Detailproduct.as_view(), name="product-detail"),
    path("List/by-genre/<str:genre_name>/" , ProductByGenre.as_view() , name="products-by-genre"),
    path("List/by-category/<int:category_id>/" ,ProductByCategory.as_view() , name="product-by-category"),
    path("List/<int:product_id>/file/" ,FileListView.as_view() , name='file-list' ),
    path("List/<int:product_id>/file/<int:pk>/" , FileDetailView.as_view() , name="file-detail"),
]

