from django.urls import path
from review_and_rating import views


urlpatterns = [
    path('reviews-ratings/create-list-reviews/', views.CreateListReviewServiceView.as_view(),
            name='create-list-reviews'),
    path('reviews-ratings/', views.CreateListRatingReviewServiceView.as_view(),
            name='create-list-reviews-ratings'),
    path('reviews-ratings/<int:pk>/',
         views.RetrieveUpdateDestroyReviewRatingServiceView.as_view(),
            name='retrieve-update-destroy-reviews'),
    path('reviews-ratings/average-rating/', views.CountAverageRatingServiceView.as_view(),
            name='average-rating'),
    path('reviews-ratings/service-provider-services/',
             views.ListReviewsRatingServiceForEachServiceProvider.as_view(),
            name='list-reviews-rating-service-provider-service'),
         
]