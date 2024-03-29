from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReviewServiceSerializer, RatingReviewServiceSerializer
from .models import ReviewAndRating
from services.models import Service
from professional_service_provider.models import ServiceProviderProfile
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateListReviewServiceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all reviews",
        operation_description="List all reviews",
        tags=['Reviews & Ratings'],
        responses={
            200: ReviewServiceSerializer(many=True),
        }
    )
    def get(self, request):
    
        reviews = ReviewAndRating.objects.all()
        serializer = ReviewServiceSerializer(reviews, many=True)
        response = {
            "status": "success",
            "message": "Reviews retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a review",
        operation_description="Registered users as a client can make a review for a particular service of a service provider",
        tags=['Reviews & Ratings'],
        request_body=ReviewServiceSerializer,
        responses={
            201: ReviewServiceSerializer(),
            400: "Bad request"
        }
    )
    def post(self, request):
        user = request.user
        data = request.data
        service_provider_name = data.get('service_provider')
        if service_provider_name:
            service_provider_name = service_provider_name.lower()
        service_name = data.get('service')
        if service_name:
            service_name = service_name.lower()
        review_text = data.get('review_text')
        
        try:
            service_provider = ServiceProviderProfile.objects.get(business_name=service_provider_name)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service provider does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = Service.objects.get(service_name=service_name, service_provider=service_provider)
        except Service.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        review = ReviewAndRating(
            user=user,
            service_provider=service_provider,
            service=service,
            review_text=review_text
        )
        review.save()
        
        serializer = ReviewServiceSerializer(review)
        response = {
            "status": "success",
            "message": "Review added successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CreateListRatingReviewServiceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all reviews and ratings",
        operation_description="List all reviews and ratings",
        tags=['Reviews & Ratings'],
        responses={
            200: RatingReviewServiceSerializer(many=True),
        }
    )
    def get(self, request):
        reviews = ReviewAndRating.objects.all()
        serializer = RatingReviewServiceSerializer(reviews, many=True)
        response = {
            "status": "success",
            "message": "Reviews and Ratings retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a review and rating",
        operation_description="Registered users as a client can make a review and rating for a particular service of a service provider",
        tags=['Reviews & Ratings'],
        request_body=RatingReviewServiceSerializer,
        responses={
            201: RatingReviewServiceSerializer(),
            400: "Bad request"
        }
    )
    def post(self, request):
        user = request.user
        data = request.data
        service_provider_name = data.get('service_provider')
        if service_provider_name:
            service_provider_name = service_provider_name.lower()
        service_name = data.get('service')
        if service_name:
            service_name = service_name.lower()
        review_text = data.get('review_text')
        rating = data.get('rating')
        if not (1 <= rating <= 5):
            response = {
                "status": "error",
                "message": "Rating must be between 1 and 5 (inclusive)",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the service provider exists and ignorecase from database
        try:
            service_provider = ServiceProviderProfile.objects.get(business_name=service_provider_name)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service provider does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = Service.objects.get(service_name__iexact=service_name, service_provider__iexact=service_provider)
        except Service.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        review = ReviewAndRating(
            user=user,
            service_provider=service_provider,
            service=service,
            review_text=review_text,
            rating=rating
        )
        review.save()
        
        serializer = RatingReviewServiceSerializer(review)
        response = {
            "status": "success",
            "message": "Review and Rating added successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyReviewRatingServiceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Client can retrieve a specific review and rating made by them",
        operation_description="Client can retrieve a specific review and rating made by them",
        tags=['Reviews & Ratings'],
        responses={
            200: RatingReviewServiceSerializer(),
            404: "Not found"
        }
    )
    def get(self, request, pk):
        user = request.user
        try:
            review_rating = ReviewAndRating.objects.get(pk=pk, user=user)
        except ReviewAndRating.DoesNotExist:
            response = {
                "status": "error",
                "message": "Review and Rating does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingReviewServiceSerializer(review_rating)
        response = {
            "status": "success",
            "message": "Review and Rating retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Client can update a specific review and rating made by them",
        operation_description="Client can update a specific review and rating made by them",
        tags=['Reviews & Ratings'],
        request_body=RatingReviewServiceSerializer,
        responses={
            200: RatingReviewServiceSerializer(),
            400: "Bad request",
            404: "Not found"
        }
    )
    def patch(self, request, pk):
        user = request.user
        data = request.data
        rating = data.get('rating')
        try:
            review_rating = ReviewAndRating.objects.get(pk=pk, user=user)
        except ReviewAndRating.DoesNotExist:
            response = {
                "status": "error",
                "message": "Review and Rating does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if not (1 <= rating <= 5):
            response = {
                "status": "error",
                "message": "Rating must be between 1 and 5 (inclusive)",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RatingReviewServiceSerializer(review_rating, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Review and Rating updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": "error",
                "message": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Client can delete a specific review and rating made by them",
        operation_description="Client can delete a specific review and rating made by them",
        tags=['Reviews & Ratings'],
        responses={
            204: "No content",
            404: "Not found"
        }
    )    
    def delete(self, request, pk):
        user = request.user
        try:
            review_rating = ReviewAndRating.objects.get(pk=pk, user=user)
        except ReviewAndRating.DoesNotExist:
            response = {
                "status": "error",
                "message": "Review and Rating does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        review_rating.delete()
        response = {
            "status": "success",
            "message": "Review and Rating deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
       

class CountAverageRatingServiceView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Retrieve an average rating for a specific service of a service provider",
        operation_description="Retrieve an average rating for a specific service of a service provider",
        tags=['Reviews & Ratings'],
        manual_parameters=[
            openapi.Parameter(
                name='service_provider',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='business name',
                required=True,
            ),
            openapi.Parameter(
                name='service',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service name',
                required=True,
            ),
        ],
        responses={
            200: "Average rating retrieved successfully",
            400: "Bad request",
            404: "Not found"
        }
    )
    def get(self, request):
        user = request.user
        #data = request.data
        service_provider = request.query_params.get('business_name')
        service_name = request.query_params.get('service')
        # if service_provider_name:
        #     service_provider_name = service_provider_name.lower()
        # service_name = data.get('service')
        # if service_name:
        #     service_name = service_name.lower()
        
        # Filter reviews for the given service and service provider
        service_provider = ServiceProviderProfile.objects.filter(business_name__iexact=service_provider).first()
        if service_provider is None:
        
            response = {
                "status": "error",
                "message": "Service provider does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     service = Service.objects.get(service_name=service_name, service_provider=service_provider)
        # except Service.DoesNotExist:
        #     response = {
        #         "status": "error",
        #         "message": "Service does not exist",
        #     }
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        review_rating = ReviewAndRating.objects.filter(service_provider=service_provider).all()
        
        
        
        # Filter out reviews with None rating
        review_rating = [review for review in review_rating if review.rating is not None]
        
        if review_rating:
            review_rating_count = sum([review.rating for review in review_rating])
            review_rating_average = review_rating_count / len(review_rating)
            review_rating_average = round(review_rating_average)
            
            response = {
                "status": "success",
                "message": f"Average Rating retrieved successfully for  {service_provider.business_name}",
                "data": review_rating_average
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": "error",
                "message": f"No reviews found for  {service_provider}",
                "data": None
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListReviewsRatingServiceForEachServiceProvider(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve all reviews and ratings for a specific service of a service provider",
        operation_description="Retrieve all reviews and ratings for a specific service of a service provider",
        tags=['Reviews & Ratings'],
        manual_parameters=[
            openapi.Parameter(
                name='service_provider',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service provider name',
                required=True,
            ),
            openapi.Parameter(
                name='service',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Service name',
                required=True,
            ),
        ],
        responses={
            200: RatingReviewServiceSerializer(many=True),
            400: "Bad request",
            404: "Not found"
        }
    )
    def get(self, request):
        data = request.data
        service_provider_name = data.get('service_provider')
        service_name = data.get('service')
        if service_provider_name:
            service_provider_name = service_provider_name.lower()
        service_name = data.get('service')
        if service_name:
            service_name = service_name.lower()
        
        try:
            service_provider = ServiceProviderProfile.objects.get(business_name=service_provider_name)
        except ServiceProviderProfile.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service provider does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = Service.objects.get(service_name=service_name, service_provider=service_provider)
        except Service.DoesNotExist:
            response = {
                "status": "error",
                "message": "Service does not exist",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        review_rating = ReviewAndRating.objects.filter(service=service).all()
        
        if review_rating:
            serializer = RatingReviewServiceSerializer(review_rating, many=True)
            response = {
                "status": "success",
                "message": f"Reviews and Ratings retrieved successfully for {service_name} by {service_provider_name}",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": "error",
                "message": f"No reviews found for {service_name} by {service_provider_name}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)