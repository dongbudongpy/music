
from django.urls import path
from .views import *
urlpatterns = [
    path('<int:id>.html', commentView, name='comment'), # 参数id是播放页面的id
]
