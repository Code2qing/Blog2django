from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

from django.urls import reverse


# Create your views here.

def post_comment(request,post_id):
	post = get_object_or_404(Post,pk=post_id)

	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid():
			comment = form.save(commit=False)#不将数据提交到数据库，仅生成模型实例
			comment.post = post
			comment.save()

			return redirect(reverse('blog:detail',args=(post_id,)))

		else:
			comment_list =post.comment_set.order_by('-created_time').all()
			context={
			'post':post,
			'form':form,
			'comment_list':comment_list
			}

			return render(request,'blog/detail.html',context)

	else:
		return redirect(reverse('blog:detail',args=(post_id,)))