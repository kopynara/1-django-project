"""
URL configuration for _20250723django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include # include 함수 임포트
from django.conf import settings # settings를 사용하기 위해 임포트
from django.conf.urls.static import static # static 함수를 사용하기 위해 임포트
import os # os 모듈 임포트 (STATIC_ROOT 설정에 필요)

urlpatterns = [
    # Django 관리자 페이지 URL
    path('admin/', admin.site.urls),

    # 웹사이트 루트 URL ('/')에 home 앱의 urls.py 포함
    path('', include('home.urls')),

    # 'bookmark/' 경로를 bookmark 앱의 urls.py로 전달
    path('bookmark/', include('bookmark.urls')),

    # 'blog/' 경로를 blog 앱의 urls.py로 전달
    path('blog/', include('blog.urls')),

    # 'photo/' 경로를 photo 앱의 urls.py로 전달
    path('photo/', include('photo.urls')),

    # 'tagcloud/' 경로를 새로 생성한 tag_cloud 앱의 urls.py로 전달
    path('tagcloud/', include('tag_cloud.urls')),
]

# 개발 환경에서만 미디어 파일과 정적 파일을 서빙하도록 설정
# DEBUG가 True일 때만 static() 함수를 사용하여 MEDIA_URL 및 STATIC_URL에 대한 요청을 처리
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 정적 파일 서빙 설정 (STATICFILES_DIRS를 사용하도록)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))

