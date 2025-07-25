from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    # Django 관리자 페이지 URL
    path('admin/', admin.site.urls),

    # 웹사이트 루트 URL ('/')에 home 앱의 urls.py 포함
    path('', include('home.urls')),

    # 'bookmark/' 경로를 bookmark 앱의 urls.py로 전달
    path('bookmark/', include('bookmark.urls')),

    # 'blog/' 경로를 blog 앱의 urls.py로 전달
    path('blog/', include('blog.urls')),

    # 'photo/' 경로를 photo 앱의 urls.py로 전달
    path('photo/', include('photo.urls')),
]

if settings.DEBUG:
    # 미디어 파일 서빙 설정
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 정적 파일 서빙 설정 (STATICFILES_DIRS를 사용하도록)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
