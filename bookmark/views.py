from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from bookmark.models import Bookmark, Category
from django.db.models import Q # 검색 기능을 위해 Q 객체 임포트
from django.contrib.auth.mixins import LoginRequiredMixin # 로그인 여부 확인

class BookmarkListView(LoginRequiredMixin, ListView):
    # 모델 설정: Bookmark 모델을 사용
    model = Bookmark
    # 템플릿 파일 경로 설정: bookmark_list.html 템플릿을 사용
    template_name = 'bookmark/bookmark_list.html'
    # 컨텍스트 변수 이름 설정: 템플릿에서 북마크 목록을 'object_list' 대신 'bookmarks'로 접근할 수 있게 함
    context_object_name = 'bookmarks'
    # 한 페이지에 보여줄 객체 수 설정 (페이지네이션)
    paginate_by = 10 
    # 로그인하지 않은 사용자가 접근 시 리다이렉트될 URL
    login_url = '/admin/login/' 

    def get_queryset(self):
        # 현재 로그인한 사용자의 북마크만 가져오도록 필터링
        queryset = super().get_queryset().filter(owner=self.request.user)

        # 정렬 기능 추가
        sort_by = self.request.GET.get('sort', 'created_at') # 기본값: created_at
        order = self.request.GET.get('order', 'desc') # 기본값: 내림차순

        valid_sort_fields = ['title', 'url', 'created_at', 'updated_at', 'category__name']
        
        if sort_by in valid_sort_fields:
            if order == 'desc':
                queryset = queryset.order_by(f'-{sort_by}')
            else:
                queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        # 기본 컨텍스트 데이터를 가져옴
        context = super().get_context_data(**kwargs)
        # 현재 정렬 기준과 순서를 템플릿으로 전달
        context['current_sort_by'] = self.request.GET.get('sort', 'created_at')
        context['current_order'] = self.request.GET.get('order', 'desc')

        # 페이지네이션 정보를 템플릿으로 전달
        paginator = context['paginator']
        page_obj = context['page_obj']
        
        # 페이지 번호 목록 생성 (예: 1, 2, 3, ..., 10)
        max_pages_to_show = 5 # 보여줄 최대 페이지 번호 개수
        num_pages = paginator.num_pages
        current_page = page_obj.number

        start_page = max(1, current_page - (max_pages_to_show // 2))
        end_page = min(num_pages, start_page + max_pages_to_show - 1)

        # 시작 페이지 조정: 끝 페이지가 max_pages_to_show보다 작으면 시작 페이지를 더 당겨옴
        if end_page - start_page + 1 < max_pages_to_show:
            start_page = max(1, end_page - max_pages_to_show + 1)

        context['page_range'] = range(start_page, end_page + 1)
        
        return context

class BookmarkDetailView(LoginRequiredMixin, DetailView):
    # 모델 설정: Bookmark 모델을 사용
    model = Bookmark
    # 템플릿 파일 경로 설정: bookmark_detail.html 템플릿을 사용
    template_name = 'bookmark/bookmark_detail.html'
    # 컨텍스트 변수 이름 설정: 템플릿에서 북마크 객체를 'object' 대신 'bookmark'로 접근할 수 있게 함
    context_object_name = 'bookmark'
    login_url = '/admin/login/'

    def get_queryset(self):
        # 상세 페이지도 현재 로그인한 사용자의 북마크만 볼 수 있도록 필터링합니다.
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

class BookmarkSearchListView(LoginRequiredMixin, ListView):
    # 검색 뷰는 BookmarkListView를 상속받아 대부분의 기능을 재사용
    model = Bookmark
    template_name = 'bookmark/bookmark_list.html' # 동일한 템플릿 사용
    context_object_name = 'bookmarks' # 템플릿에서 북마크 목록을 'bookmarks'로 접근
    paginate_by = 10 # 한 페이지에 10개의 객체 표시
    login_url = '/admin/login/'

    def get_queryset(self):
        # BookmarkListView의 get_queryset을 먼저 호출하여 기본 필터링(사용자)을 적용
        # 여기서는 LoginRequiredMixin의 get_queryset을 호출하는 것이 아니라,
        # 직접 Bookmark.objects.filter(owner=self.request.user)를 사용합니다.
        # 이렇게 하면 BookmarkSearchListView가 BookmarkListView를 상속받지 않아도 됩니다.
        queryset = Bookmark.objects.filter(owner=self.request.user)
        
        # 검색어 가져오기
        search_query = self.request.GET.get('q', '')
        self.search_query = search_query # 템플릿에 검색어를 전달하기 위해 저장

        if search_query:
            # Q 객체를 사용하여 제목(title) 또는 URL(url) 또는 설명(description) 또는 카테고리 이름에서 검색
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(url__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct() # 중복 결과 제거

        # 검색 결과에도 정렬을 적용합니다.
        sort_by = self.request.GET.get('sort', 'created_at')
        order = self.request.GET.get('order', 'desc')
        
        valid_sort_fields = ['title', 'url', 'created_at', 'updated_at', 'category__name']
        
        if sort_by in valid_sort_fields:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            elif order == 'desc':
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset

    def get_context_data(self, **kwargs):
        # 기본 컨텍스트 데이터를 가져옴
        context = super().get_context_data(**kwargs)
        # 검색어를 템플릿으로 전달
        context['search_query'] = self.search_query
        # 현재 정렬 기준과 순서를 템플릿으로 전달
        context['current_sort_by'] = self.request.GET.get('sort', 'created_at')
        context['current_order'] = self.request.GET.get('order', 'desc')

        # 페이지네이션 정보를 템플릿으로 전달
        paginator = context['paginator']
        page_obj = context['page_obj']
        
        # 페이지 번호 목록 생성 (예: 1, 2, 3, ..., 10)
        max_pages_to_show = 5 # 보여줄 최대 페이지 번호 개수
        num_pages = paginator.num_pages
        current_page = page_obj.number

        start_page = max(1, current_page - (max_pages_to_show // 2))
        end_page = min(num_pages, start_page + max_pages_to_show - 1)

        # 시작 페이지 조정: 끝 페이지가 max_pages_to_show보다 작으면 시작 페이지를 더 당겨옴
        if end_page - start_page + 1 < max_pages_to_show:
            start_page = max(1, end_page - max_pages_to_show + 1)

        context['page_range'] = range(start_page, end_page + 1)
        
        return context
