from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from product import views


urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('all-products/', views.AllProductsList.as_view()),
    path('update-product-by-id/<int:pk>', views.update_product),
    path('update-product-by-id-non-image/<int:pk>', views.update_product_nonimage),
    path('get-product-by-id/<int:pk>', views.GetProductById.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('location/distance/', views.LocationDistance.as_view()),
    path('products/create', views.post_product),
    path('category-delete/<int:pk>', views.delete_category),
    path('products/<int:pk>/delete', views.ProductDelete.as_view()),
    path('category/post', views.CategoryCreate.as_view()),
    path('category/lists/', views.CategoryList.as_view()),
    path('topping/post', views.ToppingCreate.as_view()),
    path('topping/lists/', views.ToppingList.as_view()),
    path('topping-delete/<int:pk>', views.delete_topping),
]
