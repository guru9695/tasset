from django.urls import path
from .views import RegisterView,LoginAPIView,movilistView,detailViewDetail,movifilter

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('movilist/', movilistView.as_view()),
    path('detail/<int:pk>/',detailViewDetail.as_view()),
    path('movifilter/', movifilter.as_view()),
 
]