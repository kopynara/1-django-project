from django.urls import path
from .views import PhotoLV, PhotoDV # PhotoLV (List View), PhotoDV (Detail View) 임포트

app_name = 'photo' # 이 앱의 네임스페이스를 'photo'로 설정

urlpatterns = [
    # 사진 목록 페이지: /photo/
    path('', PhotoLV.as_view(), name='index'),
    
    # 사진 상세 페이지: /photo/사진ID/
    # Photo 모델의 get_absolute_url 메서드에서 id를 사용하므로, 여기에 <int:pk>를 사용합니다.
    path('<int:pk>/', PhotoDV.as_view(), name='detail'),
]
