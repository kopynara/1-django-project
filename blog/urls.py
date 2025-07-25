# blog/urls.py

from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from blog.views import * # 모든 뷰 임포트 (blog/views.py에 정의된 PostLV, PostDV 등 모든 뷰 클래스 사용)

app_name = 'blog' # 앱의 네임스페이스 설정
urlpatterns = [
    # /blog/
    path('', PostLV.as_view(), name='index'), # 게시물 목록 페이지 (PostLV 뷰 사용)
    # /blog/post/
    path('post/', PostLV.as_view(), name='post_list'), # 게시물 목록 페이지 (PostLV 뷰 사용, 동일)
    # /blog/post/django-example/
    re_path(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='detail'), # slug 기반 상세 페이지 (PostDV 뷰 사용, 이름 'detail'로 변경)
    # /blog/archive/
    path('archive/', PostAV.as_view(), name='post_archive'), # 아카이브 페이지 (PostAV 뷰 사용)
    # /blog/2025/
    path('<int:year>/', PostYAV.as_view(), name='post_year_archive'), # 연도별 아카이브 (PostYAV 뷰 사용)
    # /blog/2025/jul/
    path('<int:year>/<str:month>/', PostMAV.as_view(), name='post_month_archive'), # 월별 아카이브 (PostMAV 뷰 사용)
    # /blog/2025/jul/24/
    path('<int:year>/<str:month>/<int:day>/', PostDAV.as_view(), name='post_day_archive'), # 일별 아카이브 (PostDAV 뷰 사용)
    # /blog/today/
    path('today/', PostTAV.as_view(), name='post_today_archive'), # 오늘 날짜 아카이브 (PostTAV 뷰 사용)
    # /blog/tag/
    path('tag/', TagCloudTV.as_view(), name='tag_cloud'), # 태그 클라우드 (TagCloudTV 뷰 사용)
    # /blog/tag/tagname/
    path('tag/<str:tag>/', PostTOL.as_view(), name='post_tag_list'), # 특정 태그 게시물 목록 (PostTOL 뷰 사용)
    # /blog/search/
    path('search/', SearchFV.as_view(), name='search'), # 검색 페이지 (SearchFV 뷰 사용)
]