from django.contrib import admin
from .models import Post # Post 모델 임포트

# Post 모델을 관리자 페이지에 등록
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 관리자 목록에 표시할 필드
    list_display = ('title', 'slug', 'author', 'created_at', 'modify_dt')
    
    # 'title' 필드를 클릭 가능한 링크로 설정합니다.
    # list_display에 있는 필드 중 하나여야 합니다.
    list_display_links = ('title',) # <-- 이 줄을 추가합니다.
    
    # 필터링 가능한 필드
    list_filter = ('created_at', 'author')
    
    # 검색 가능한 필드
    search_fields = ('title', 'content', 'author__username') # content도 검색 가능하도록 추가
    
    # slug 필드를 자동으로 채워주도록 설정
    prepopulated_fields = {'slug': ('title',)}
    
    # 기본 정렬 순서
    ordering = ('-created_at',)

