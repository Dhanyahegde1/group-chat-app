from .models import UploadedFile
from users.models import User
from channels_app.chanels import Channel


def handle_file_upload(file, username, channel_id=None, receiver_id=None):

    user = User.objects.get(username=username)

    channel = None
    receiver = None

    if channel_id:
        channel = Channel.objects.get(id=channel_id)

    if receiver_id:
        receiver = User.objects.get(id=receiver_id)

    if not channel and not receiver:
        raise ValueError("Either channel_id or receiver_id is required")

    uploaded = UploadedFile.objects.create(
        file=file,
        filename=file.name,
        uploaded_by=user,
        channel=channel,
        receiver=receiver
    )

    return uploaded
