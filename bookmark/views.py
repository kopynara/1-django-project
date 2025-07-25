from django.views.generic import ListView, DetailView
from .models import Bookmark, Category
from django.db.models import Q
# 로그인 여부를 확인하기 위해 LoginRequiredMixin을 임포트합니다.
from django.contrib.auth.mixins import LoginRequiredMixin

# 북마크 목록을 보여주는 뷰 (사용자별 필터링 및 정렬 기능 추가)
# LoginRequiredMixin을 추가하여 로그인한 사용자만 접근할 수 있도록 합니다.
class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'bookmark/bookmark_list.html'
    context_object_name = 'object_list'
    ordering = ['-created_at'] # 기본 정렬: 최신순

    # 로그인하지 않은 사용자가 접근 시 리다이렉트될 URL을 지정합니다.
    # settings.py에 LOGIN_URL이 설정되어 있지 않다면 기본값은 /accounts/login/ 입니다.
    # 필요하다면 settings.py에 LOGIN_URL = '/accounts/login/'을 추가할 수 있습니다.
    login_url = '/admin/login/' # 임시로 관리자 로그인 페이지로 리다이렉트 (나중에 사용자 로그인 페이지로 변경)

    def get_queryset(self):
        # 현재 로그인한 사용자(self.request.user)의 북마크만 필터링합니다.
        # super().get_queryset()은 기본적으로 모든 북마크를 가져오지만,
        # 여기에 .filter(owner=self.request.user)를 추가하여 소유자로 필터링합니다.
        queryset = super().get_queryset().filter(owner=self.request.user)
        
        # 정렬 기준과 정렬 방식을 쿼리 파라미터에서 가져옵니다.
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
        context = super().get_context_data(**kwargs)
        context['current_sort_by'] = self.request.GET.get('sort', 'created_at')
        context['current_order'] = self.request.GET.get('order', 'desc')
        return context


# 북마크 상세 페이지를 보여주는 뷰
# LoginRequiredMixin을 추가하여 로그인한 사용자만 접근할 수 있도록 합니다.
class BookmarkDetailView(LoginRequiredMixin, DetailView):
    model = Bookmark
    template_name = 'bookmark/bookmark_detail.html'
    context_object_name = 'object'
    login_url = '/admin/login/' # 임시로 관리자 로그인 페이지로 리다이렉트

    def get_queryset(self):
        # 상세 페이지도 현재 로그인한 사용자의 북마크만 볼 수 있도록 필터링합니다.
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


# 검색 기능을 위한 뷰 (사용자별 필터링 및 정렬 기능 추가)
# LoginRequiredMixin을 추가하여 로그인한 사용자만 접근할 수 있도록 합니다.
class BookmarkSearchListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'bookmark/bookmark_list.html'
    context_object_name = 'object_list'
    login_url = '/admin/login/' # 임시로 관리자 로그인 페이지로 리다이렉트

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        
        # 현재 로그인한 사용자(self.request.user)의 북마크만 필터링합니다.
        queryset = Bookmark.objects.filter(owner=self.request.user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(url__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        
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
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort_by'] = self.request.GET.get('sort', 'created_at')
        context['current_order'] = self.request.GET.get('order', 'desc')
        return context

