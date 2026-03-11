from .models import UploadedFile
from users.models import User
from channels_app.chanels import Channel


def handle_file_upload(file, username, channel_id):

    # Get user and channel from database
    user = User.objects.get(username=username)
    channel = Channel.objects.get(id=channel_id)

    # Create and save the file record
    uploaded = UploadedFile.objects.create(
        file=file,
        filename=file.name,
        uploaded_by=user,
        channel=channel
    )

    return uploaded