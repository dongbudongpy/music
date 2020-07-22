from django.shortcuts import render
from index.models import *
from django.views.generic import ListView

def rankingView(request):
    searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
    labels = Label.objects.all()
    t = request.GET.get('type', '')
    # 请求参数不为空
    if t:
        dynamics = Dynamic.objects.select_related('song').filter(song__label=t).order_by('-plays').all()[:10]
    else:
        dynamics = Dynamic.objects.select_related('song').order_by('-plays').all()[:10]
    return render(request, 'ranking.html', locals())

# 通用视图
class RankingList(ListView):
    # 设置HTML模板的某一个变量名称
    context_object_name = 'dynamics'
    # 设定模板文件
    template_name = 'ranking.html'
    def get_queryset(self):
        # 获取请求参数
        t = self.request.GET.get('type', '')
        # 参数不为空
        if t:
            dynamics = Dynamic.objects.select_related('song').filter(song__label=t).order_by('-plays').all()[:10]
        else:
            dynamics = Dynamic.objects.select_related('song').order_by('-plays').all()[:10]
        return dynamics

    # 添加其他变量
    def get_context_data(self, **kwargs):
        # 调用父类ListView中的方法
        context = super().get_context_data(**kwargs)
        # 搜索歌曲
        context['searchs'] = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
        # 所有歌曲分类
        context['labels'] = Label.objects.all()
        return context
