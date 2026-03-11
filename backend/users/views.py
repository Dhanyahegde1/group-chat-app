# Import API decorator for creating REST endpoints
from rest_framework.decorators import api_view

# Import Response class for sending API responses
from rest_framework.response import Response

# Import HTTP status codes
from rest_framework import status

# Import serializer for user registration
from .serializers import RegisterSerializer

# Import Django authentication system
from django.contrib.auth import authenticate


# ---------------------------------------------------
# User Registration API
# Endpoint: POST /users/register
# ---------------------------------------------------
@api_view(['POST'])
def register(request):

    # Pass incoming request data to serializer
    serializer = RegisterSerializer(data=request.data)

    # Validate data
    if serializer.is_valid():

        # Save user to database
        serializer.save()

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

    # Return validation errors if input is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------
# User Login API
# Endpoint: POST /users/login
# ---------------------------------------------------
@api_view(['POST'])
def login(request):

    # Extract username and password from request body
    username = request.data.get("username")
    password = request.data.get("password")

    # Authenticate user using Django auth system
    user = authenticate(username=username, password=password)

    # If authentication is successful
    if user:
        return Response({
            "message": "Login successful",
            "username": user.username
        })

    # If credentials are invalid
    return Response({"error": "Invalid credentials"}, status=400)
