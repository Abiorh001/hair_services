from django.urls import path
from products import views

urlpatterns = [
    path('product-categories/create/', views.CreateProductCategoryView.as_view(),
            name='product-categories'),
    path('product-categories/', views.ListProductCategoryView.as_view(),
                name='list-product-categories'),
    path('products/create/', views.CreateProductView.as_view(), name='create-products'),
    path('products/all/', views.ListProductView.as_view(),
            name='list-products'),
    path('products/by-name/<str:product_name>/', views.RetrieveProductsByNameView.as_view(),
         name='retrieve-products'),
    path('products/<int:id>/', views.RetrieveUpdateDestroyProductView.as_view(),
         name='retrieve-update-destroy-products'),
    path('products/orders/create/', views.CreateProductOrderView.as_view(),
         name='create-product-orders'),
    path('products/orders/all/', views.ListProductOrderView.as_view(),
            name='list-product-orders'),
    path('products/orders/<int:id>/', views.RetrieveUpdateDestroyProductOrderView.as_view(),
            name='retrieve-update-destroy-product-orders'),
    
]