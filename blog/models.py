from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
from django.utils import timezone
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
    	return self.name

    class Meta:
    	verbose_name = '分类'
    	verbose_name_plural= '分类'
class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = '标签'
		verbose_name_plural = '标签'
class Post(models.Model):
	title=models.CharField('标题',max_length=70)

	body = models.TextField()
	body_md = models.TextField("md格式内容",blank=True)
	created_time=models.DateTimeField('创建时间',default=timezone.now)
	modified_time=models.DateTimeField('修改时间',auto_now=True)

	excerpt = models.TextField('摘要',blank=True)
	category = models.ForeignKey(Category,related_name='posts',on_delete=models.SET_DEFAULT,default=1,verbose_name='分类')
	tags = models.ManyToManyField(Tag,blank=True,related_name='posts',verbose_name='标签')
	author = models.ForeignKey(User,related_name='posts',on_delete=models.SET_DEFAULT,default="admin",verbose_name='作者')
	views=models.IntegerField('阅读量',default=0)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})

	def increase_views(self):
		self.views+=1
		self.save(update_fields=['views'])

	#复写save方法
	def save(self,*args,**kwargs):
		
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			TocExtension(slugify = slugify),
		])

		self.body_md = md.convert(self.body)
		self.toc=md.toc
		
		models.Model.save(self,*args,**kwargs)
	class Meta:
		ordering = ['-created_time']
		verbose_name = '文章'
		verbose_name_plural = '文章'
