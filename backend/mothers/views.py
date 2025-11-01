from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mother_dashboard(request):
    if request.user.role != 'mother':
        return Response({"error": "Unauthorized"}, status=403)
    return Response({"message": f"Welcome Mother {request.user.username}!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nurse_dashboard(request):
    if request.user.role != 'nurse':
        return Response({"error": "Unauthorized"}, status=403)
    return Response({"message": f"Welcome Nurse {request.user.username}!"})
