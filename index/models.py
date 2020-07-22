from django.db import models

# 总共定义5张表 歌曲相关4张 用户信息1张
# 以歌曲信息表为中心 与这里其他歌曲三张表构成一对一或一对多的关系
# 实际数据库中显示为index_label index_song index_dynamic index_comment

# 歌曲分类表 与Song表构成一对多关系 外键写在多的那一边
# 实际中可以重构为多对多
class Label(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('分类标签', max_length=10)

    # 打印类的实例对象时调用该方法 一般返回一个字符串 显示给用户
    def __str__(self):
        return self.name

    class Meta:
        # 元类 设置Admin后台系统的显示内容
        verbose_name = '歌曲分类'
        verbose_name_plural = '歌曲分类'

# 歌曲信息表 与Dynamic表构成一对一 与Comment表构成一对多
class Song(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('歌名', max_length=50)
    singer = models.CharField('歌手', max_length=50)
    time = models.CharField('时长', max_length=10)
    album = models.CharField('专辑', max_length=50)
    languages = models.CharField('语种', max_length=20)
    type = models.CharField('类型', max_length=20)
    release = models.DateField('发行时间')
    img = models.FileField('歌曲图片', upload_to='songImg/')
    lyrics = models.FileField('歌词', upload_to='songLyric/', default='暂无歌词', blank=True)
    file = models.FileField('歌曲文件', upload_to='songFile/')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='歌曲分类')


    def __str__(self):
        return self.name

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '歌曲信息'
        verbose_name_plural = '歌曲信息'


# 歌曲动态表
class Dynamic(models.Model):
    id = models.AutoField('序号', primary_key=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌名')
    plays = models.IntegerField('播放次数', default=0)
    search = models.IntegerField('搜索次数', default=0)
    download = models.IntegerField('下载次数', default=0)

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '歌曲动态'
        verbose_name_plural = '歌曲动态'


# 歌曲点评表
class Comment(models.Model):
    id = models.AutoField('序号', primary_key=True)
    text = models.CharField('内容', max_length=500)
    user = models.CharField('用户', max_length=20)
    date = models.DateField('日期', auto_now=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌名')

    class Meta:
        # 设置Admin的显示内容
        verbose_name = '歌曲评论'
        verbose_name_plural = '歌曲评论'
