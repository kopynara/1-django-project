from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from . import views # views 모듈을 임포트합니다.

app_name = 'blog' # 앱의 네임스페이스를 'blog'로 설정합니다.

urlpatterns = [
    # 모든 게시물 목록 페이지 (PostListView 사용)
    # URL: /blog/
    path('', views.PostListView.as_view(), name='index'), 
    
    # 블로그 아카이브 페이지 (기존)
    path('archive/', views.PostAV.as_view(), name='post_archive'), 
    
    # 블로그 검색 페이지 (기존)
    path('search/', views.SearchFV.as_view(), name='search'), 

    # 블로그 태그 클라우드 페이지 (기존)
    # /blog/tag/ 경로가 먼저 매칭되도록 일반 slug 패턴보다 위에 배치
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'), 
    
    # 태그별 게시물 목록 페이지 (PostListView 재사용)
    # 한글(유니코드) 태그 슬러그를 허용하도록 정규 표현식 유지
    re_path(r'^tag/(?P<tag_slug>[-\w\uAC00-\uD7A3]+)/$', views.PostListView.as_view(), name='post_list_by_tag'),

    # 게시물 상세 페이지 (PostDetailView 사용)
    # URL: /blog/세번째-포스트/ (slug 기반 상세 페이지)
    # 가장 일반적인 패턴이므로 다른 구체적인 패턴들 뒤로 이동
    re_path(r'^(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post_detail'), 
]
