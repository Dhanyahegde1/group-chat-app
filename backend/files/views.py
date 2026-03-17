from rest_framework.decorators import api_view
from rest_framework.response import Response
from .upload_services import handle_file_upload
from users.models import User


@api_view(["POST"])
def upload_file(request):

    file = request.FILES.get("file")
    username = request.data.get("username")
    channel_id = request.data.get("channel_id")
    receiver_id = request.data.get("receiver_id")

    if not file or not username:
        return Response({"error": "file and username required"}, status=400)

    try:
        if channel_id:
            # Channel file upload
            uploaded = handle_file_upload(file, username, channel_id)
        elif receiver_id:
            # DM file upload — save without channel
            from .models import UploadedFile
            user = User.objects.get(username=username)
            uploaded = UploadedFile.objects.create(
                file=file,
                filename=file.name,
                uploaded_by=user,
                channel=None  # no channel for DMs
            )
        else:
            return Response({"error": "channel_id or receiver_id required"}, status=400)

        return Response({
            "message": "File uploaded successfully",
            "filename": uploaded.filename,
            "uploaded_by": username,
            "uploaded_at": str(uploaded.uploaded_at)
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["GET"])
def get_files(request):
    return Response({"message": "File API working"})