from django.db import models
from user.models import User
from strategy.models import Strategy

# 文章类型
class ArticleType(models.Model):
    article_type = models.CharField('文章类型', unique=True, max_length=20)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'articletype'

# 文章
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=50)
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE)
    browse_nums = models.IntegerField('浏览数', default=0, null=True)
    collection = models.IntegerField('收藏数', default=0, null=True)
    good = models.IntegerField('赞', default=0, null=True)
    content = models.TextField()
    comments = models.IntegerField('评论数', default=0, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改时间', auto_now=True)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'article'

# 收藏
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection')
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, null=True, related_name='collection_strategy')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name='collection_article')
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'collection'

'''
class CommentType(models.Model):
    comment_type = models.CharField(max_length=10)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'commenttype'
'''

# 评论
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('内容')
    good = models.IntegerField('赞')
    send_time = models.DateTimeField('发送时间', auto_now_add=True)

    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'comment'

# 回复
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_id')     # 评论id
    content= models.TextField('内容')
    good = models.IntegerField('赞')
    replyuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_replay')         # 回复用户id
    touser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_to')            # 目标用户id
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'reply'