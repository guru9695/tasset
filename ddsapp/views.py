from django.shortcuts import render
from rest_framework import generics, status,views,permissions
from .serializers import RegisterSerializer,LoginSerializer,Movi_ModelSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Movi_Model
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters



# Create your views here.


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        # user = User.objects.get(email=user_data['email'])
        # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hi '+user.username + \
        #     ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}

        # Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class movilistView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Movi_ModelSerializer
   
    def get(self, request, format=None):
        login_uaer_data=request.user
        snippets = Movi_Model.objects.all()
        serializer = Movi_ModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Movi_ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function for update delete retrive oraganation
class detailViewDetail(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Movi_ModelSerializer
    def get_object(self, pk):
        try:
            return Movi_Model.objects.get(pk=pk)
        except Movi_Model.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Movi_ModelSerializer(snippet)
        return Response(serializer.data)
import django_filters        
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
class movifilter(ListAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset=Movi_Model.objects.all()
    serializer_class=Movi_ModelSerializer
    filterset_fields = ['movi_title','movi_rank','description']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['movi_title','movi_rank','description']

    