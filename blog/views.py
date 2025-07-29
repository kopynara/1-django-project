from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post # Post 모델 임포트
from photo.models import Photo # Photo 모델 임포트 (TagCloudTV에서 사진 개수를 세기 위해)
from taggit.models import Tag # Tag 모델 임포트 (django-taggit에서 제공)
from django.db import models # models.Count 사용을 위해 임포트
from django.db.models import Q, Count # Q 객체 및 Count 함수 임포트
from django.utils import timezone # PostTAV 뷰에서 오늘 날짜를 가져오기 위해 임포트

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' # 템플릿에서 게시물 목록을 'posts'로 접근
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

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' # 템플릿에서 게시물 객체를 'post'로 접근

# PostAV (Archive View): 월별/연도별 아카이브 목록을 보여줍니다.
class PostAV(ListView):
    model = Post
    template_name = 'blog/post_archive.html'
    context_object_name = 'posts'
    date_field = 'created_at'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC')
        return context

# PostYAV (Year Archive View): 특정 연도의 게시물 목록을 보여줍니다.
class PostYAV(ListView):
    model = Post
    template_name = 'blog/post_archive.html' # post_archive.html 재사용
    context_object_name = 'posts'
    date_field = 'created_at'
    paginate_by = 10
    allow_empty = True
    year_format = '%Y'

    def get_queryset(self):
        return super().get_queryset().filter(created_at__year=self.kwargs['year']).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC')
        context['year'] = self.kwargs['year'] # 현재 연도 전달
        return context

# PostMAV (Month Archive View): 특정 월의 게시물 목록을 보여줍니다.
class PostMAV(ListView):
    model = Post
    template_name = 'blog/post_archive.html' # post_archive.html 재사용
    context_object_name = 'posts'
    date_field = 'created_at'
    paginate_by = 10
    allow_empty = True
    month_format = '%m'
    year_format = '%Y'

    def get_queryset(self):
        return super().get_queryset().filter(
            created_at__year=self.kwargs['year'],
            created_at__month=self.kwargs['month']
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC')
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        return context

# PostDAV (Day Archive View): 특정 일의 게시물 목록을 보여줍니다.
class PostDAV(ListView):
    model = Post
    template_name = 'blog/post_archive.html'
    context_object_name = 'posts'
    date_field = 'created_at'
    paginate_by = 10
    allow_empty = True
    day_format = '%d'
    month_format = '%m'
    year_format = '%Y'

    def get_queryset(self):
        return super().get_queryset().filter(
            created_at__year=self.kwargs['year'],
            created_at__month=self.kwargs['month'],
            created_at__day=self.kwargs['day']
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC')
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['day'] = self.kwargs['day']
        return context

# PostTAV (Today Archive View): 오늘 날짜의 게시물 목록을 보여줍니다.
class PostTAV(ListView):
    model = Post
    template_name = 'blog/post_archive.html'
    context_object_name = 'posts'
    date_field = 'created_at'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        today = timezone.localdate()
        return super().get_queryset().filter(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_list'] = Post.objects.dates('created_at', 'year', order='DESC')
        context['today'] = timezone.localdate()
        return context

# TagCloudTV (Tag Cloud View): 모든 태그를 보여줍니다.
class TagCloudTV(ListView):
    template_name = 'tag_cloud/unified_tag_cloud.html' # 템플릿 경로를 tag_cloud 앱의 것으로 명시
    context_object_name = 'tags'

    def get_queryset(self):
        # 모든 태그를 가져오고, 각 태그에 연결된 Post 객체와 Photo 객체의 수를 계산합니다.
        # 'post'는 Post 모델의 기본 related_name, 'photo'는 Photo 모델의 기본 related_name입니다.
        # TaggableManager의 related_name이 명시적으로 지정되지 않았다면 이 이름들을 사용합니다.
        return Tag.objects.annotate(
            num_blog_posts=Count('post'),  # Post 모델과의 관계를 통해 게시물 수 계산
            num_photos=Count('photo')      # Photo 모델과의 관계를 통해 사진 수 계산
        ).order_by('-num_blog_posts', '-num_photos') # 블로그 게시물 수, 그 다음 사진 수 기준으로 정렬

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # taggit_cloud.html에서 num_items를 사용하므로, num_blog_posts와 num_photos를 합쳐서 제공
        for tag in context['tags']:
            tag.num_items = tag.num_blog_posts + tag.num_photos
        return context

# SearchFV (Search Form View): 검색 결과를 보여줍니다.
class SearchFV(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        if search_keyword:
            return Post.objects.filter(
                Q(title__icontains=search_keyword) |
                Q(content__icontains=search_keyword) |
                Q(description__icontains=search_keyword) |
                Q(tags__name__icontains=search_keyword)
            ).distinct().order_by('-created_at')
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
