from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import UserSerializer


class UserCreateView(APIView):
    """
    View para criação de novos usuários.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()  # Cria o usuário
            return Response(
                {"message": "User created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )