from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    # 회원가입
    def post(self, request):
        pass

class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    # 로그인
    def post(self, request):
        pass