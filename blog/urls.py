from django.urls import path, re_path # re_path 임포트 (정규식 기반 URL 패턴 사용을 위함)
from . import views # views 모듈 임포트 (모든 뷰 클래스를 참조할 수 있도록)

app_name = 'blog' # 앱의 네임스페이스 설정

urlpatterns = [
    # /blog/ (모든 게시물 목록 페이지)
    path('', views.PostListView.as_view(), name='index'), # PostLV -> PostListView
    
    # /blog/post/ (게시물 목록 페이지, index와 동일)
    path('post/', views.PostListView.as_view(), name='post_list'), # PostLV -> PostListView
    
    # /blog/post/django-example/ (slug 기반 상세 페이지)
    # PostDV -> PostDetailView로 변경, URL 이름도 'detail' -> 'post_detail'로 변경
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post_detail'), 
    
    # /blog/archive/ (최근 게시물 아카이브)
    path('archive/', views.PostAV.as_view(), name='post_archive'), 
    
    # /blog/2025/ (연도별 아카이브)
    path('<int:year>/', views.PostYAV.as_view(), name='post_year_archive'), 
    
    # /blog/2025/jul/ (월별 아카이브)
    path('<int:year>/<str:month>/', views.PostMAV.as_view(), name='post_month_archive'), 
    
    # /blog/2025/jul/24/ (일별 아카이브)
    path('<int:year>/<str:month>/<int:day>/', views.PostDAV.as_view(), name='post_day_archive'), 
    
    # /blog/today/ (오늘 날짜 아카이브)
    path('today/', views.PostTAV.as_view(), name='post_today_archive'), 
    
    # /blog/tag/ (태그 클라우드)
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'), 
    
    # /blog/tag/tagname/ (특정 태그 게시물 목록)
    # PostListView 뷰를 사용하여 태그 이름으로 필터링된 목록을 보여줍니다.
    # URL 이름을 'post_list_by_tag'로 변경하고, 인자 이름을 'tag_slug'로 변경합니다.
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'), 
    
    # /blog/search/ (검색 페이지)
    path('search/', views.SearchFV.as_view(), name='search'), 
]
