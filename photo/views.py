from django.views.generic import ListView, DetailView # ListView와 DetailView 임포트
from .models import Photo # Photo 모델 임포트
from taggit.models import Tag # Tag 모델 임포트 (taggit 사용을 위해)
from django.db import models # models.Count 사용을 위해 임포트
from django.db.models import Q, Count # Q 객체 및 Count 함수 임포트 (Q는 검색, Count는 집계에 필요)

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

# Photo 태그 클라우드 뷰 (모든 태그를 보여줌)
class PhotoTagCloudTV(ListView):
    template_name = 'photo/photo_tag_cloud.html' # 렌더링할 템플릿 파일 경로 (이 템플릿은 직접 생성해야 합니다)
    context_object_name = 'tags' # 템플릿에서 태그 목록을 'tags'로 접근

    def get_queryset(self):
        # 모든 태그를 가져오고, 각 태그에 연결된 Photo 객체의 수를 계산합니다.
        # 'photo'는 Photo 모델의 기본 related_name입니다.
        return Tag.objects.annotate(num_times=Count('photo')).order_by('-num_times')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # num_times를 템플릿에서 사용하기 위해 추가합니다.
        # 이 부분은 get_queryset에서 이미 처리되었으므로 추가적인 로직은 필요 없습니다.
        return context
