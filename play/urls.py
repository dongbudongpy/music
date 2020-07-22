
from django.urls import path
from .views import *
urlpatterns = [
    # 歌曲播放页 url变量与视图函数的参数一一对应
    path('<int:id>.html', playView, name='play'),
    # 歌曲下载
    path('download/<int:id>.html', downloadView, name='download')
]
