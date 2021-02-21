from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view  # <-- Here
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from posts import views
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- Here
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),    path('admin/', admin.site.urls),
    path('api/posts/', views.PostList.as_view()),
    path('api/posts/<int:pk>/', views.PostRetrievDestroy.as_view()),
    path('api/posts/<int:pk>/vote/', views.VoteCreate.as_view()),
    path('api/accounts/', include('user.urls')),
    # path('api/posts/<int:pk>/comment/', views.PostCommentList.as_view()),
    path('api/posts/<int:pk>/comment', views.Comment.as_view()),
    path('api/favorite/', views.FavoritePosts.as_view()),
]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
#для перехода и отображения изображения







