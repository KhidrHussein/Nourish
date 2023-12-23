from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, RegistrationForm, LoginForm
from customusers.models import CustomUser

# Create your views here.


def home(request):
    return render(request, 'base/home.html')



def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until the second step
            user.save()
            request.session['user_id'] = user.id
            return redirect('register')
    else:
        form = RegistrationForm()

    return render(request, 'base/sign_up.html', {'form': form})


def register(request):
    # Retrieve 'user_id' from session or redirect to sign up if not present
    user_id = request.session.get('user_id')

    if user_id is None:
        print("User ID not present in session. Redirecting to step 1.")
        return redirect('sign_up')

    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.is_active = True
            form.save()
            login(request, user)
            
            # Remove 'user_id' from session after sign-up
            user_id_from_session = request.session.pop('user_id', None)
            
            if user_id_from_session is not None:
                print(f"Removed 'user_id' from session: {user_id_from_session}")
            else:
                print("'user_id' was not present in session.")
            
            return redirect('home')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = UserForm(instance=user)

    return render(request, 'base/register.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract username/email and password from the form
            username_email = form.cleaned_data['username_email']
            password = form.cleaned_data['password']

            # Try to get the user by email
            user = authenticate(request, email=username_email, password=password)

            if user is None:
                # If the user does not exist by email, try by username
                user = authenticate(request, username=username_email, password=password)

            if user is not None:
                # If the user exists, authenticate and log in
                login(request, user)
                return redirect('home')
            else:
                # If the user does not exist or the password is incorrect, show an error message
                messages.error(request, 'Invalid username/email or password.')
                # Redirect the user to the login page or display the login form again
                return redirect('login') 
        else:
            # If the form is not valid, show an error message
            messages.error(request, 'Invalid form submission.')
    else:
        # If the request method is not POST, create an empty form
        form = LoginForm()

    return render(request, 'base/login.html', {'form': form})