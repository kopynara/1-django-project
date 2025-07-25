# home/urls.py

from django.urls import path
from home.views import HomeView

app_name = 'home' # <-- 앱 이름을 설정합니다.

urlpatterns = [
    path('', HomeView.as_view(), name='home'), # <-- 루트 경로에 HomeView를 연결합니다.
]
