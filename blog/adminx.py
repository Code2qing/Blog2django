import xadmin
from .models import Post,Category,Tag
# Register your models here.
class PostAdmin():
	list_display=['title','created_time','modified_time','category','author']
xadmin.site.register(Post,PostAdmin)
xadmin.site.register(Category)
xadmin.site.register(Tag)