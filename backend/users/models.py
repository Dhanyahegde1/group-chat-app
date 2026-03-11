# Import Django's built-in AbstractUser model
# This allows us to extend the default user functionality
from django.contrib.auth.models import AbstractUser

# Import Django model base class
from django.db import models


# ---------------------------------------------------
# Custom User Model
# ---------------------------------------------------
# Extends Django's default AbstractUser to add extra fields
class User(AbstractUser):

    # Email field must be unique for every user
    email = models.EmailField(unique=True)

    # Automatically stores the timestamp when a user account is created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the user object
    # This will show the username in Django admin and querysets
    def __str__(self):
        return self.username