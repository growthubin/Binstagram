from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed  # Feed라는 클래스를 가져올 거다

class Main(APIView):   # Sub 클래스
    def get(self, request):   # get으로 호출하면 get 함수 실행
        feed_list = Feed.objects.all().order_by('-id')  # select * from content_feed;

        return render(request, "binstagram/main.html", context=dict(feeds=feed_list))  # feeds <- 템플릿에 보여줄 딕셔너리의 key


class UploadFeed(APIView):
    def post(self, request):
        file = request.data.get('file')
        image = request.data.get('image')
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        return Response(status=200)