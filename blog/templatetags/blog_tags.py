from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count

register=template.Library()
@register.simple_tag
def get_posts_count():
	return Post.objects.all().count()

@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def get_archives():
	return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
	return Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
	# return Category.objects.all()

@register.simple_tag
def get_tags():	
	return Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
	# return Tag.objects.all()