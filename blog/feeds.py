from django.contrib.syndication.views import Feed
from .models import Post
import markdown

class AllPostsRssFeed(Feed):
	title = "黑白格"

	link = '/'

	description ='黑白格'

	def items(self):
		return Post.objects.all()

	def item_title(self,item):
		return '[{}] {}'.format(item.category,item.title)

	def item_description(self,item):
		return item.body