from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# from django.contrib.auth.forms import UserCreationForm
# from .forms import UserForm, RegistrationForm, LoginForm
# from customusers.models import CustomUser
from .models import Category, Payment, Product, Order, OrderItem, NewsletterSubscription, Cart
from .serializers import PaymentSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CategorySerializer, NewsletterSubscriptionSerializer, CartSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from nourish import settings
import paystack
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Cart.objects.filter(user=user)
        else:
            # Handle the case where the user is anonymous
            # For example, you could return an empty queryset
            return Cart.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().create(request, *args, **kwargs)
        else:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)


# class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
#     queryset = NewsletterSubscription.objects.all()
#     serializer_class = NewsletterSubscriptionSerializer
#     data = {'key': 'value'}
#     response = Response(data)

    

#     # Allow CORS
#     response["Access-Control-Allow-Origin"] = "http://localhost:5500", "http://localhost:3000"
#     response["Access-Control-Allow-Methods"] = "POST"
#     response["Access-Control-Allow-Headers"] = "Content-Type"


class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer

    @action(detail=False, methods=['post'])
    def create_subscription(self, request):
        try:
            serializer = NewsletterSubscriptionSerializer(data=request.data)

            if serializer.is_valid():
                # Save the subscription
                subscription = serializer.save()
                print("subscription saved")

                # Send confirmation email
                subject = 'Subscription Confirmation'
                message = f'Thank you for signing up!!!'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [subscription.email]

                print("Mail about to send")
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print("Mail sent!")

                data = {'success': True, 'message': 'Subscription created successfully'}
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                # errors = serializer.errors
                # data = {'success': False, 'errors': errors}
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except (ValidationError, IntegrityError) as e:
            print(f"Caught exception: {e}")
            if 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
                # Custom error message for duplicate email
                data = {'success': False, 'message': 'Email address is already subscribed'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Handle other ValidationError cases
                data = {'success': False, 'message': 'Validation error while processing the request'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {str(e)}")
            data = {'success': False, 'message': 'An error occurred while processing the request'}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def home(request):
    return render(request, 'base/home.html')

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
transaction = Transaction(secret_key=paystack_secret_key)

class PaymentViewSet(viewsets.ViewSet):
    serializer_class = PaymentSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount_in_naira = serializer.validated_data.get('amount')
        amount_in_kobo = amount_in_naira * 100
        email = serializer.validated_data.get('email')
        # Initialize payment on Paystack   
        response = Transaction.initialize(amount=amount_in_kobo, email=email, currency='NGN', callback_url='http://127.0.0.1:8000/api/base/paystack-payments')
     
        # Redirect user to Paystack UI for payment
        payment_url = response['data']['authorization_url']
        return redirect(payment_url)


    # def retrieve(self, request, pk=None):
    #     reference = pk
    #     response = Transaction.verify(reference=reference)
    #     return Response(response)
    
# def payment_callback(request):
#     # Handle the payment callback logic here
#     return HttpResponse(status=200)


# The views used to render the templates for sign in, register and login

# def sign_up(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Deactivate user until the second step
#             user.save()
#             request.session['user_id'] = user.id
#             return redirect('register')
#     else:
#         form = RegistrationForm()

#     return render(request, 'base/sign_up.html', {'form': form})


# def register(request):
#     # Retrieve 'user_id' from session or redirect to sign up if not present
#     user_id = request.session.get('user_id')

#     if user_id is None:
#         print("User ID not present in session. Redirecting to step 1.")
#         return redirect('sign_up')

#     user = CustomUser.objects.get(pk=user_id)

#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             user.is_active = True
#             form.save()
#             login(request, user)
            
#             # Remove 'user_id' from session after sign-up
#             user_id_from_session = request.session.pop('user_id', None)
            
#             if user_id_from_session is not None:
#                 print(f"Removed 'user_id' from session: {user_id_from_session}")
#             else:
#                 print("'user_id' was not present in session.")
            
#             return redirect('home')
#         else:
#             print("Form is not valid. Errors:", form.errors)
#     else:
#         form = UserForm(instance=user)

#     return render(request, 'base/register.html', {'form': form})


# def log_in(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Extract username/email and password from the form
#             username_email = form.cleaned_data['username_email']
#             password = form.cleaned_data['password']

#             # Try to get the user by email
#             user = authenticate(request, email=username_email, password=password)

#             if user is None:
#                 # If the user does not exist by email, try by username
#                 user = authenticate(request, username=username_email, password=password)

#             if user is not None:
#                 # If the user exists, authenticate and log in
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 # If the user does not exist or the password is incorrect, show an error message
#                 messages.error(request, 'Invalid username/email or password.')
#                 # Redirect the user to the login page or display the login form again
#                 return redirect('login') 
#         else:
#             # If the form is not valid, show an error message
#             messages.error(request, 'Invalid form submission.')
#     else:
#         # If the request method is not POST, create an empty form
#         form = LoginForm()

#     return render(request, 'base/login.html', {'form': form})


# class SignUpAPIView(APIView):
#     def post(self, request):
#         form = RegistrationForm(request.data)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             request.session['user_id'] = user.id
#             serializer = CustomUserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterAPIView(APIView):
#     def post(self, request):
#         user_id = request.session.get('user_id')
#         if user_id is None:
#             return Response({"error": "User ID not present in session."}, status=status.HTTP_400_BAD_REQUEST)

#         user = CustomUser.objects.get(pk=user_id)
#         form = UserForm(request.data, instance=user)
#         if form.is_valid():
#             user.is_active = True
#             form.save()
#             login(request, user)
#             request.session.pop('user_id', None)
#             serializer = CustomUserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# class LogInAPIView(APIView):
#     def post(self, request):
#         form = LoginForm(request.data)
#         if form.is_valid():
#             username_email = form.cleaned_data['username_email']
#             password = form.cleaned_data['password']

#             user = authenticate(request, email=username_email, password=password)

#             if user is None:
#                 user = authenticate(request, username=username_email, password=password)

#             if user is not None:
#                 login(request, user)
#                 serializer = CustomUserSerializer(user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid username/email or password."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Invalid form submission."}, status=status.HTTP_400_BAD_REQUEST)