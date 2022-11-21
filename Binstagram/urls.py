"""Binstagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import Sub
from content.views import Main, UploadFeed
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # 127.0.0.1 뒤에 admin을 치면, 뒤에 있는 거 실행
    path('main/', Main.as_view()),  # 아무것도 안 치면 Sub 클래스를 view로 사용하겠다.
    path('content/upload', UploadFeed.as_view())
]

# 유저가 업로드하여 media에 들어간 파일을 조회하기 위해 필요한 코드
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)