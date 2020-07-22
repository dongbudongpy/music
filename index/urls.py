
from django.urls import path
from .views import *

# 由全局的url地址找过来 命名为index 交给视图函数idexView处理（需要先定义模型）
urlpatterns = [
    path('', indexView, name='index'),
]
