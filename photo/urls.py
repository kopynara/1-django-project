from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from .views import PhotoLV, PhotoDV, PhotoTagCloudTV # PhotoTagCloudTV 임포트

app_name = 'photo' # 이 앱의 네임스페이스를 'photo'로 설정

urlpatterns = [
    # 사진 목록 페이지: /photo/
    path('', PhotoLV.as_view(), name='index'),
    
    # 사진 상세 페이지: /photo/사진ID/
    path('<int:pk>/', PhotoDV.as_view(), name='detail'),

    # 태그별 사진 목록 페이지: /photo/tag/태그슬러그/
    re_path(r'^tag/(?P<tag_slug>[-\w\uAC00-\uD7A3]+)/$', PhotoLV.as_view(), name='photo_list_by_tag'),

    # 사진 태그 클라우드 페이지: /photo/tagcloud/
    path('tagcloud/', PhotoTagCloudTV.as_view(), name='tag_cloud'),
]
