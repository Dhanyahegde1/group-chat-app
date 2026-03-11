# Import HttpResponse to create a simple test endpoint
from django.http import HttpResponse

# Django admin panel
from django.contrib import admin

# URL routing utilities
from django.urls import path, include


# ---------------------------------------------------
# Simple home route to confirm backend is running
# ---------------------------------------------------
def home(request):
    return HttpResponse("Chat Application Backend Running")


# ---------------------------------------------------
# Main URL routing for the project
# ---------------------------------------------------
urlpatterns = [

    # Root endpoint
    # Used to verify that the backend server is running
    path('', home),

    # Django admin panel
    path('admin/', admin.site.urls),

    # User authentication routes
    # Example endpoints:
    # /users/register
    # /users/login
    path('users/', include('users.links')),

    # Channel management routes
    # Example endpoints:
    # /channels/create
    # /channels/join
    # /channels/list
    path('channels/', include('channels_app.chanel_url')),

    # Messaging routes
    # Example endpoints:
    # /messages/send
    # /messages/history
    path('messages/', include('messaging.msgroute')),
    path('files/', include('files.file_url')),
]