from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):   # Sub 클래스
    def get(self, request):   # get으로 호출하면 get 함수 실행
        print("겟으로 호출")
        return render(request, "binstagram/main.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "binstagram/main.html")

