from django.contrib import admin
from .models import Photo # Photo 모델 임포트

# Photo 모델을 Django 관리자 페이지에 등록
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # 관리자 목록에 표시할 필드 정의
    # 'image_tag'는 나중에 썸네일 이미지를 보여주기 위해 추가할 커스텀 메서드입니다.
    list_display = ('title', 'author', 'created_at', 'updated_at', 'image_tag')
    
    # 목록에서 클릭하여 상세 페이지로 이동할 수 있는 필드 지정
    list_display_links = ('title',)
    
    # 필터링 옵션 추가
    list_filter = ('created_at', 'author', 'tags') # tags 필터 추가 (taggit 사용 시)
    
    # 검색 기능 필드 지정
    search_fields = ('title', 'description', 'author__username', 'tags__name') # 태그 이름으로도 검색 가능
    
    # Admin 페이지에서 객체 생성/수정 시 필드 순서 및 그룹화
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'description', 'author', 'tags')
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # 이 섹션을 기본적으로 접어둘 수 있습니다.
        }),
    )
    
    # 'created_at'과 'updated_at' 필드는 자동으로 채워지므로 읽기 전용으로 설정
    readonly_fields = ('created_at', 'updated_at')

    # Admin 목록에서 이미지 썸네일을 보여주기 위한 메서드 (나중에 추가)
    # 이 메서드는 list_display에 'image_tag'로 지정됩니다.
    def image_tag(self, obj):
        if obj.image:
            from django.utils.html import mark_safe
            # Admin 목록에서 클릭 가능한 작은 썸네일 이미지 표시
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto; border-radius: 5px;" />')
        return "No Image"
    
    image_tag.short_description = '썸네일' # Admin 목록 헤더 이름

