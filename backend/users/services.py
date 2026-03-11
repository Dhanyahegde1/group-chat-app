# Import the custom User model
from .models import User


# ---------------------------------------------------
# Service Function: Create User
# ---------------------------------------------------
# This function handles the business logic of creating
# a new user in the database.
#
# It uses Django's built-in create_user() method which:
# - hashes the password
# - saves the user securely
# - follows Django authentication standards
#
def create_user(username, email, password):

    # Create user using Django ORM
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # Return the created user object
    return user