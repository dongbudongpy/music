from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import reverse
from django.db.models import Q, F
from index.models import *

# 获取url中的参数page
def searchView(request, page):
    # 重定向之后是get请求
    if request.method == 'GET':
        searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:6]
        # 获取搜索内容
        kword = request.session.get('kword', '')
        if kword:
            # Q对象 逻辑或 匹配歌曲名或歌手名 模糊匹配
            songs = Song.objects.filter(Q(name__icontains=kword) | Q(singer=kword)).order_by('-release').all()
        else:
            songs = Song.objects.order_by('-release').all()[:50]
        # 5首歌分一页
        paginator = Paginator(songs, 5)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        # 添加歌曲搜索次数
        if kword:
            # 精确匹配
            idList = Song.objects.filter(name__icontains=kword)
            for i in idList:
                dynamics = Dynamic.objects.filter(song_id=i.id)
                if dynamics:
                    # 若动态信息存在 则搜索次数加1 F对象 代表模型中一个字段的值
                    dynamics.update(search=F('search') + 1)
                else:
                    # 若动态信息不存在 则创建
                    dynamic = Dynamic(plays=0, search=1, download=0, song_id=i.id)
                    dynamic.save()
        return render(request, 'search.html', locals())
    else:
        # 用户点击搜索按钮时 发送post请求 此时将搜索内容写入session
        request.session['kword'] = request.POST.get('kword', '')
        # 点击搜索后 重定向至搜索页面 相当于发送get请求
        return redirect(reverse('search', kwargs={'page': 1}))