from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

# Category 모델
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='카테고리 이름')
    description = models.TextField(blank=True, verbose_name='설명')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'
        ordering = ['name']

    def __str__(self):
        return self.name

# Bookmark 모델 수정 (is_favorite 필드 추가)
class Bookmark(models.Model):
    title = models.CharField(max_length=100, verbose_name='제목')
    url = models.URLField(unique=True, verbose_name='URL')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='bookmarks',
        verbose_name='카테고리'
    )
    description = models.TextField(blank=True, verbose_name='설명/메모')
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name='썸네일 URL')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_bookmarks',
        verbose_name='소유자'
    )
    
    # 새로운 is_favorite 필드 추가
    # BooleanField: True/False 값을 저장합니다.
    # default=False: 기본값은 즐겨찾기가 아님으로 설정합니다.
    # verbose_name: Admin 페이지 등에서 사용자에게 보여줄 이름입니다.
    is_favorite = models.BooleanField(default=False, verbose_name='즐겨찾기')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookmark:detail', args=[self.pk])

