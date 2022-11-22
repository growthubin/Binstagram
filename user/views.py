import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password
from Binstagram.settings import MEDIA_ROOT

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    # 회원가입
    def post(self, request):
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        # post로 입력받은 사용자의 정보들을 models.py에서 만든 User DB에 추가
        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    # 로그인
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        # 쿼리
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인을 했다. 세션 or 쿠키. email로 세션을 저장하면, user.objeect로부터 다른 정보를 가져올 수 있음
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()  # 세션 clear 후 delete
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):
        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex  # 랜덤하게 이미지 파일명 재생성
        save_path = os.path.join(MEDIA_ROOT, uuid_name)  # 두 가지 path 더하기 ~/media/uuidsjfksjdkfjsf

        with open(save_path, 'wb+') as destination:  # 파일 열어서 저장하는 코드
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        # DB에 접근해 사용자(객체) 정보(프로필 이미지) 수정
        user = User.objects.filter(email=email).first()
        user.profile_image = profile_image
        user.save()

        return Response(status=200)
