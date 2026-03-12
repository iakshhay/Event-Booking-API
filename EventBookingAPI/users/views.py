from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Profile
from .serializers import RegisterSerializer, ProfileSerializer, UserSerializer

# Create your views here.
class RegistrationView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
        
class UserView(generics.GenericAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user=request.user
        serializer=self.get_serializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
