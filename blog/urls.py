from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from . import views # views 모듈 임포트 (모든 뷰 클래스를 참조할 수 있도록)

app_name = 'blog' # 앱의 네임스페이스 설정

urlpatterns = [
    # /blog/ (모든 게시물 목록 페이지)
    path('', views.PostLV.as_view(), name='index'), # PostLV 뷰 사용 (기존 'index' 이름 유지)
    
    # /blog/post/ (게시물 목록 페이지, index와 동일)
    path('post/', views.PostLV.as_view(), name='post_list'), 
    
    # /blog/post/django-example/ (slug 기반 상세 페이지)
    # <int:pk> 대신 <slug:slug>를 사용하여 slug 필드를 인자로 받도록 수정
    # URL 이름은 'post_detail'로 설정합니다.
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDV.as_view(), name='post_detail'), 
    
    # /blog/archive/ (최근 게시물 아카이브)
    path('archive/', views.PostAV.as_view(), name='post_archive'), 
    
    # /blog/archive/2025/ (연도별 아카이브)
    path('archive/<int:year>/', views.PostYAV.as_view(), name='post_year_archive'), 
    
    # /blog/archive/2025/jul/ (월별 아카이브)
    re_path(r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', views.PostMAV.as_view(), name='post_month_archive'), 
    
    # /blog/archive/2025/jul/29/ (일별 아카이브)
    re_path(r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', views.PostDAV.as_view(), name='post_day_archive'), 
    
    # /blog/archive/today/ (오늘 날짜 아카이브)
    path('archive/today/', views.PostTAV.as_view(), name='post_today_archive'), 
    
    # /blog/tag/ (태그 클라우드)
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'), 
    
    # /blog/tag/tagname/ (특정 태그 게시물 목록)
    # PostLV 뷰를 사용하여 태그 이름으로 필터링된 목록을 보여줍니다.
    # URL 이름을 'post_tag_list'로 설정하고, 인자 이름을 'tag_slug'로 변경합니다.
    path('tag/<slug:tag_slug>/', views.PostLV.as_view(), name='post_tag_list'), 
    
    # /blog/search/ (검색 페이지)
    path('search/', views.SearchFV.as_view(), name='search'), 
]
