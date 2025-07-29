from django.views.generic import ListView, DetailView # ListView와 DetailView 임포트
from .models import Photo # Photo 모델 임포트
from taggit.models import Tag # Tag 모델 임포트 (taggit 사용을 위해)
from django.db.models import Q # Q 객체 임포트 (태그 필터링에 필요)

# Photo 목록을 보여주는 클래스 기반 뷰 (ListView)
class PhotoLV(ListView):
    model = Photo # 이 뷰가 사용할 모델은 Photo입니다.
    template_name = 'photo/photo_list.html' # 이 뷰가 렌더링할 템플릿 파일 경로
    context_object_name = 'photos' # 템플릿에서 사용할 객체 목록의 변수 이름 (기본값은 object_list)
    paginate_by = 6 # 한 페이지에 보여줄 사진의 개수 (페이지네이션)

    def get_queryset(self):
        # 기본 쿼리셋: 모든 사진을 최신 작성일 기준으로 정렬
        queryset = super().get_queryset().order_by('-created_at')

        # URL에서 tag_slug 파라미터 가져오기
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            # tag_slug가 있다면 해당 태그가 달린 사진만 필터링
            try:
                tag = Tag.objects.get(slug=tag_slug)
                queryset = queryset.filter(tags__in=[tag])
                self.tag_name = tag.name # 템플릿에 태그 이름 전달을 위해 저장
            except Tag.DoesNotExist:
                # 해당 태그가 존재하지 않을 경우 빈 쿼리셋 반환
                queryset = Photo.objects.none()
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

# Photo 상세 정보를 보여주는 클래스 기반 뷰 (DetailView)
class PhotoDV(DetailView):
    model = Photo # 이 뷰가 사용할 모델은 Photo입니다.
    template_name = 'photo/photo_detail.html' # 이 뷰가 렌더링할 템플릿 파일 경로
    context_object_name = 'photo' # 템플릿에서 사용할 단일 객체의 변수 이름 (기본값은 object)
