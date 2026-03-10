# Import Django path function for URL routing
from django.urls import path

# Import the API view functions
from .views import register, login


# ---------------------------------------------------
# User Authentication Routes
# ---------------------------------------------------
# These endpoints handle user registration and login
urlpatterns = [

    # Endpoint: POST /users/register/
    # Used to create a new user account
    path('register/', register),

    # Endpoint: POST /users/login/
    # Used for user authentication
    path('login/', login),
]