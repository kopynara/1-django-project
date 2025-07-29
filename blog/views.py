from django.shortcuts import render
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
from blog.models import Post # Post 모델 임포트
from photo.models import Photo # Photo 모델 임포트 (TagCloudTV에서 사진 개수를 세기 위해)
from taggit.models import Tag # Tag 모델 임포트 (django-taggit에서 제공)
from django.db.models import Q, Count, F # Q 객체, Count 함수, F 함수 임포트
from django.utils import timezone # PostTAV 뷰에서 오늘 날짜를 가져오기 위해 임포트
import calendar # 월 이름을 가져오기 위해 임포트

# blog/views.py

# --- Post 목록 뷰 (PostLV) ---
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' # 템플릿에서 사용할 객체 리스트의 이름
    paginate_by = 10 # 한 페이지에 10개의 게시물 표시

    def get_queryset(self):
        # 기본 쿼리셋: 모든 게시물을 최신 생성일 기준으로 정렬
        queryset = super().get_queryset().order_by('-created_at')

        # URL에서 tag_slug 파라미터 가져오기
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            # tag_slug가 있다면 해당 태그가 달린 게시물만 필터링
            try:
                tag = Tag.objects.get(slug=tag_slug)
                queryset = queryset.filter(tags__in=[tag])
                self.tag_name = tag.name # 템플릿에 태그 이름 전달을 위해 저장
            except Tag.DoesNotExist:
                # 해당 태그가 존재하지 않을 경우 빈 쿼리셋 반환
                queryset = Post.objects.none()
                self.tag_name = None # 태그 이름 없음
        else:
            self.tag_name = None # 태그 슬러그가 없으면 태그 이름 없음

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 태그 이름이 있다면 컨텍스트에 추가하여 템플릿으로 전달
        if self.tag_name:
            context['tagname'] = self.tag_name # 템플릿에서 'tagname'으로 접근
        return context

