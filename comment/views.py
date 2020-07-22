from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from django.http import Http404
from index.models import *
import time


def commentView(request, id):
    # 热搜歌曲
    searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:6]
    # 点评内容的提交功能
    if request.method == 'POST':
        # 获取页面的表单信息 默认为空 参数comment如何定义？？
        text = request.POST.get('comment', '')
        # 如果用户处于登录状态，则使用用户名，反之使用匿名用户
        if request.user.username:
            user = request.user.username
        else:
            user = '匿名用户'
        # 获取当前时间
        now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 如果存在
        if text:
            comment = Comment()
            comment.text = text
            comment.user = user
            comment.date = now
            comment.song_id = id
            comment.save()
        # 重定向comment页面 防止多次提交
        return redirect(reverse('comment', kwargs={'id': str(id)}))
    else:
        songs = Song.objects.filter(id=id).first()
        # 歌曲不存在抛出404异常
        if not songs:
            raise Http404('歌曲不存在')
        # 如果存在 获取当前歌曲的全部点评信息
        c = Comment.objects.filter(song_id=id).order_by('date')
        # 获取请求参数page 代表分页页数 默认为1 参数page如何定义？？
        page = int(request.GET.get('page', 1))
        # 每两条点评分一页
        paginator = Paginator(c, 2)
        try:
            pages = paginator.page(page) # 返回当前页
        except PageNotAnInteger:
            pages = paginator.page(1) # 返回首页
        except EmptyPage:
            pages = paginator.page(paginator.num_pages) # 返回最后一页
        return render(request, 'comment.html', locals())
