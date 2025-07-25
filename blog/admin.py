# blog/admin.py

from django.contrib import admin
from blog.models import Post # Post 모델 임포트

@admin.register(Post) # Post 모델을 Admin 사이트에 등록
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt') # Admin 목록 페이지에 표시할 필드 (id, title, modify_dt만)
    list_filter = ('modify_dt',) # 필터링 옵션 추가
    search_fields = ('title', 'content') # 검색 필드 추가
    prepopulated_fields = {'slug': ('title',)} # title 입력 시 slug 자동 생성