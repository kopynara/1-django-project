# _20250723dj/_20250723django/photo/urls.py
from django.urls import path
# from django.http import HttpResponse # 기존에 있던 이 줄은 이제 필요 없으므로 삭제하거나 주석 처리합니다.
from django.views.generic import TemplateView # TemplateView를 사용하기 위해 import 합니다.

app_name = 'photo'

urlpatterns = [
    # 'photo/' 경로로 접속했을 때, photo/photo_list.html 템플릿을 렌더링하도록 설정합니다.
    path('', TemplateView.as_view(template_name='photo/photo_list.html'), name='index'),
]