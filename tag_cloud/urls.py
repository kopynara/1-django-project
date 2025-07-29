from django.urls import path
from .views import UnifiedTagCloudTV # UnifiedTagCloudTV 임포트

app_name = 'tag_cloud' # 이 앱의 네임스페이스를 'tag_cloud'로 설정

urlpatterns = [
    # 통합 태그 클라우드 페이지: /tagcloud/
    path('', UnifiedTagCloudTV.as_view(), name='index'),
]
