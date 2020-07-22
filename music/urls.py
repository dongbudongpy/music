
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings

# 配置各个app的url地址
urlpatterns = [
    path('admin/', admin.site.urls), # 后台
    path('', include('index.urls')), # 首页
    path('ranking/', include('ranking.urls')),
    path('play/', include('play.urls')),
    path('comment/', include('comment.urls')),
    path('search/', include('search.urls')),
    path('user/', include('user.urls')),
    # 定义静态资源的路由信息
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    # 定义媒体资源的路由信息
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]

# 自定义异常机制
from index import views

handler404 = views.page_not_found
handler500 = views.page_error
