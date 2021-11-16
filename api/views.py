from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializer import LoginSerializer

class LoginView(APIView):
    def post(self, request, *args):
        data = JSONParser().parse(request)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            raise ValueError
        return Response(serializer.data)


class LogoutView(APIView):
    pass