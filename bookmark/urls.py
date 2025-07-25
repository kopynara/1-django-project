from django.urls import path
from . import views # views 모듈 전체를 임포트하거나, 필요한 뷰만 명시적으로 임포트합니다.

app_name = 'bookmark'

urlpatterns = [
    # 북마크 목록 페이지: BookmarkListView.as_view()로 수정
    path('', views.BookmarkListView.as_view(), name='index'),
    # 북마크 상세 페이지: BookmarkDetailView.as_view()로 수정
    path('<int:pk>/', views.BookmarkDetailView.as_view(), name='detail'),
    # 검색 기능 URL: BookmarkSearchListView 사용
    path('search/', views.BookmarkSearchListView.as_view(), name='search'),
]
