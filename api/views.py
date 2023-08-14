from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from bs4 import BeautifulSoup
import requests
from .models import Product
from .serializers import ProductSerializer
from decimal import Decimal


class WelcomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Flipkart Scraper API!"}, status=status.HTTP_200_OK)

class UserSignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'detail': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email address already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    # Using the built-in view for JWT token generation
    pass

class ScrapeFlipkartView(APIView):
    def post(self, request):
        # Authenticate user
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        flipkart_url = request.data.get('url')
        if not flipkart_url:
            return Response({'detail': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_product = Product.objects.filter(url=flipkart_url).first()

        if existing_product:
            if existing_product.user == request.user:
                # URL is present in the database for the logged-in user
                serializer = ProductSerializer(existing_product)
                return Response(serializer.data)
            else:
                # URL is present in the database but for the other user
                return Response({'detail': 'URL already exists for another user.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the URL is not present in the database
        response = requests.get(flipkart_url)
        if response.status_code != 200:
            return Response({'detail': 'Failed to fetch the URL.'}, status=status.HTTP_400_BAD_REQUEST)

        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting the required fields from the URL's web page
        title = soup.find('span', {'class': 'B_NuCI'}).text
        price_str = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text
        price_numeric = Decimal(price_str.replace('₹', '').replace(',', ''))
        description = soup.find('div', {'class': '_1mXcCf RmoJUa'}).text
        ratings_reviews_span = soup.find('span', {'class': '_2_R_DZ'})
        if ratings_reviews_span:
            ratings_reviews_text = ratings_reviews_span.get_text()
            ratings_text, reviews_text = ratings_reviews_text.split('&')
            ratings_count = int(ratings_text.replace(',', '').strip().split()[0])
            review_count = int(reviews_text.replace(',', '').strip().split()[0])
        else:
            ratings_count = 0
            review_count = 0
        ratings = float(soup.find('div', {'class': '_3LWZlK'}).text)
        media_count = len(soup.find_all('li', {'class': '_20Gt85 _1Y_A6W'}))

        product = Product(
            user=request.user,
            url=flipkart_url,
            title=title,
            price=price_numeric,
            description=description,
            review_count=review_count,
            ratings_count=ratings_count,
            ratings=ratings,
            media_count=media_count
        )
        # save the data to database
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



