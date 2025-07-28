from django.views.generic import ListView, DetailView # ListView와 DetailView 임포트
from .models import Photo # Photo 모델 임포트

# Photo 목록을 보여주는 클래스 기반 뷰 (ListView)
class PhotoLV(ListView):
    model = Photo # 이 뷰가 사용할 모델은 Photo입니다.
    template_name = 'photo/photo_list.html' # 이 뷰가 렌더링할 템플릿 파일 경로
    context_object_name = 'photos' # 템플릿에서 사용할 객체 목록의 변수 이름 (기본값은 object_list)
    paginate_by = 6 # 한 페이지에 보여줄 사진의 개수 (페이지네이션)

# Photo 상세 정보를 보여주는 클래스 기반 뷰 (DetailView)
class PhotoDV(DetailView):
    model = Photo # 이 뷰가 사용할 모델은 Photo입니다.
    template_name = 'photo/photo_detail.html' # 이 뷰가 렌더링할 템플릿 파일 경로
    context_object_name = 'photo' # 템플릿에서 사용할 단일 객체의 변수 이름 (기본값은 object)

