from django.views.generic import ListView
from taggit.models import Tag # Tag 모델 임포트
from django.db.models import Count, Q, F # Count, Q, F 함수 임포트
from blog.models import Post # Post 모델 임포트
from photo.models import Photo # Photo 모델 임포트

# 통합 태그 클라우드 뷰
class UnifiedTagCloudTV(ListView):
    template_name = 'tag_cloud/unified_tag_cloud.html' # 렌더링할 템플릿 파일 경로
    context_object_name = 'tags' # 템플릿에서 태그 목록을 'tags'로 접근

    def get_queryset(self):
        # 모든 태그를 가져오고, 각 태그에 연결된 블로그 게시물과 사진의 개수를 계산합니다.
        # TaggedItem을 통해 Post와 Photo를 구분하여 Count하는 방식을 사용합니다.
        
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
