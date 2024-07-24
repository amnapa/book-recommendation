from django.urls import path
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]