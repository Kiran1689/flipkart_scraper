from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import ScrapeFlipkartView, WelcomeView, UserSignupView

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),  
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('scrape/', ScrapeFlipkartView.as_view(), name='scrape-flipkart'),
  
]
