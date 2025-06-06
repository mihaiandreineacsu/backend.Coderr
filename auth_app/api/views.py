from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationsSerializer


class RegestrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationsSerializer(data=request.data)

        try:
            if serializer.is_valid():
                new_user = serializer.save()
                token, created = Token.objects.get_or_create(user=new_user)
                return Response(
                    {
                        "token": token.key,
                        "username": new_user.username,
                        "email": new_user.email,
                        "user_id": new_user.id,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "username": user.username,
                        "email": user.email,
                        "user_id": user.id,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )