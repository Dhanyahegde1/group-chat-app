from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

def home(request):
    return HttpResponse("Chat Application Backend Running")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('users/', include('users.links')),
    path('channels/', include('channels_app.chanel_url')),  # ADD THIS
]