# --- Post 상세 뷰 (PostDV) ---
class PostDV(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' # 템플릿에서 게시물 객체를 'post'로 접근

# --- Post 아카이브 인덱스 뷰 (PostAV) ---
# 모든 게시물을 연도별로 그룹화하여 보여주는 뷰
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'created_at' # 아카이브를 위한 날짜/시간 필드 지정
    template_name = 'blog/post_archive.html' # 기존 템플릿 유지 (연도 목록 표시)
    context_object_name = 'posts' # 템플릿에서 사용할 객체 리스트의 이름
    allow_empty = True # 게시물이 없어도 페이지 표시

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 각 연도별 게시물 수를 포함하여 date_list를 전달
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC').annotate(num_posts=Count('id'))
        return context

# --- Post 연도별 아카이브 뷰 (PostYAV) ---
# 특정 연도의 게시물 목록을 보여주는 뷰
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'created_at'
    make_object_list = True # 해당 연도의 Post 객체들을 리스트로 전달
    template_name = 'blog/post_archive_year.html' # 새로운 연도별 템플릿 지정
    allow_empty = True # 게시물이 없어도 페이지 표시

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year'] # 현재 연도 전달
        # 해당 연도의 월별 목록과 게시물 수를 템플릿에 전달 (나중에 상세 디자인 시 활용)
        # context['month_list'] = Post.objects.filter(created_at__year=self.kwargs['year']).dates('created_at', 'month', order='ASC').annotate(num_posts=Count('id'))
        return context

# --- Post 월별 아카이브 뷰 (PostMAV) ---
# 특정 월의 게시물 목록을 보여주는 뷰
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'created_at'
    month_format = '%m' # URL에서 월을 인식하는 형식 (예: 01, 02)
    make_object_list = True
    template_name = 'blog/post_archive_month.html' # 새로운 월별 템플릿 지정
    allow_empty = True # 게시물이 없어도 페이지 표시

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month_number'] = self.kwargs['month'] # 월 번호 (예: '07')
        context['month_name'] = calendar.month_name[int(self.kwargs['month'])] # 월 이름 (예: 'July')
        # 해당 월의 일별 목록과 게시물 수를 템플릿에 전달 (나중에 상세 디자인 시 활용)
        # context['day_list'] = Post.objects.filter(created_at__year=self.kwargs['year'], created_at__month=self.kwargs['month']).dates('created_at', 'day', order='ASC').annotate(num_posts=Count('id'))
        return context

# --- Post 일별 아카이브 뷰 (PostDAV) ---
# 특정 일의 게시물 목록을 보여주는 뷰
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'created_at'
    month_format = '%m'
    make_object_list = True
    template_name = 'blog/post_archive_day.html' # 새로운 일별 템플릿 지정
    allow_empty = True # 게시물이 없어도 페이지 표시

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month_number'] = self.kwargs['month']
        context['month_name'] = calendar.month_name[int(self.kwargs['month'])]
        context['day'] = self.kwargs['day']
        return context

# --- Post 오늘 날짜 아카이브 뷰 (PostTAV) ---
# 오늘 날짜의 게시물 목록을 보여주는 뷰
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'created_at'
    month_format = '%m'
    make_object_list = True
    template_name = 'blog/post_archive_day.html' # 일별 아카이브 템플릿 재사용
    allow_empty = True # 게시물이 없어도 페이지 표시

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context['year'] = today.year
        context['month_number'] = today.month
        context['month_name'] = calendar.month_name[today.month]
        context['day'] = today.day
        return context

# --- 태그 클라우드 뷰 (TagCloudTV) ---
# 이 뷰는 blog 앱 내에서 태그 클라우드 기능을 제공합니다.
# tag_cloud 앱의 UnifiedTagCloudTV와 유사한 로직을 가집니다.
class TagCloudTV(ListView):
    template_name = 'tag_cloud/unified_tag_cloud.html' # 템플릿 경로를 tag_cloud 앱의 것으로 명시
    context_object_name = 'tags'

    def get_queryset(self):
        # 모든 태그를 가져오고, 각 태그에 연결된 블로그 게시물과 사진의 개수를 계산합니다.
        tags_with_counts = Tag.objects.annotate(
            # 'taggit_taggeditem_items'는 TaggedItem 모델의 related_name입니다.
            # filter=Q(taggit_taggeditem_items__content_type__model='post')는
            # TaggedItem이 연결된 모델이 'post'인 경우만 필터링하여 Count합니다.
            num_blog_posts=Count('taggit_taggeditem_items', filter=Q(taggit_taggeditem_items__content_type__model='post')),
            # 'photo' 모델에 연결된 TaggedItem만 필터링하여 Count합니다.
            num_photos=Count('taggit_taggeditem_items', filter=Q(taggit_taggeditem_items__content_type__model='photo'))
        ).annotate(
            # 전체 아이템 수 = 블로그 게시물 수 + 사진 수
            num_items=F('num_blog_posts') + F('num_photos')
        ).filter(num_items__gt=0).order_by('-num_items') # 하나라도 연결된 태그만 표시하고, 전체 아이템 수 기준으로 내림차순 정렬

        return tags_with_counts

# --- 검색 뷰 (SearchFV) ---
class SearchFV(ListView):
    model = Post
    template_name = 'blog/post_list.html' # 검색 결과를 보여줄 템플릿 (기존 post_list.html 재사용)
    context_object_name = 'posts' # 템플릿에서 사용할 검색 결과 리스트의 이름
    paginate_by = 10 # 검색 결과도 페이지네이션

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        if search_keyword:
            return Post.objects.filter(
                Q(title__icontains=search_keyword) |
                Q(content__icontains=search_keyword) |
                Q(description__icontains=search_keyword) |
                Q(tags__name__icontains=search_keyword)
            ).distinct().order_by('-created_at')
        return Post.objects.all().order_by('-created_at') # 검색어가 없으면 모든 게시물 반환

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '') # 템플릿에 검색어 다시 전달
        return context
