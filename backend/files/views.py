from rest_framework.decorators import api_view
from rest_framework.response import Response
from .upload_services import handle_file_upload



@api_view(["POST"])
def upload_file(request):

    file = request.FILES.get("file")
    username = request.data.get("username")
    channel_id = request.data.get("channel_id")
    receiver_id = request.data.get("receiver_id")

    if not file or not username:
        return Response({"error": "file and username required"}, status=400)

    channel_id = int(channel_id) if channel_id and channel_id != "undefined" else None
    receiver_id = int(receiver_id) if receiver_id and receiver_id != "undefined" else None 
    try:
        uploaded = handle_file_upload(
            file,
            username,
            channel_id,
            receiver_id
        )

        return Response({
            "message": "File uploaded successfully",
            "filename": uploaded.filename
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def get_files(request):
    return Response({"message": "File API working"})