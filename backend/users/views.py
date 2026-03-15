from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from users.models import User

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
            "username": user.username,
            "id": user.id
        })

    # If credentials are invalid
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['GET'])
def list_users(request):
    users = User.objects.all().values("id", "username")
    return Response(list(users))