from django.urls import path
from .views import upload_file, get_files

urlpatterns = [

    path('upload/', upload_file),
    path('channel/<int:channel_id>/', get_files),

]