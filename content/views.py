from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed  # Feed라는 클래스를 가져올 거다
from user.models import User
import os
from Binstagram.settings import MEDIA_ROOT


class Main(APIView):  # Sub 클래스
    def get(self, request):  # get으로 호출하면 get 함수 실행
        feed_list = Feed.objects.all().order_by('-id')  # select * from content_feed;

        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")  # email이 없으면(로그아웃 상태면) 메인 안 보여주고 login 페이지만 보여줌

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, "user/login.html")  # 사용자 정보가 없어도 로그인 페이지만 보여줌(다시 로그인 시도해라)

        # feeds <- main.html 화면에 보여줄 딕셔너리의 key
        return render(request, "binstagram/main.html", context=dict(feeds=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex  # 랜덤하게 이미지 파일명 재생성
        save_path = os.path.join(MEDIA_ROOT, uuid_name)  # 두 가지 path 더하기 ~/media/uuidsjfksjdkfjsf

        with open(save_path, 'wb+') as destination:  # 파일 열어서 저장하는 코드
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        # 피드에 저장(피드에 업로드한 정보 프론트에 추가하기)
        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")  # email이 없으면(로그아웃 상태면) 메인 안 보여주고 login 페이지만 보여줌

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, "user/login.html")  # 사용자 정보가 없어도 로그인 페이지만 보여줌(다시 로그인 시도해라)

        return render(request, 'content/profile.html', context=dict(user=user))