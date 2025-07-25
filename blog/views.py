# blog/views.py

from django.shortcuts import render # 필요한 경우를 위해 임포트 유지
from django.views.generic import ListView, DetailView, TemplateView # TemplateView 추가
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView # 날짜 기반 아카이브 뷰 임포트
from django.db.models import Q # 검색 기능을 위해 Q 객체 임포트
from taggit.models import Tag # taggit의 Tag 모델 임포트

from blog.models import Post # Post 모델 임포트

#--- ListView (Post 목록) ---
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' # 템플릿에서 사용할 객체 리스트의 변수명
    paginate_by = 2 # 한 페이지에 보여줄 게시물 수
    queryset = Post.objects.all().prefetch_related('tags') # 태그를 미리 가져와서 N+1 쿼리 방지

#--- DetailView (Post 상세) ---
class PostDV(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' # 템플릿에서 사용할 객체 단일의 변수명

#--- Archive View (최근 게시물 아카이브) ---
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt' # 날짜 필드 지정
    template_name = 'blog/post_archive.html'
    context_object_name = 'posts'
    paginate_by = 2

#--- Year Archive View (연도별 아카이브) ---
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True # 해당 연도의 모든 객체를 리스트로 전달
    template_name = 'blog/post_archive_year.html'
    context_object_name = 'posts'

#--- Month Archive View (월별 아카이브) ---
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'
    month_format = '%m' # 월 포맷 지정 (예: 01, 02...)
    template_name = 'blog/post_archive_month.html'
    context_object_name = 'posts'

#--- Day Archive View (일별 아카이브) ---
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'
    month_format = '%m' # 월 포맷 지정
    template_name = 'blog/post_archive_day.html'
    context_object_name = 'posts'

#--- Today Archive View (오늘 날짜 아카이브) ---
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
    template_name = 'blog/post_archive_day.html' # 오늘 날짜도 일별 아카이브 템플릿 사용
    context_object_name = 'posts'

#--- Tag Cloud View (태그 클라우드) ---
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html' # taggit에서 제공하는 기본 템플릿

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 모든 태그를 이름 순으로 정렬하여 컨텍스트에 추가
        context['tags'] = Tag.objects.all().order_by('name')
        return context

#--- Post List by Tag View (특정 태그별 게시물 목록) ---
class PostTOL(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # URL에서 'tag' 파라미터를 가져와 해당 태그를 가진 게시물 필터링
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tags__name=tag).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs.get('tag') # 현재 태그 이름을 템플릿에 전달
        return context

#--- Search Form View (검색 폼) ---
class SearchFV(ListView):
    paginate_by = 5 # 검색 결과 페이지당 5개 게시물
    template_name = 'blog/post_list.html' # 검색 결과도 post_list 템플릿 사용
    context_object_name = 'posts'

    def get_queryset(self):
        # URL 쿼리 파라미터에서 'q' 값을 가져옴 (검색어)
        q = self.request.GET.get('q', '')
        if q:
            # 제목(title) 또는 내용(content)에 검색어가 포함된 게시물 검색
            # Q 객체를 사용하여 OR 조건 검색, distinct()로 중복 제거
            return Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).distinct()
        return Post.objects.none() # 검색어가 없으면 빈 쿼리셋 반환

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '') # 템플릿에 검색어 전달
        return context