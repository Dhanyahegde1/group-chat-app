from rest_framework.decorators import api_view
from rest_framework.response import Response
from .upload_services import handle_file_upload


@api_view(['POST'])
def upload_file(request):

    file = request.FILES.get('file')
    username = request.data.get('username')
    channel_id = request.data.get('channel_id')

    # Check all fields are present
    if not file or not username or not channel_id:
        return Response({"error": "file, username and channel_id are required"}, status=400)

    try:
        uploaded = handle_file_upload(file, username, channel_id)
        return Response({
            "message": "File uploaded successfully",
            "filename": uploaded.filename,
            "uploaded_by": username,
            "uploaded_at": str(uploaded.uploaded_at)
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_files(request, channel_id):
    from .models import UploadedFile
    files = UploadedFile.objects.filter(channel_id=channel_id).values(
        'id', 'filename', 'uploaded_by__username', 'uploaded_at', 'file'
    )
    return Response(list(files))