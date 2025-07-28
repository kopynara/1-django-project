from django.contrib import admin
from .models import Bookmark, Category

# Category 모델을 관리자 페이지에 등록
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Bookmark 모델 등록 (owner 필드 추가)
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    # list_display에 'is_favorite' 추가하여 목록에서 볼 수 있도록 합니다.
    # is_favorite는 BooleanField이므로 체크박스 형태로 표시됩니다.
    list_display = ('title', 'url', 'category', 'description', 'thumbnail_url', 'owner', 'is_favorite', 'created_at', 'updated_at')
    
    # 'title' 필드를 클릭 가능한 링크로 설정합니다.
    # list_display에 있는 필드 중 하나여야 합니다.
    list_display_links = ('title',) # <-- 이 줄을 추가합니다.
    
    list_filter = ('category', 'owner', 'is_favorite', 'created_at') # 'owner'로 필터링 가능하도록 추가
    # search_fields에 'owner__username' 추가하여 소유자 이름으로 검색 가능하도록 합니다.
    search_fields = ('title', 'url', 'category__name', 'description', 'thumbnail_url', 'owner__username')
    ordering = ('-created_at',)

