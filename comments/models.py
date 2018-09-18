from django.db import models
# Create your models here.
class Comment(models.Model):
	nickname = models.CharField('昵称',max_length=100)
	email = models.EmailField('邮箱',max_length=100)
	url = models.URLField('网址',blank=True)
	text = models.TextField('评论内容',blank=False)
	created_time = models.DateTimeField('评论时间',auto_now_add=True)
	post = models.ForeignKey('blog.Post',verbose_name='所属文章',on_delete=models.CASCADE)

	def __str__(self):
		return self.text[:20]

	class Meta:
		ordering = ['-created_time']
		verbose_name = '评论'
		verbose_name_plural = verbose_name