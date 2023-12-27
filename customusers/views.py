from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .serializers import CustomUserSerializer, UserSerializer, RegistrationSerializer, LoginSerializer
from rest_framework import viewsets, status
from customusers.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.


# class CustomUserViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list` and `retrieve` actions.
#     """
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sign_up(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            request.session['user_id'] = user.id
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return Response({'detail': 'User ID not present in session.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(pk=user_id)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            user.is_active = True
            serializer.save()
            login(request, user)
            request.session.pop('user_id', None)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def log_in(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_email = serializer.validated_data['username_email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username_email, password=password)
            if user is None:
                user = authenticate(request, email=username_email, password=password)

            if user is not None:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid username/email or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)