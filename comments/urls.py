from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
	path(r'comment/post/<int:post_id>/',views.post_comment,name='post_comment'),
	path(r'comment/check/<int:comment_id>/', views.check_comment, name="check_comment")
]