from django.db import models
from users.models import User
from channels_app.chanels import Channel
from django.core.exceptions import ValidationError

# Allowed file types
ALLOWED_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]

MAX_SIZE = 100 * 1024 * 1024  # 100MB in bytes


def validate_file(file):

    # Check file size
    if file.size > MAX_SIZE:
        raise ValidationError("File size cannot exceed 100MB")

    # Check file type
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError("Allowed types: PDF, DOC, DOCX, JPG, JPEG, CSV, XLS, XLSX")



class UploadedFile(models.Model):

    # The actual file saved to disk
    file = models.FileField(upload_to='uploads/')

    # Original filename
    filename = models.CharField(max_length=255)

    # Who uploaded it
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Which channel it was sent in
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    # When it was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} by {self.uploaded_by}"