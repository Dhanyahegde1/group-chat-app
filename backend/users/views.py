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
from channels_app.chanels import Channel, ChannelMember

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
        user = serializer.save()
        try:
            general = Channel.objects.get(name="General")
            ChannelMember.objects.get_or_create(user=user, channel=general)
        except Channel.DoesNotExist:
            pass
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)


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
