from django.db import models
import os

# 动态生成上传头像路径
def get_avatar_path(user,filename):
    return os.path.join('user','avatar',user.username,filename)

# 用户
class User(models.Model):

    username = models.CharField('用户名',max_length=8 ,unique=True)
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    password = models.CharField('密码', max_length=50)
    email = models.EmailField('邮箱')
    phone = models.CharField('手机号', max_length=11)
    info = models.CharField(max_length=150,verbose_name='个人简介')
    avatar = models.ImageField(upload_to=get_avatar_path, null=True)       # 用户头像
    created_date = models.DateField('注册日期', auto_now_add=True)

    class Meta:
        db_table = 'user'

# 关注,被关注
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')    # 关注者（粉丝）
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')    # 被关注

    class Meta:
        db_table = 'follow'

