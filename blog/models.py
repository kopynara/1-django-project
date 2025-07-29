from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager # Taggit 라이브러리 (태그 기능을 위해 필요)
from django.conf import settings # settings.AUTH_USER_MODEL을 사용하기 위해 임포트

class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField(verbose_name='SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField(verbose_name='DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField(verbose_name='CONTENT')
    
    created_at = models.DateTimeField(verbose_name='CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField(verbose_name='MODIFY DATE', auto_now=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='AUTHOR'
    )
    
    tags = TaggableManager(blank=True) # 태그 필드 추가

    class Meta:
        verbose_name = 'post' # 단수 별칭
        verbose_name_plural = 'posts' # 복수 별칭
        db_table = 'my_post' # 데이터베이스 테이블 이름 지정 (기존 'blog_posts'에서 'my_post'로 변경)
        ordering = ('-created_at',) # 기본 정렬 순서 (최신 생성일 기준 내림차순으로 변경)

    def __str__(self):
        return self.title # 객체를 문자열로 표현할 때 title 필드를 반환

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.slug,)) # slug 기반 URL (URL 패턴 이름 'post_detail'로 변경)

    def get_previous_post(self):
        return self.get_previous_by_created_at() # 이전 게시물 가져오기

    def get_next_post(self):
        return self.get_next_by_created_at() # 다음 게시물 가져오기
