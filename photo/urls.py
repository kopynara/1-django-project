from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from .views import PhotoLV, PhotoDV # PhotoLV (List View), PhotoDV (Detail View) 임포트

app_name = 'photo' # 이 앱의 네임스페이스를 'photo'로 설정

urlpatterns = [
    # 사진 목록 페이지: /photo/
    path('', PhotoLV.as_view(), name='index'),
    
    # 사진 상세 페이지: /photo/사진ID/
    # Photo 모델의 get_absolute_url 메서드에서 id를 사용하므로, 여기에 <int:pk>를 사용합니다.
    path('<int:pk>/', PhotoDV.as_view(), name='detail'),

    # 태그별 사진 목록 페이지 (PhotoLV 재사용)
    # URL: /photo/tag/tagname/ (특정 태그가 달린 사진)
    # [-\w]+는 유니코드 단어 문자(한글 포함), 숫자, 하이픈, 언더스코어를 모두 매칭합니다.
    # 이전에 제거했던 것을 다시 추가합니다.
    re_path(r'^tag/(?P<tag_slug>[-\w\uAC00-\uD7A3]+)/$', PhotoLV.as_view(), name='photo_list_by_tag'),

    # 아래 PhotoTagCloudTV 관련 URL 패턴은 이제 사용하지 않으므로 제거합니다.
    # path('tagcloud/', PhotoTagCloudTV.as_view(), name='tagcloud'),
]
