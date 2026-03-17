from django.urls import path
from .views import get_notifications, mark_all_read, mark_read

urlpatterns = [
    path('<int:user_id>/', get_notifications),
    path('<int:user_id>/read-all/', mark_all_read),
    path('read/<int:notification_id>/', mark_read),
]