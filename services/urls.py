from django.urls import path
from services import views

urlpatterns = [
    path('services/create/', views.CreateServiceView.as_view(), name='create-services'),
    path('services/', views.ListServiceView.as_view(),
            name='list-services'),
    path('services/<int:id>/', views.RetrieveServiceView.as_view(),
         name='retrieve-services'),
    
    path('services/search-category-location/',
         views.SearchListServiceByCategoryAndLocationView.as_view(),
         name='search-services-by-category-location'),
    
    path('services/search-location-date-time/',
         views.SearchListServiceByDateTimeAndLocationView.as_view(),
         name='search-services-by-date-time-location'),
    
    path('services/all-providers/', views.ListAllServiceProvidersView.as_view(),
         name='list-all-service-providers'),
    
    path('services/providers/', views.RetrieveServiceProviderView.as_view(),
            name='retrieve-service-provider'),
    
    path('services/shops/', views.ListAllServiceProviderShopView.as_view(),
            name='list-all-service-shops'),
    
    path('services/shop/', views.RetrieveServiceProviderShopView.as_view(),
            name='retrieve-service-shop'),
   
   path('recently-visited-pages/' , views.RecentlyVisitedPagesView.as_view(),
         name='recently-visited-pages'),
   
   path('services/featured-professionals/', views.ListOfFeaturedServiceProvidersViews.as_view(),
         name='list-of-featured-service-providers'),
   
   path('services/top-professionals/', views.ListOfTopRatedServiceProvidersViews.as_view(),
         name='list-of-top-rated-service-providers'),
   
   path('services/by-category/', views.SearchListServiceByCategory.as_view(),
                name='search-services-by-category'),
   
   path('services/service-provider-by-service/', views.SearchListServiceProviderByService.as_view(),
                name='search-service-provider-by-service'),
   
   path('services/service-provider/all-services/', views.ListAllserviceProviderServices.as_view(),
name='list-service-provider-services')
]