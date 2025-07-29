from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from . import views # views 모듈 임포트 (모든 뷰 클래스를 참조할 수 있도록)

app_name = 'blog' # 앱의 네임스페이스 설정

urlpatterns = [
    # /blog/ (모든 게시물 목록 페이지)
    path('', views.PostListView.as_view(), name='index'), 
    
    # /blog/post/ (게시물 목록 페이지, index와 동일)
    path('post/', views.PostListView.as_view(), name='post_list'), 
    
    # /blog/archive/ (최근 게시물 아카이브)
    path('archive/', views.PostAV.as_view(), name='post_archive'), 
    
    # /blog/2025/ (연도별 아카이브)
    path('<int:year>/', views.PostYAV.as_view(), name='post_year_archive'), 
    
    # /blog/2025/jul/ (월별 아카이브)
    re_path(r'^<int:year>/<str:month>/$', views.PostMAV.as_view(), name='post_month_archive'), 
    
    # /blog/2025/jul/24/ (일별 아카이브)
    re_path(r'^<int:year>/<str:month>/<int:day>/$', views.PostDAV.as_view(), name='post_day_archive'), 
    
    # /blog/today/ (오늘 날짜 아카이브)
    path('today/', views.PostTAV.as_view(), name='post_today_archive'), 
    
    # /blog/search/ (검색 페이지)
    path('search/', views.SearchFV.as_view(), name='search'), 
    
    # /blog/tag/tagname/ (특정 태그 게시물 목록)
    # 기존 path('<slug:tag_slug>/', ...) 대신 re_path를 사용하여 유니코드 문자를 허용합니다.
    # [-\w\uAC00-\uD7A3]+는 유니코드 단어 문자(한글 포함), 숫자, 하이픈, 언더스코어를 모두 매칭합니다.
    re_path(r'^tag/(?P<tag_slug>[-\w\uAC00-\uD7A3]+)/$', views.PostListView.as_view(), name='post_list_by_tag'), 
    
    # /blog/post/django-example/ (slug 기반 상세 페이지)
    # 이 패턴은 다른 구체적인 패턴들(예: archive, tag) 뒤에 위치해야 합니다.
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post_detail'), 
]
