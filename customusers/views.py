from django.shortcuts import render
from .serializers import CustomUserSerializer
from rest_framework import viewsets
from customusers.models import CustomUser

# Create your views here.


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
