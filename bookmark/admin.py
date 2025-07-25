from django.contrib import admin
from .models import Bookmark, Category

# Category 모델을 관리자 페이지에 등록
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Bookmark 모델 등록 (is_favorite 필드 추가)
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    # list_display에 'is_favorite' 추가하여 목록에서 볼 수 있도록 합니다.
    # is_favorite는 BooleanField이므로 체크박스 형태로 표시됩니다.
    list_display = ('title', 'url', 'category', 'description', 'thumbnail_url', 'owner', 'is_favorite', 'created_at', 'updated_at')
    # list_filter에 'is_favorite' 추가하여 즐겨찾기 여부로 필터링 가능하도록 합니다.
    list_filter = ('category', 'owner', 'is_favorite', 'created_at')
    search_fields = ('title', 'url', 'category__name', 'description', 'thumbnail_url', 'owner__username')
    ordering = ('-created_at',)

