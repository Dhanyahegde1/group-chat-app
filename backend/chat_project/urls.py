from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

# Simple home route to confirm backend is running
def home(request):
    return HttpResponse("Chat Application Backend Running")

# main URL routing for the project
urlpatterns = [

    # Root endpoint to verify that the backend server is running
    path('', home),

    # Django admin panel
    path('admin/', admin.site.urls),

    # User authentication routes
    path('users/', include('users.links')),

    # Channel management routes
    path('channels/', include('channels_app.chanel_url')),

    # Messaging routes
    path('messages/', include('messaging.msgroute')),

    path('files/', include('files.file_url')),
]

