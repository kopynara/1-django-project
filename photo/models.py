from django.db import models
from django.contrib.auth.models import User # 사용자 모델 임포트
from django.urls import reverse # URL 패턴을 동적으로 가져오기 위해 임포트
from taggit.managers import TaggableManager # 태그 기능을 위해 임포트 (선택 사항이지만 블로그와 일관성 유지)

# Photo 모델 정의
class Photo(models.Model):
    # 제목 필드: 최대 500자, 필수 필드
    title = models.CharField(max_length=500, verbose_name='제목')
    
    # 이미지 파일 필드: 'photos/' 디렉토리에 저장될 이미지 파일
    # upload_to는 MEDIA_ROOT 아래의 경로를 의미합니다.
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='이미지 파일')
    
    # 설명 필드: 긴 텍스트를 위한 TextField, 필수는 아님 (blank=True)
    description = models.TextField(blank=True, verbose_name='설명')
    
    # 작성일 필드: 객체가 처음 생성될 때 자동으로 현재 날짜와 시간으로 설정
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    # 수정일 필드: 객체가 저장될 때마다 자동으로 현재 날짜와 시간으로 업데이트
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    # 작성자 필드: Django의 기본 User 모델과 1:N 관계 (ForeignKey)
    # on_delete=models.CASCADE는 User가 삭제되면 해당 User가 작성한 Photo도 함께 삭제됨을 의미
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')

    # 태그 기능 추가 (django-taggit 활용)
    # blank=True는 태그가 필수가 아님을 의미합니다.
    tags = TaggableManager(blank=True)

    # 메타 클래스: 모델의 옵션을 정의합니다.
    class Meta:
        # 테이블 이름을 명시적으로 지정 (선택 사항, 기본값은 '앱이름_모델이름')
        db_table = 'photo'
        # 기본 정렬 순서: 작성일 기준 내림차순 (최신 글이 먼저 오도록)
        ordering = ['-created_at']
        # Admin 페이지 등에서 보여질 모델의 단수/복수 이름 설정
        verbose_name = '사진'
        verbose_name_plural = '사진들'

    # 객체의 문자열 표현을 정의합니다. (Admin 페이지 등에서 객체를 쉽게 식별할 수 있도록)
    def __str__(self):
        return self.title

    # 객체의 절대 URL을 반환하는 메서드 (URLconf와 연결)
    # 이 메서드는 나중에 템플릿에서 photo.get_absolute_url과 같이 사용될 것입니다.
    def get_absolute_url(self):
        # 'photo:detail'은 photo 앱의 detail 뷰에 연결된 URL 패턴 이름이어야 합니다.
        # 아직 photo 앱의 URLconf를 만들지 않았으므로, 임시로 'photo_detail'과 같은 이름을 사용하거나,
        # 나중에 URLconf를 정의할 때 이 부분을 수정해야 합니다.
        # 여기서는 Django의 reverse 함수를 사용하여 Photo 상세 페이지의 URL을 동적으로 생성합니다.
        # Photo 모델은 일반적으로 slug 필드를 가지지 않으므로, id를 사용하여 고유 URL을 생성합니다.
        return reverse('photo:detail', args=[self.id])
