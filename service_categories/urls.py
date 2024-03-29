from django.urls import path
from service_categories import views

urlpatterns = [
    path('service-categories/create/', views.CreateServiceCategoryView.as_view(),
            name='service-categories'),
    path('service-categories/', views.ListServiceCategoryView.as_view(),
                name='list-service-categories'),
    path('service-categories/<int:id>/', views.RetrieveServiceCategoryView.as_view(),
            name='retrieve-service-categories'),
]