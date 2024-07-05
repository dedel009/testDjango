from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


#swagger 관련 urls 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Test API",    # 원하는 제목
        default_version='v1',   # 어플리케이션 버전
        description='TEST API 관련 개발',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='dedel009@ronfic.com'),
        license=openapi.License(name='Test License'),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated, ),
)


# 자동 URL 라우팅을 사용하여 API를 연결한다.
# 또한 검색 가능한 API에 대한 로그인 URL을 포함한다.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('search/', include('testApi.urls')),
    # path('', base_views.main, name='main'),
    path('', include(router.urls)),

]


urlpatterns += [
    # 라이브러리 관련 url
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('quickstart.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
