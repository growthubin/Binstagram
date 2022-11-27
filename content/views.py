from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply  # Feed라는 클래스를 가져올 거다
from user.models import User
import os
from Binstagram.settings import MEDIA_ROOT


class Main(APIView):  # Sub 클래스
    def get(self, request):  # get으로 호출하면 get 함수 실행
        feed_object_list = Feed.objects.all().order_by('-id')  # select * from content_feed;
        feed_list = []

        # Feed.objects 안에 사용자 정보가 email밖에 없으므로 feed_list에 피드에 표시할 정보를 하나씩 append
        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()  # 유저 객체(email)를 찾고
            reply_object_list = Reply.objects.filter(feed_id=feed.id)  # 해당 feed id에 해당하는 댓글 리스트 찾기
            reply_list = []

            # 댓글 목록
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))

            # 피드 이미지랑 내용, 좋아요 개수, 댓글 리스트 등 표시
            feed_list.append(dict(image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list
                                  ))

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
        email = request.session.get('email', None)

        # 피드에 저장(피드에 업로드한 정보 프론트에 추가하기)
        Feed.objects.create(image=image, content=content, email=email, like_count=0)

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


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)