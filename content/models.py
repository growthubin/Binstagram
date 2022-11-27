from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()  # 글 내용
    image = models.TextField()  # 피드 이미지
    email = models.EmailField(default="")  # 글쓴이
    like_count = models.IntegerField()  # 좋아요 수

    class Meta:
        db_table = "content_feed"


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')  # 좋아요 누른 사람
    is_like = models.BooleanField(default=True)
    # 1 try1@gmail.com Y

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

class BookMark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')  # 좋아요 누른 사람
    is_marked = models.BooleanField(default=True)